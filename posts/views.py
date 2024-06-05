from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import Comment, Post

@csrf_exempt
@login_required
def feed(request):
    users = request.user.accepted_friends
    posts = Post.objects.filter(user__in=users).order_by("-id")
    page = request.GET.get("page")
    paginator = Paginator(posts, 4)
    current_page = paginator.get_page(page)


    try:
        next_page = current_page.next_page_number()
    except Exception:
        return render(request, "posts/feed.html", context={"next_page": None})
    
    context = {
        "posts": current_page,
        "next_page": next_page,
    }
    
    if request.method == "POST":
        user = request.user
        html = render_to_string("includes/posts.html", context={"posts": current_page, "user": user})
        return JsonResponse({"html": html}, safe=False)

    return render(request, "posts/feed.html", context=context)


@csrf_exempt
def like_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if not user in post.likes.all():
            post.likes.add(user)
            return JsonResponse({"status": "liked"})
        else:
            post.likes.remove(user)
            return JsonResponse({"status": "unliked"})
    else:
        return HttpResponse(status=404)
    

@csrf_exempt
def write_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment_text = request.POST.get("comment_text")
        comment = Comment.objects.create(
            post_id=post_id, user=request.user, text=comment_text
            )
        comment_html = render_to_string("includes/comments.html", context={"comment": comment})
        return JsonResponse({"html": comment_html}, status=200, safe=False)
    else:
        return JsonResponse({}, status=400)
    

@csrf_exempt
def show_comments(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comments = Comment.objects.filter(post_id=post_id)
        if comments:
            comments_html = render_to_string("includes/comments.html", context={"comments": comments})
            return JsonResponse({"html": comments_html}, safe=False)
        else:
            return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)