import datetime
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator


class DummyAction:
    def __init__(self, user):
        self.action_time = datetime.datetime(2026, 10, 1, 12, 0)
        self.user = user
        self.is_addition = False
        self.is_change = True
        self.is_deletion = False

    def get_action_flag_display(self):
        return "Change"

    def get_change_message(self):
        return "Changed name."


def test_object_history_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/auth/group/1/history/")
    user = User(username="admin", is_staff=True, is_superuser=True)
    request.user = user

    group = Group(id=1, name="Store Managers")
    action = DummyAction(user=user)

    paginator = Paginator([action], 10)
    page_obj = paginator.get_page(1)

    rendered = render_to_string(
        "admin/object_history.html",
        {
            "title": "Change history: Store Managers",
            "opts": Group._meta,
            "module_name": "Groups",
            "object": group,
            "action_list": page_obj,
            "page_range": [1],
            "page_var": "p",
            "pagination_required": False,
            "has_change_permission": True,
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
    assert "daisy-history" in rendered
    assert "table" in rendered
    assert "breadcrumbs" in rendered
    assert "Changed name." in rendered
