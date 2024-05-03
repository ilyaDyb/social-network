from django.urls import path

from photos import views

app_name = "photos"

urlpatterns = [
    path("photos/load-photo/", views.load_photo, name="load_photo"),
    path("photos/delete/", views.delete_photo, name="delete_photo"),
    path("photos/<str:username>/", views.photos, name="photos"),

]
