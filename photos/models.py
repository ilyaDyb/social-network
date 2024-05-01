from django.db import models
from django.urls import reverse

from users.models import Users

# Create your models here.
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