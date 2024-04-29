from django.contrib import admin
from .models import Users, UserProfile, Friendship


admin.site.register(Users)
admin.site.register(UserProfile)
admin.site.register(Friendship)

