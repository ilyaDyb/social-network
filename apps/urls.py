from django.urls import path

from apps import views


app_name = "apps"

urlpatterns = [
    path("", views.index, name="index"),

    path("ai-images/", views.ai_images, name="ai_images"),
    path("ai-images/generate-image/", views.generate_image, name="generate_image"),

    path("avatars-RandM/", views.avatar_rick_and_morty, name="generate_avatar_rick_and_morty"),
    path("avatars-RandM/generate/", views.avatar_rick_and_morty_generate, name="generate_avatar_rick_and_morty_generate"),
]
