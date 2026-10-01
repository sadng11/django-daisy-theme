import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User


def test_changeform_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/auth/user/add/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string(
        "admin/change_form.html",
        {
            "title": "Add user",
            "has_change_permission": True,
            "has_add_permission": True,
            "has_delete_permission": False,
            "save_as": False,
            "show_save": True,
            "show_save_and_continue": True,
            "show_save_and_add_another": True,
            "show_delete_link": False,
            "opts": User._meta,
            "add": True,
            "change": False,
            "is_popup": False,
            "has_view_permission": True,
            "has_editable_inline_admin_formsets": False,
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
    assert "<form" in rendered
    assert "daisy-changeform" in rendered or "submit-row" in rendered or "sticky bottom-0" in rendered


def test_changeform_popup_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/shop/product/add/?_popup=1")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    rendered = render_to_string(
        "admin/change_form.html",
        {
            "title": "Add product",
            "has_change_permission": True,
            "has_add_permission": True,
            "has_delete_permission": False,
            "save_as": False,
            "show_save": True,
            "opts": User._meta,
            "add": True,
            "change": False,
            "is_popup": True,
            "has_view_permission": True,
            "has_editable_inline_admin_formsets": False,
            "show_save_and_continue": False,
            "show_save_and_add_another": False,
            "show_delete_link": False,
            "user": user,
            "daisy_theme": {
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "auto",
            },
        },
        request=request,
    )
    assert "<form" in rendered
    assert "drawer lg:drawer-open" not in rendered
    assert "submit" in rendered

