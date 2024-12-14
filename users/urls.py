from django.urls import path, include
from .import views as views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("accounts/", include("allauth.urls")),
    path("logout/", views.logout_view, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate_user, name="activate"),
    path("reset-password/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="reset_password"),
    path("reset-mail_sent/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_form.html"), name="password_reset_confirm"),
    path("reset-password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_done.html"), name="password_reset_complete"),
]
