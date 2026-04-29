from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .forms import StyledPasswordChangeForm


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signup/pending/", views.signup_pending, name="signup_pending"),
    path("signup/resend/", views.resend_signup_confirmation, name="resend_signup_confirmation"),
    path("signup/confirm/<uuid:token>/", views.confirm_signup, name="confirm_signup"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            form_class=StyledPasswordChangeForm,
            template_name="accounts/password_change_form.html",
            success_url=reverse_lazy("password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("confirm-email/<uidb64>/<token>/", views.confirm_email, name="confirm_email"),
    path("confirm-email/resend/", views.resend_confirmation_email, name="resend_confirmation_email"),
]
