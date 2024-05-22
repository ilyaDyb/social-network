from django.contrib import admin

from messanger.models import Chat, Message
from users.models import UserActivity

# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(UserActivity)