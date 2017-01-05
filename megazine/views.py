from django.shortcuts import render, get_object_or_404, redirect
from megazine.models import Post, Comment
from megazine.forms import PostForm, CommentForm, SignupForm
from django.core.paginator import InvalidPage, Paginator
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


def index(request):
    page_number = int(request.GET.get('page', 1))
    if request.GET.get('tags'):
        tag = request.GET.get('tags')
        post_list = Post.objects.filter(tags__name__startswith=tag)
    else:
        post_list = Post.objects.all()
    paginate_by = 12

    paginator = Paginator(post_list, paginate_by)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404('invalid page {}'.format(page_number))
    return render(request, "megazine/index.html", {
        'post_list': page.object_list,
        'page': page,
    })


def index_old(request):
    post_list = Post.objects.all()
    return render(request, 'megazine/index_old.html', {'post_list':
                  post_list, })


def detail(request, pk):
    if request.is_ajax():
        return HttpResponse({'jquery': 'ok'})
    else:
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(auto_id=False)
        return render(request,
                      "megazine/detail.html",
                      {'post': post, 'comment_form': comment_form, })


@staff_member_required
def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "새 글이 등록되었습니다")
            return redirect('megazine:index')
    else:
        form = PostForm()
    return render(request, 'megazine/form.html', {
        'form': form, 'title': 'New Post'})


@staff_member_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "글 수정에 성공하였습니다")
            return redirect('megazine:index')
    else:
        form = PostForm(instance=post)
    return render(request, 'megazine/form.html', {
        'form': form, 'title': 'Edit Post'})


@staff_member_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "글이 삭제되었습니다")
        return redirect('megazine:index')
    return render(request, 'megazine/post_delete_confirm.html', {'post': post})


def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.is_ajax():
                comment = form.save(commit=False)
                comment.post = post
                if request.user.is_authenticated():
                    comment.author = request.user
                else:
                    comment.author = User.objects.get(username='veil')
                comment.save()
                return render(request, 'megazine/comment_row.html', {
                    'comment': comment,
                })
    return redirect('megazine:detail', pk)


@login_required
def comment_edit(request, pk_comment):
    comment = get_object_or_404(Comment, pk=pk_comment)
    if request.user.id == comment.author_id:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                    form.save()
                    messages.success(request, '댓글을 수정했습니다.')
                    return redirect('megazine:detail', comment.post.pk,)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'form.html', {
            'form': form,
            'post': comment.post,
            'title': 'Edit comment'
        })
    else:
        messages.warning(request, '댓글수정은 작성자만 가능합니다')
        return redirect('megazine:detail', comment.post_id)


@login_required
def comment_delete(request, pk_comment):
    comment = get_object_or_404(Comment, pk=pk_comment)
    if request.user.id == comment.author_id:
        if request.method == 'POST':
            comment.delete()
            return HttpResponse({'jquery': 'ok'})  # ?? TODO
        else:
            return redirect('megazine:index')
    else:
        messages.warning(request, '댓글수정은 작성자만 가능합니다')
        return redirect('megazine:detail', comment.post_id)


def signup_old(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            print('가입 승인')
            print('form.cleaned_data = {}'.format(form.cleaned_data))
            messages.success(request, '회원가입 신청 완료')
            return redirect('megazine:index')
        else:
            print("가입 거절")
    else:
        form = SignupForm()
    return render(request, "form.html", {'form': form, })


def test(request):
    messages.debug(request, 'hello debug')
    messages.info(request, 'hello info')
    messages.success(request, 'hello success')
    messages.warning(request, 'hello waring')
    messages.error(request, 'hello error')
    return render(request, "megazine/test.html", {})
