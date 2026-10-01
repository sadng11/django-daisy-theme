import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User


def test_index_dashboard_renders():
    rf = RequestFactory()
    request = rf.get("/admin/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    app_list = [
        {
            "name": "Authentication and Authorization",
            "app_label": "auth",
            "app_url": "/admin/auth/",
            "has_module_perms": True,
            "models": [
                {
                    "name": "Users",
                    "object_name": "User",
                    "admin_url": "/admin/auth/user/",
                    "add_url": "/admin/auth/user/add/",
                    "view_only": False,
                },
                {
                    "name": "Groups",
                    "object_name": "Group",
                    "admin_url": "/admin/auth/group/",
                    "add_url": "/admin/auth/group/add/",
                    "view_only": False,
                },
            ],
        }
    ]
    rendered = render_to_string(
        "admin/index.html",
        {
            "app_list": app_list,
            "user": user,
            "title": "Site administration",
            "is_index": True,
            "daisy_theme": {
                "SITE_TITLE": "Admin Title",
                "SITE_HEADER": "Admin Header",
                "SHOW_RECENT_ACTIONS": True,
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
    assert "Authentication and Authorization" in rendered
    assert "Users" in rendered
    assert "Groups" in rendered
    assert "/admin/auth/user/add/" in rendered
    assert "daisy-dashboard" in rendered or "card bg-base-100" in rendered
    assert "daisy-stat-card" in rendered or "stats shadow" in rendered


def test_error_404_renders():
    rf = RequestFactory()
    request = rf.get("/admin/nonexistent/")
    rendered = render_to_string(
        "admin/404.html",
        {
            "title": "Page not found",
            "daisy_theme": {"SITE_TITLE": "Admin Title", "DEFAULT_THEME": "light"},
        },
        request=request,
    )
    assert "404" in rendered or "not found" in rendered.lower()
