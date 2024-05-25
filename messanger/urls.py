from django.urls import path

from messanger import views


app_name = "messanger"

urlpatterns = [
    path("", views.chats_page, name="chats_page"),
    path('upload/', views.upload_photo, name='upload_photo'),
    path("<str:username>/", views.dialogue_page, name="dialogue"),
]
