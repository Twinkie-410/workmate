from django.conf import settings
from django.core.mail import send_mail


def send_email(email_subject, email_body, to_email):
    from_email = settings.EMAIL_HOST_USER + settings.EMAIL_DOMAIN
    send_mail(email_subject, email_body, from_email, to_email)
