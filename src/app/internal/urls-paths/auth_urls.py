from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.internal.views.auth_view import (
    ChangeEmailAPIView,
    ChangePasswordAPIView,
    EmailConfirmAPIView,
    LoginAPIView,
    LogoutAPIView,
    RequestResetPasswordAPIView,
    SetNewPasswordAPIView,
    UserRegisterAPIView,
)

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("confirm_email/", EmailConfirmAPIView.as_view(), name="confirm-email"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("change-email/", ChangeEmailAPIView.as_view(), name="change-email"),
    # Reset password
    path("request-pass-reset/", RequestResetPasswordAPIView.as_view(), name="request-pass-reset"),
    path("password-reset-complete/", SetNewPasswordAPIView.as_view(), name="password-reset-complete"),
    # Tokens
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
