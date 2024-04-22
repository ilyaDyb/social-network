from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import UserLoginForm
from .utils import authenticate_by_email

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():

            username_or_email = form.cleaned_data.get("username_or_email")
            password = form.cleaned_data.get("password")

            if "@" in username_or_email:
                user = authenticate_by_email(username_or_email, password)
            else:
                user = auth.authenticate(request, username=username_or_email, password=password)
            if user is None:
                raise ValidationError("Invalid login or password")
            auth.login(request, user)
            return redirect(reverse("feed:index"))
            
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", context={"form": form})

def registration(request):
    return render(request, "users/registration.html")



@login_required
def logout(request):
    auth.logout(request=request)
    return redirect(reverse("users:login"))