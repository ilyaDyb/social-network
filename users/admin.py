from django.contrib import admin
from .models import TemporaryUser, Users, UserProfile, Friendship

@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "first_name", "last_name", "email"]
    search_fields = ["id", "username", "first_name", "last_name", "email"]
admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(TemporaryUser)

