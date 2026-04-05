from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail,  name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('post/<slug:slug>/delete/',  views.post_delete, name='post_delete'),
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle_like'),
    path('post/<slug:slug>/bookmark/',views.toggle_bookmark,name='toggle_bookmark'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('follow/<str:username>/', views.toggle_follow,  name='toggle_follow'),
]