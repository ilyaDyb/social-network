from django.urls import path

from . import views


app_name = "messanger"

urlpatterns = [
    path("", views.chats_page, name="chats_page"),
    path('upload/', views.upload_file, name='upload_file'),
    path("<str:username>/", views.dialogue_page, name="dialogue"),
]
