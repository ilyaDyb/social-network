from django.urls import path
from posts import views


app_name = "posts"

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("like-post/", views.like_post, name="like_post"),
]
