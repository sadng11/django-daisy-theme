import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User


def test_changelist_template_exists_and_loads():
    rf = RequestFactory()
    request = rf.get("/admin/auth/user/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string(
        "admin/change_list.html",
        {
            "title": "Select user to change",
            "module_name": "users",
            "has_add_permission": True,
            "user": user,
            "daisy_theme": {
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "auto",
                "AVAILABLE_THEMES": ["light", "dark"],
                "SHOW_THEME_SWITCHER": True,
                "COLLAPSIBLE_SIDEBAR": True,
                "SHOW_BREADCRUMBS": True,
                "FOOTER_TEXT": "Powered by django-daisy-theme",
                "SHOW_VERSION": True,
            },
        },
        request=request,
    )
    assert "daisy-changelist" in rendered or "table table-zebra" in rendered
    assert "admin-filter-drawer" in rendered or "Filter" in rendered
