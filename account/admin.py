from django.contrib import admin
from .models import Profile, Post

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']

@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['author', 'title', 'publish', 'status']    
    search_fields = ['title', 'body']
    list_filter = ['author', 'status']
    raw_id_fields = ['author']