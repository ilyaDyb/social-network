from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True, null=True)

    class Meta:
        db_table = "Users"