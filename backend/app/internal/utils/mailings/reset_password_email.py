from app.internal.utils.mailings.send_email import send_email
from config import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode


def send_reset_password_email(user_data, request):
    user = get_user_model().objects.get(username=user_data["username"])
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    activation_url = settings.PASSWORD_RESET_CONFIRM_URL
    current_site = get_current_site(request).domain
    url = f"http://{current_site}{activation_url}?token={token}&uid={uidb64}"

    mail_data = [
        "Сброс пароля",
        f"Пожалуйста, перейдите по следующей ссылке, чтобы сбросить пароль: {url}",
        [user_data["email"]],
    ]
    send_email(*mail_data)
