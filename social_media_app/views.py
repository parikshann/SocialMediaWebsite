# social_media_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, PostForm, UserProfileForm, CommentForm
from .models import Post, UserProfile, Comment
from django.contrib.auth.models import User
from django.urls import reverse


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})
   

def home_view(request):
    if request.user.is_authenticated:
        # If the user is logged in, show the news feed
        posts = Post.objects.all().order_by('-date_posted')
        comments = Comment.objects.filter(post__in=posts).order_by('timestamp')

        return render(request, 'custom_news_feed.html', {'posts': posts, 'comments': comments})
    else:
        # If the user is not logged in, show the home page with a message or login prompt
        return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')


def news_feed_view(request):
    posts = Post.objects.all().order_by('-timestamp')
    if request.user.is_authenticated:
        # If the user is logged in, render the custom_news_feed.html template
        return render(request, 'custom_news_feed.html', {'posts': posts})
    else:
        # If the user is not logged in, render the default news_feed.html template
        return render(request, 'news_feed.html', {'posts': posts})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})



@login_required
def view_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})


@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('view_profile')  # Redirect back to the profile page after saving changes
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'profile_form': profile_form})

def view_other_profile(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    user_profile = UserProfile.objects.get(user=other_user)
    posts = Post.objects.filter(author=other_user).order_by('-date_posted')
    return render(request, 'view_other_profile.html', {'user_profile': user_profile, 'posts': posts})


@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('view_post', pk=post_id)  
    else:
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('timestamp')
    return render(request, 'create_comment.html', {'form': form})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('view_post', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        
        return HttpResponseForbidden("You do not have permission to delete this comment.")

    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect(reverse('view_post', args=[post_id]))
    return render(request, 'delete_comment.html', {'comment': comment})
@login_required
def view_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('timestamp')
    print (comments)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        return redirect('view_post', pk=post.pk) 

    else:
        form = CommentForm()

    return render(request, 'view_post.html', {'post': post, 'comments': comments, 'form': form})
