from django.contrib import admin

from posts.models import Comment, Post

admin.site.register(Post)
admin.site.register(Comment)