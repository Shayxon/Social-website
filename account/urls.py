from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('blog_posts/', views.blog_posts, name='blog_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
]