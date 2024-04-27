from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from users.models import Users

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
            messages.success(request, "Account created successfully")
            return redirect(reverse("feed:feed"))
    else:
        form = UserRegistrationForm()
    return render(request, "users/registration.html", context={"form": form})



@login_required
def logout(request):
    auth.logout(request=request)
    messages.success(request, "Successful logout")
    return redirect(reverse("users:login"))


def profile(request, username):
    user = Users.objects.get(username=username)
    context = {
        "user": user,
    }
    return render(request, "users/profile.html", context=context)