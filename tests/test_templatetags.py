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

