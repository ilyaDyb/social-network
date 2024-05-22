from django.db import models
from django.urls import reverse

from users.models import Users


class Post(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="text_content", null=True, blank=True)
    image = models.FileField(upload_to="post_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Users, related_name="liked_posts")
    comments = models.ManyToManyField('Comment', related_name="posts")

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return f"{self.pk} {self.user.username}'s post"

    def get_absolute_url(self):
        return reverse("Posts_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


# class Answer(models.Model):
#     ... #foreign key with comment