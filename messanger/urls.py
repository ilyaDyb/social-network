from django.urls import path

from messanger import views


app_name = "messanger"

urlpatterns = [
    path("", views.index, name="index"),
]
