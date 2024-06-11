import datetime
from email.mime.text import MIMEText
import smtplib
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from application import settings
from users.models import TemporaryUser, Users

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
    

@shared_task
def delete_empty_Temporary_User():
    time_diff = timezone.now() - datetime.timedelta(days=1)
    temprary_users = TemporaryUser.objects.filter(created_at__lte=time_diff)
    # temprary_users = TemporaryUser.objects.all()
    with transaction.atomic():
        temp_users_ids = [temp_user.user.id for temp_user in temprary_users]
        Users.objects.filter(id__in=temp_users_ids, is_active=False).delete()
        temprary_users.delete()
            
    print(f"Deleted {len(temp_users_ids)} temporary users and corresponding users.")