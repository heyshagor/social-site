from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import PostForm, CommentForm
from .models import Post, Like

def home(request):
    posts = Post.objects.all().order_by('-created_at')

    post_form = PostForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'content' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('home')

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
        'comment_form': comment_form
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
