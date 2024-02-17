from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import RegisterForm, UserEditForm, ProfileEditForm, PostEditForm, PostCreateForm, CommentForm, SearchForm
from .models import Profile, Post, Comment
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

@login_required
def dashboard(request):
    posts = Post.objects.filter(author = request.user.id)
    return render(request, 'account/dashboard.html', {'posts':posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    tags = post.tags.values_list('id', flat=True)
    comments = post.comments.all()
    similar_posts = Post.published.filter(tags__in=tags).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:4]
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.save()
            post.comments.add(new_comment)
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()    
    return render(request, 'account/post-detail.html', {'post':post, 'form':form, 'comments':comments, 'similar_posts':similar_posts})

@login_required
def blog_posts(request, post_tag=None):
    form = SearchForm()
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            posts = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
    elif post_tag:
        tag = get_object_or_404(Tag, slug=post_tag)
        posts = Post.published.filter(tags__in=[tag])
    else:     
        posts = Post.published.all()
    return render(request, 'account/blog-posts.html', {'posts':posts, "post_tag":post_tag, 'query':query, 'form':form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = PostEditForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('edit_post', post_id)
    else:
        form = PostEditForm(instance=post)    
    return render(request, 'account/edit-post.html', {'form':form, 'post_id':post_id, 'comments':comments})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('dashboard')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = PostCreateForm()    
    return render(request, 'account/create-post.html', {'form':form})

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

@login_required
@require_POST
def like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

        if action == 'like':
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'error'})

@login_required
@require_POST
def comment_like(request, comment_id, post_id):
    user = request.user
    comment = get_object_or_404(Comment, id=comment_id)
    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)
    return redirect('post_detail', post_id=post_id)        


@login_required
@require_POST
def delete_comment(request, comment_id, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = get_object_or_404(Comment, id=comment_id)
    post.comments.remove(comment)
    return redirect('edit_post', post_id)  


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