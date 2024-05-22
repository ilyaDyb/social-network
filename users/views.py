import json
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q

from posts.models import Post

from .models import Friendship, UserActivity, UserProfile, Users
from .forms import UserLoginForm, UserRegistrationForm
from .utils import authenticate_by_email
from .validators import validate_create_post

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():

            username_or_email = form.cleaned_data.get("username_or_email")
            password = form.cleaned_data.get("password")

            if "@" in username_or_email:
                user = authenticate_by_email(username_or_email, password)
            # elif "+7" in username_or_email_or_phone_number: #в будущем

            else:
                user = auth.authenticate(request, username=username_or_email, password=password)
            if user is None:
                form.add_error(None, "Invalid login or password") #need fix
            else:
                auth.login(request, user)
                messages.success(request, "Successful login")
                return redirect(reverse("posts:feed"))
            
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", context={"form": form})

def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = Users.objects.get(username=form.cleaned_data["username"])
            UserProfile.objects.create(user=user)
            messages.success(request, "Account created successfully")
            return redirect(reverse("users:login"))
    else:
        form = UserRegistrationForm()
    if request.user.is_authenticated:
        return HttpResponse(status=404)
    return render(request, "users/registration.html", context={"form": form})



@login_required
def logout(request):
    auth.logout(request=request)
    messages.success(request, "Successful logout")
    return redirect(reverse("users:login"))

@login_required
def profile(request, username):
    if request.method == "POST":
        text = request.POST.get("text_content")
        image = request.FILES.get("file_content")
        validate_result = validate_create_post(text=text, image=image)

        if validate_result["status"]:
            Post.objects.create(user=request.user, text=text, image=image)
            messages.success(request, str(validate_result["text"]))
            return redirect(reverse("users:profile", kwargs={"username": username}))
        if not validate_result["status"]:
            messages.warning(request, str(validate_result["text"]))
            return redirect(reverse("users:profile", kwargs={"username": username}))
    else:
        user = Users.objects.get(username=username)
        friends = user.accepted_friends
        photos = user.photos.all().order_by("-id")[0:3]
        posts = Post.objects.filter(user=user).order_by("-id")
        activity = user.activity
        context = {
            "user": user,
            "friends": friends,
            "photos": photos,
            "posts": posts,
            "activity": activity,
        }
        return render(request, "users/profile.html", context=context)


@login_required
@csrf_exempt
def edit_profile_img(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if image.size > 1048576:
            response = {"message": "Your file is too big"}
            return JsonResponse(response)
        user = Users.objects.get(id=request.user.id)
        if user.avatar:
            user.avatar.delete()
        user.avatar = image
        user.save()
        response = {
            "message": "You change avatar successful"
        }
        return JsonResponse(response)
    else:
        return HttpResponse(status=404)
    
@login_required
@csrf_exempt
def edit_short_inf(request):
    if request.method == "POST":
        text = request.POST.get("text")
        if not len(text) >= 257:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.small_info = text
                user_profile.save()
                return JsonResponse({"message": "Success"})
            except Exception as ex:
                print(ex)
                return JsonResponse({"message": "Error"})
        else:
            return JsonResponse({"message": "Your text is too big"})
    else:
        return HttpResponse(status=404)
    
@login_required
def friends(request, username):
    flag = None
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return render(request, "users/friends.html", context={"message": "User does not exist"})
    friends = user.accepted_friends
    find = request.GET.get("find")
    find_all = request.GET.get("find_all")
    section = request.GET.get("section")

    if find:
        friends = friends.filter(
            Q(username__icontains=find) | Q(first_name__icontains=find) | Q(last_name__icontains=find)
        )

    elif section == "requests":
        if request.user.username:
            friend_requests = Friendship.objects.filter(to_user=request.user, status="pending")
            friend_user_ids = friend_requests.values_list('from_user_id', flat=True)
            friends = Users.objects.filter(id__in=friend_user_ids)
            flag = True

    elif find_all:
        friends = Users.objects.filter(
            Q(username__icontains=find_all) | Q(first_name__icontains=find_all) | Q(last_name__icontains=find_all)
        )

    context = {
        "friends": friends,
        "username": username,
        "flag": flag,
    }
    return render(request, "users/friends.html", context=context)


@login_required
@csrf_exempt
def send_friend_request(request, username):
    if request.method == "POST":
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        if not Friendship.objects.filter(from_user=request.user, to_user=user, status="pending").exists():
            Friendship.objects.create(from_user=request.user, to_user=user, status="pending")
            return JsonResponse({"message": "Friend request sent"})
        else:
            return JsonResponse({"message": "Friend request already sent"}, status=400)
    return JsonResponse({"message": "Invalid method"}, status=405)


@login_required
@csrf_exempt
def accept_friend_request(request, username):
    if request.method == "POST":
        try:
            to_user = request.user
            from_user = Users.objects.get(username=username)

            friendship = Friendship.objects.get(from_user=from_user, to_user=to_user)
        except Friendship.DoesNotExist:
            return JsonResponse({"message": "Friendship request does not exist"}, status=404)
        if friendship.status == "pending":
            friendship.status = "accepted"
            friendship.save()
            return JsonResponse({"message": "Friend request accepted"})
        else:
            return JsonResponse({"message": "Friend request is not pending"}, status=400)
    return JsonResponse({"message": "Invalid method"}, status=405)


@csrf_exempt
def delete_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
        except Post.DoesNotExist:
            return JsonResponse({"message": "Does not exists"}, status=400)
        return JsonResponse({"message": "Success"}, status=200)
    else:
        return JsonResponse({"message": "Bad request"}, status=405)
    

@csrf_exempt
@login_required
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        status = data["status"]
        now = timezone.now()

        defaults = {"last_activity": now}

        if status == "offline":
            defaults["is_online"] = False
        elif status == "online":
            defaults["is_online"] = True
        else:
            return JsonResponse({"status": "Fatal error"})
        
        UserActivity.objects.update_or_create(user=request.user, defaults=defaults)

        return JsonResponse({"status": "Success"}, status=200)
    else:
        return JsonResponse({"status": "Fail"}, status=405)