# social_media_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from .models import Post, UserProfile, Comment

class RegistrationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']