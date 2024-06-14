from django.contrib import admin

from audios.models import UserAudio
from photos.models import Photo
from posts.models import Post
from .models import TemporaryUser, Users, UserProfile, Friendship, UserActivity

class UserActivityTab(admin.TabularInline):
    model = UserActivity
    fields = "last_activity", "is_online"
    search_fields = ("is_online",)

class UserProfileTab(admin.TabularInline):
    model = UserProfile
    fields = ("small_info", )

class UserPostsTab(admin.TabularInline):
    model = Post
    fields = "text", "image", "created_at"
    readonly_fields = ("created_at", )


class UserPhotosTab(admin.TabularInline):
    model = Photo
    fields = "photo", "created_at"
    readonly_fields = ("created_at",)

class UserAudiosTab(admin.TabularInline):
    model = UserAudio
    fields = "audio_title", "audio_author"
    readonly_fields = "audio_title", "audio_author"

    def audio_title(self, instance):
        return instance.audio.title
    audio_title.short_description = "title"
    
    def audio_author(self, instance):
        return instance.audio.author
    audio_author.short_description = "author"


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display =  ["id", "username", "first_name", "last_name", "email", "date_joined"]
    search_fields = ["id", "username", "first_name", "last_name", "email", "date_joined"]
    inlines = [
        UserActivityTab, UserProfileTab, UserPostsTab, UserPhotosTab, UserAudiosTab
    ]
    show_full_result_count = True
admin.site.register(UserProfile)
admin.site.register(Friendship)
admin.site.register(TemporaryUser)

