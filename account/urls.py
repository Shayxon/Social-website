from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('blog_posts/', views.blog_posts, name='blog_posts'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/', views.like, name='like'),
    path('comment_like/<int:comment_id>/<int:post_id>/', views.comment_like, name='comment_like'),
    path('comment_delete/<int:comment_id>/<int:post_id>/', views.delete_comment, name='delete_comment'),
]