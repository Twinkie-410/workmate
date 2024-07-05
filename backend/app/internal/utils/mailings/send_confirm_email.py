from app.internal.utils.mailings.send_email import send_email
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken


def send_confirm_email(user_data, request, to=None):
    user = get_user_model().objects.get(username=user_data["username"])
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    activation_url = reverse_lazy("confirm-email")
    if to is None:
        to = user_data["email"]

    url = f"http://{current_site}/{activation_url}?token={token}&change-to={to}"
    mail_data = [
        "Подтвердите свой электронный адрес",
        f"Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {url}",
        [to],
    ]
    send_email(*mail_data)
