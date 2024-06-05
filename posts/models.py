from django.db import models
from django.urls import reverse

from tools import tools_get_timestamp
from users.models import Users


class Post(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="text_content", null=True, blank=True)
    image = models.FileField(upload_to="post_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Users, related_name="liked_posts")

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return f"{self.pk} {self.user.username}'s post"

    def get_absolute_url(self):
        return reverse("Posts_detail", kwargs={"pk": self.pk})
    
    def get_timestamp(self):
        return tools_get_timestamp(timestamp=self.created_at)


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments", default=None)
    file = models.FileField(upload_to="comment_images", null=True, blank=True)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Comment from {self.user} to post: {self.post.pk}"


class Answer(models.Model):
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="answer_images", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answer_to = models.ForeignKey(to=Users, on_delete=models.CASCADE, related_name="user_answers")

    def __str__(self):
        return f"{self.pk} answer by {self.user.username} to {self.answer_to.username}"