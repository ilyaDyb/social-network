from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('profile/edit-img/', views.edit_profile_img, name='edit_profile_img'),
    path('profile/<str:username>/', views.profile, name='profile'),
]