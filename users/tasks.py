from email.mime.text import MIMEText
import smtplib
from celery import shared_task
from application import settings

@shared_task
def send_email_for_confirmation(email, token) -> None:
    sender = settings.MAIL_HOST_USER
    password = settings.MAIL_HOST_USER_PASSWORD

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        if token:
            message = f"Your link for confirm: {settings.SITE_PROTOCOL}{settings.SITE_URL}/registration/verify/{token}"
        else:
            return Exception("Token is missed")
        msg = MIMEText(message)
        msg["From"] = "Social-network DI"
        msg["Subject"] = "Confirm your email"
        server.sendmail(sender, email, msg.as_string())

    except Exception as ex:
        return ex