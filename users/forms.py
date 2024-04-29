from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

import re

from .models import Users

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = Users
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = Users.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError("A user with such email already exists")
        return email
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        special_characters = r'[!@#$%^&*()_+\[\]{};\'\\:"|]'
        pattern = re.compile(special_characters)
        if pattern.search(first_name):
            raise forms.ValidationError("Firstname must be without special characters")
        if len(first_name) <= 3:
            raise forms.ValidationError("Your firstname too small")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        special_characters = r'[!@#$%^&*()_+\[\]{};\'\\:"|]'
        pattern = re.compile(special_characters)
        if pattern.search(last_name):
            raise forms.ValidationError("Lastname must be without special characters")
        if len(last_name) <= 3:
            raise forms.ValidationError("Your lastname too small")
        return last_name

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        model = Users
        fields = ['username_or_email', 'password']

