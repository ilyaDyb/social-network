from django.urls import path

from feed import views

app_name = "feed"

urlpatterns = [
    path("", views.index, name="index"),
]
