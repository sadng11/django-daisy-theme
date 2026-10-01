import pytest
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.test import RequestFactory


@pytest.mark.django_db
def test_password_change_form_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/password_change/")
    user = User.objects.create_user(username="admin", is_staff=True, is_superuser=True)
    request.user = user
    form = PasswordChangeForm(user=user)

    rendered = render_to_string(
        "registration/password_change_form.html",
        {
            "title": "Password change",
            "form": form,
            "user": user,
            "daisy_theme": {
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "rtl",
                "SHOW_BREADCRUMBS": True,
            },
        },
        request=request,
    )

    assert "card bg-base-100" in rendered
    assert "btn btn-primary" in rendered
    assert "old_password" in rendered
    assert "new_password1" in rendered
    assert "new_password2" in rendered


@pytest.mark.django_db
def test_password_change_done_template_renders():
    rf = RequestFactory()
    request = rf.get("/admin/password_change/done/")
    user = User.objects.create_user(username="admin_done", is_staff=True, is_superuser=True)
    request.user = user

    rendered = render_to_string(
        "registration/password_change_done.html",
        {
            "title": "Password change successful",
            "user": user,
            "daisy_theme": {
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "rtl",
                "SHOW_BREADCRUMBS": True,
            },
        },
        request=request,
    )

    assert "card bg-base-100" in rendered
    assert "btn btn-primary" in rendered


@pytest.mark.django_db
def test_admin_user_change_password_template_renders():
    rf = RequestFactory()
    user = User.objects.create_user(username="target_user", is_staff=False)
    admin_user = User.objects.create_user(username="superuser", is_staff=True, is_superuser=True)
    request = rf.get(f"/admin/auth/user/{user.pk}/password/")
    request.user = admin_user
    form = AdminPasswordChangeForm(user=user)

    rendered = render_to_string(
        "admin/auth/user/change_password.html",
        {
            "title": "Change password",
            "original": user,
            "opts": User._meta,
            "form": form,
            "user": admin_user,
            "daisy_theme": {
                "DEFAULT_THEME": "light",
                "DARK_THEME": "dark",
                "DIRECTION": "rtl",
                "SHOW_BREADCRUMBS": True,
            },
        },
        request=request,
    )

    assert "card bg-base-100" in rendered
    assert "btn btn-primary" in rendered
    assert "password1" in rendered
