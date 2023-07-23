# social_media_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('news-feed/', views.news_feed_view, name='news_feed'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.view_other_profile, name='view_other_profile'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('create_comment/<int:post_id>/', views.create_comment, name='create_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:pk>/', views.view_post, name='view_post'),  


]

