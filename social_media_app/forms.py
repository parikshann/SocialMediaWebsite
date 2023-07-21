# social_media_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

class RegistrationForm(UserCreationForm):
    # Customize fields if needed
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    # Customize fields if needed
    class Meta:
        model = User
        fields = ('username', 'password')
