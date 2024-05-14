from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from posts.models import Post


@login_required
def feed(request):
    users = request.user.accepted_friends
    posts = Post.objects.filter(user__in=users).order_by("-id")
    context = {
        "posts": posts,
    }
    return render(request, "posts/feed.html", context=context)