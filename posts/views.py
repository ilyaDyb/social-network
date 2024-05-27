from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .models import Post

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
        html = render_to_string("posts/more_posts.html", context={"posts": current_page, "user": user})
        return JsonResponse({"html": html}, safe=False)

    return render(request, "posts/feed.html", context=context)