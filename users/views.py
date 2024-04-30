from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Q
from django.db import transaction

from .models import Friendship, UserProfile, Users
from .forms import UserLoginForm, UserRegistrationForm
from .utils import authenticate_by_email

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
                form.add_error(None, "Invalid login or password")
            else:
                auth.login(request, user)
                messages.success(request, "Successful login")
                return redirect(reverse("feed:feed"))
            
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
    user = Users.objects.get(username=username)
    context = {
        "user": user,
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
    # user1 = Users.objects.get(username="test3")
    # user2 = Users.objects.get(username="test2")
    # print(user1.username, user2.username)
    # # Friendship.objects.create(from_user=user1, to_user=user2, status="accepted")
    # friend = Friendship.objects.get(pk=1)
    # print(friend)
    # print(user1.friends.all())
    friends = Users.objects.get(username=username).friends.all()
    find = request.GET.get("find")
    section = request.GET.get("section")
    if find:
        friends = friends.filter(
            Q(username__icontains=find) | Q(first_name__icontains=find) | Q(last_name__icontains=find)
        )
    if section == "requests":
        if request.user.username == username:
            from_user_ids = Friendship.objects.filter(to_user=request.user, status="pending").values_list('from_user', flat=True)
            friends = Users.objects.filter(username__in=from_user_ids)
            print(friends)
            
    print(friends)
    context = {
        "friends": friends,
        "username": username,
    }

    return render(request, "users/friends.html", context=context)


@login_required()
@csrf_exempt
def send_friend_request(request, username):
    if request.method == "POST":
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return JsonResponse({"message": "User does not exist"}, status=404)
        if Friendship.objects.filter(from_user=request.user, to_user=user, status="pending").exists():
            return JsonResponse({"message": "Friend request already sent"}, status=200)
        else:
            with transaction.atomic():
                friendship, created = Friendship.objects.get_or_create(from_user=request.user, to_user=user, status="pending")
                if not created:
                    friendship.status = "accepted"
                    friendship.save()
            return JsonResponse({"message": "Success"})
    return JsonResponse({"message": "Invalid method"}, status=405)