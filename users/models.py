from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Users(AbstractUser):
    first_name = models.CharField(max_length=20, blank=False, null=False)
    last_name = models.CharField(max_length=20, blank=False, null=False)
    avatar = models.ImageField(upload_to="users_avatars", blank=True, null=True, default="User-avatar.svg.png")
    friends = models.ManyToManyField("self", through="Friendship")

    class Meta:
        db_table = "Users"

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

class Photo(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="photo")

    photo = models.FileField(upload_to="users_files/users_photos/", blank=True, null=True)
    class Meta:
        verbose_name = ("Photo")
        verbose_name_plural = ("Photos")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Photo_detail", kwargs={"pk": self.pk})
    
# class Settings(models.Model):
#     PRIVACY_CHOICE = (("yes", "yes"), ("no", "no"))
#     user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
#     privacy = models.CharField(max_length=3, choices=PRIVACY_CHOICE, default="no")

#     class Meta:
#         verbose_name = ("Settings")
#         verbose_name_plural = ("Settingss")

#     def __str__(self):
#         return f"Settings for user: {self.user.id}"

#     def get_absolute_url(self):
#         return reverse("Settings_detail", kwargs={"pk": self.pk})


# class Audio(models.Model):
#     title = models.CharField(max_length=35, null=False)
#     audio_file = models.FileField(upload_to="users_files/audio_files/")
#     class Meta:
#         verbose_name = _("Audio")
#         verbose_name_plural = _("Audios")

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse("Audio_detail", kwargs={"pk": self.pk})
