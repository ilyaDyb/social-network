from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

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

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        model = Users
        fields = ['username_or_email', 'password']

