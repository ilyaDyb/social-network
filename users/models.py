from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from tools import tools_get_timestamp


class Users(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        ("username"),
        max_length=150,
        unique=True,
        db_index=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    avatar = models.ImageField(upload_to="users_avatars", blank=True, null=True, default="User-avatar.svg.png")
    friends = models.ManyToManyField("self", through="Friendship", related_name="user_friends")

    # PRIVACY_CHOICE = (("yes", "yes"), ("no", "no"))
    # privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICE, default="no")

    class Meta:
        db_table = "Users"

    @property
    def accepted_friends(self):
        from_user_friendships = Friendship.objects.filter(from_user=self, status='accepted').values_list('to_user', flat=True)
        to_user_friendships = Friendship.objects.filter(to_user=self, status='accepted').values_list('from_user', flat=True)
        friends_ids = set(list(from_user_friendships) + list(to_user_friendships))
        return Users.objects.filter(id__in=friends_ids)
    
    def __str__(self) -> str:
        return f"{self.username}:{self.pk}"

class UserProfile(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE, related_name="user_profile")
    small_info = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = ("Userprofile")
        verbose_name_plural = ("Userprofiles")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Userprofile_detail", kwargs={"pk": self.pk})


class Friendship(models.Model):
    STATUS_CHOICES = (
        ("pending", "pending"),
        ("accepted", "accepted"),
    )
    from_user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="from_user", default=None)
    to_user = models.ForeignKey(to=Users, on_delete=models.CASCADE,related_name="to_user", default=None)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        verbose_name = ("Friendship")
        verbose_name_plural = ("Friendships")

    def get_absolute_url(self):
        return reverse("Friendship_detail", kwargs={"pk": self.pk})
    

class UserActivity(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE, related_name="activity")
    last_activity = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=None)

    def __str__(self):
        return f"{self.user.username} is {'onine' if self.is_online else 'offline'}"
    
    def get_last_activity(self):
        return tools_get_timestamp(timestamp=self.last_activity)