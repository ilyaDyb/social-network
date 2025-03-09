
from django.urls import path

from audios import views


app_name = "audios"
urlpatterns = [
    path("audios/load/", views.LoadAudio.as_view(), name="load_audio"),
    path("audios/add-audio/", views.AddAudio.as_view(), name="add_audio"),
    path("audios/delete-audio/", views.DeleteAudio.as_view(), name="delete_audio"),
    path("preview/<int:instance_id>", views.preview, name="preview"),
    
    path("audios/", views.AudioRedirectView.as_view(), name="audios"),
    path("audios/<str:username>/", views.AudioListView.as_view(), name="audios"),
]
