import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser, User


def test_login_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/login/")
    request.user = AnonymousUser()
    rendered = render_to_string(
        "admin/login.html",
        {
            "title": "Log in",
            "app_path": "/admin/login/",
            "daisy_theme": {
                "SITE_HEADER": "Test Daisy Admin",
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "auto",
                "AVAILABLE_THEMES": ["light", "dark"],
                "LOAD_DEFAULT_FONTS": True,
            },
        },
        request=request,
    )
    assert "Test Daisy Admin" in rendered
    assert "daisy-theme.min.css" in rendered
    assert "<form" in rendered
    assert "input" in rendered


def test_base_site_renders_with_user():
    rf = RequestFactory()
    request = rf.get("/admin/")
    user = User(username="superuser", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string(
        "admin/base_site.html",
        {
            "title": "Site administration",
            "user": user,
            "daisy_theme": {
                "SITE_TITLE": "Admin Title",
                "SITE_HEADER": "Admin Header",
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "auto",
                "AVAILABLE_THEMES": ["light", "dark"],
                "LOAD_DEFAULT_FONTS": True,
                "SHOW_THEME_SWITCHER": True,
                "COLLAPSIBLE_SIDEBAR": True,
                "SHOW_BREADCRUMBS": True,
                "FOOTER_TEXT": "Powered by django-daisy-theme",
                "SHOW_VERSION": True,
            },
        },
        request=request,
    )
    assert "Admin Header" in rendered
    assert "superuser" in rendered
    assert "drawer" in rendered
    assert "sidebar" in rendered
