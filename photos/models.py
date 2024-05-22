from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

from users.models import Users

# Create your models here.
class Photo(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="photos")
    photo = models.FileField(upload_to="users_photos", blank=True, null=True,
                            validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])])
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.pk} {self.user.username}'s photo"
    
    class Meta:
        verbose_name = ("Photo")
        verbose_name_plural = ("Photos")

