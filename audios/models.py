from django.db import models

# class Audio(models.Model):
#     title = models.CharField(max_length=35, null=False)
#     audio_file = models.FileField(upload_to="audio_files")
#     class Meta:
#         verbose_name = ("Audio")
#         verbose_name_plural = ("Audios")

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse("Audio_detail", kwargs={"pk": self.pk})

