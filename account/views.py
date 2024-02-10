from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserEditForm, ProfileEditForm, PostEditForm
from .models import Profile, Post

@login_required
def dashboard(request):
    posts = Post.objects.filter(author = request.user.id)
    return render(request, 'account/dashboard.html', {'posts':posts})

@login_required
def blog_posts(request):
    posts = Post.published.all()
    return render(request, 'account/blog-posts.html', {'posts':posts})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostEditForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('edit_post', post_id)
    else:
        form = PostEditForm(instance=post)    
    return render(request, 'account/edit-post.html', {'form':form, 'post_id':post_id})

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form':form})