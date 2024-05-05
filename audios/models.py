from django.db import models
from django.urls import reverse

from users.models import Users

class Audio(models.Model):
    title = models.CharField(max_length=35, null=False, db_index=True)
    author = models.CharField(max_length=20, null=False, db_index=True)
    audio_file = models.FileField(upload_to="audio_files")
    
    class Meta:
        verbose_name = ("Audio")
        verbose_name_plural = ("Audios")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Audio_detail", kwargs={"pk": self.pk})

class UserAudio(models.Model):
    audio = models.ForeignKey(to=Audio, on_delete=models.CASCADE, related_name="user_audios")
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="user_audios")
    

    class Meta:
        verbose_name = ("UserAudio")
        verbose_name_plural = ("UserAudios")

    def __str__(self):
        return f"{self.audio.title} - {self.user.username}"

    def get_absolute_url(self):
        return reverse("UserAudio_detail", kwargs={"pk": self.pk})


