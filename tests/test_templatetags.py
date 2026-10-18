import pytest
from django.test import RequestFactory
from django.utils import translation
from django_daisy_theme.context_processors import daisy_theme_context
from django_daisy_theme.templatetags.daisy_theme import (
    daisy_direction,
    daisy_theme_attr,
    daisy_icon,
    daisy_config,
    daisy_sidebar_apps,
)


def test_context_processor():
    rf = RequestFactory()
    request = rf.get("/admin/")
    ctx = daisy_theme_context(request)
    assert "daisy_theme" in ctx
    assert ctx["daisy_theme"]["DEFAULT_THEME"] == "light"
    assert ctx["daisy_theme"]["SITE_HEADER"] == "Daisy Theme Admin"


def test_direction_auto_persian():
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("fa"):
        assert daisy_direction(request) == "rtl"


def test_direction_auto_arabic():
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("ar"):
        assert daisy_direction(request) == "rtl"


def test_direction_auto_english():
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("en"):
        assert daisy_direction(request) == "ltr"


def test_direction_forced(settings):
    settings.DAISY_THEME_CONFIG = {"DIRECTION": "rtl"}
    rf = RequestFactory()
    request = rf.get("/admin/")
    with translation.override("en"):
        assert daisy_direction(request) == "rtl"


def test_daisy_theme_attr():
    assert daisy_theme_attr() == "light"


def test_daisy_config_tag():
    assert daisy_config("DEFAULT_THEME") == "light"
    assert daisy_config("NON_EXISTING_KEY", "fallback") == "fallback"


def test_daisy_icon_rendering():
    svg = daisy_icon("home", css_class="w-5 h-5")
    assert "<svg" in svg
    assert "w-5 h-5" in svg
    assert "</svg>" in svg


def test_daisy_icon_fallback():
    svg = daisy_icon("non_existing_icon_name")
    assert "<svg" in svg
    assert "lucide-help-circle" in svg or "<circle" in svg


def test_daisy_sidebar_apps():
    # Context with available_apps (standard admin changelist/changeform)
    ctx1 = {"available_apps": [{"name": "Shop", "models": []}]}
    assert len(daisy_sidebar_apps(ctx1)) == 1
    assert daisy_sidebar_apps(ctx1)[0]["name"] == "Shop"

    # Context with app_list fallback (admin index)
    ctx2 = {"app_list": [{"name": "Auth", "models": []}]}
    assert len(daisy_sidebar_apps(ctx2)) == 1
    assert daisy_sidebar_apps(ctx2)[0]["name"] == "Auth"

    # Empty context
    assert daisy_sidebar_apps({}) == []
    assert daisy_sidebar_apps(None) == []


def test_daisy_icon_palette():
    svg = daisy_icon("palette", css_class="w-4 h-4")
    assert "<svg" in svg
    assert "lucide-palette" in svg
    assert "w-4 h-4" in svg


def test_theme_toggle_template_rendering(admin_client):
    response = admin_client.get("/admin/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "Select Theme" in html
    assert "data-theme=" in html
    assert "lucide-palette" in html
    assert "w-72" in html


def test_zero_config_fallback_rendering():
    from django.template.loader import render_to_string
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser

    rf = RequestFactory()
    request = rf.get("/admin/login/")
    request.user = AnonymousUser()

    # Context without any 'daisy_theme' or context processor
    rendered = render_to_string("admin/login.html", {}, request=request)
    assert "fonts.css" in rendered
    assert "select2-init.js" in rendered
    assert "Select Theme" in rendered
    assert "daisy-theme.min.css" in rendered


