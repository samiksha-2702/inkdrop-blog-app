from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from .models import Post, Category, Tag, Comment, Follow, UserProfile
from .forms import PostForm, CommentForm
from .forms import UserUpdateForm, UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    posts = Post.objects.filter(status='published')
    categories = Category.objects.annotate(post_count=Count('posts'))[:8]
    tags = Tag.objects.annotate(post_count=Count('posts'))[:20]

    category_slug = request.GET.get('category')
    tag_slug  = request.GET.get('tag')
    query = request.GET.get('q', '')

    if category_slug:
        posts = posts.filter(categories__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/home.html',
        {'posts':posts,'categories':categories,'tags':tags,'query':query})


from django.contrib.auth.decorators import login_required
from .models import Comment

def post_detail(request, slug):
    post     = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(parent=None, is_approved=True).prefetch_related('replies')
    form     = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = post
            comment.author = request.user
            parent_id      = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            return redirect(post.get_absolute_url())

    is_liked      = request.user.is_authenticated and post.likes.filter(pk=request.user.pk).exists()
    is_bookmarked = request.user.is_authenticated and post.bookmarks.filter(pk=request.user.pk).exists()
    return render(request, 'blog/post_detail.html',
        {'post':post,'comments':comments,'form':form,
         'is_liked':is_liked,'is_bookmarked':is_bookmarked})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()   # save ManyToMany (categories/tags)
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form':form,'action':'Create'})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect(post.get_absolute_url())
    return render(request, 'blog/post_form.html', {'form':form,'action':'Edit'})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post':post})

from django.http import JsonResponse
from .models import Follow, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user);  liked = False
    else:
        post.likes.add(request.user);     liked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.likes.count()})
    return redirect(post.get_absolute_url())

@login_required
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
    return redirect('profile', username=username)


from django.contrib.auth import login
from .forms import UserRegisterForm, UserProfileForm, UserUpdateForm

def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/register.html', {'form':form})

def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_following = (
        request.user.is_authenticated and
        Follow.objects.filter(follower=request.user, following=user).exists()
    )
    return render(request, 'blog/profile.html', {
        'profile_user': user,
        'posts': user.posts.filter(status='published'),
        'is_following': is_following,
        'follower_count': user.followers.count(),
        'following_count': user.following.count(),
    })

@login_required
def dashboard(request):
    posts = request.user.posts.all()
    return render(request, 'blog/dashboard.html', {'posts': posts})


@login_required
def toggle_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)

    return redirect('post_detail', slug=slug)

@login_required
def profile_edit(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)  # ← fix this line

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', username=user.username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = UserProfileForm(instance=profile)

    return render(request, 'blog/profile_edit.html', {
        'u_form': u_form,
        'p_form': p_form
    })