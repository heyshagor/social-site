from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm
from .models import Post, Like
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()

    # Prepare a list of post IDs the current user has liked
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    if request.method == 'POST':
        # New post
        if 'content' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')

        # New comment
        elif 'text' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post_id = request.POST.get('post_id')
                comment.save()
                return redirect('home')

    return render(request, 'core/home.html', {
        'posts': posts,
        'form': post_form,
        'comment_form': comment_form,
        'liked_post_ids': liked_post_ids,  # Pass to template
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})

def like_post(request, post_id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=post_id)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post
        )

        if not created:
            like.delete()  # unlike

    return redirect('home')


def profile(request, username):
    user_obj = User.objects.get(username=username)
    posts = user_obj.post_set.all().order_by('-created_at')
    post_count = posts.count()
    
    return render(request, 'core/profile.html', {
        'profile_user': user_obj,
        'posts': posts,
        'post_count': post_count
    })


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'core/edit_post.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('home')