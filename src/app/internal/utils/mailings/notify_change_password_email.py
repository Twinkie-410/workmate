from app.internal.utils.mailings.send_email import send_email


def notify_change_password(user_data, request):
    mail_data = ["Пароль был изменён", "Уведомляем, что пароль на вашем аккаунте был изменён", [user_data["email"]]]
    send_email(*mail_data)
