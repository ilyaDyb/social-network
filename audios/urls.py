
from django.urls import path

from audios import views


app_name = "audios"
urlpatterns = [
    path("audios/load/", views.load_audio, name="load_audio"),
    path("audios/add-audio/", views.add_audio, name="add_audio"),
    path("audios/delete-audio/", views.delete_audio, name="delete_audio"),
    
    path("audios/<str:username>/", views.audios, name="audios"),
]
