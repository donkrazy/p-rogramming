from django.shortcuts import get_object_or_404, render, redirect
from blog.models import Post
from blog.forms import PostForm, CommentForm, JokeSignupForm
from django.contrib import messages


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', {'post_list': post_list, })


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {'post': post,
         })


def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "새 댓글이 등록되었습니다.")
            return redirect('blog:detail', pk)
    else:
        form = CommentForm()
    return render(request, 'blog/form.html', {'form': form,})



def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "새 글이 등록되었습니다.")
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {'form': form,})


def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:index')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/form.html', {'form': form, })

def signup_joke(request):
    if request.method == 'POST':
        form = JokeSignupForm(request.POST)
        if form.is_valid():
            print('form.cleaned_data = {}'.format(form.cleaned_data))
            return redirect('blog.views.index')
    else:
        form = JokeSignupForm()
    return render(request, "blog/form.html", {
        'form': form,
    })
