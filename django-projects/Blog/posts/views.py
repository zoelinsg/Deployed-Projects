from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Post, Tag, LikePost, BookmarkPost
from .forms import CommentForm, PostForm, TagForm

# 首頁，顯示所有文章
@login_required
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

# 文章詳細資訊
@login_required
def post_detail(request, pk):
    # 獲取指定的文章
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()  # 獲取文章的所有評論
    is_liked = False  # 喜歡狀態
    is_bookmarked = False  # 收藏狀態

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 保存評論但不立即提交到數據庫
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # 提交評論後重定向到文章詳細頁面，避免重複提交
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()  # 初始化評論表單

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
        'is_bookmarked': is_bookmarked,
    })

# 文章搜尋
@login_required
def post_search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

# 文章分類
@login_required
def post_category(request, category):
    posts = Post.objects.filter(category=category)
    return render(request, 'posts/post_list.html', {'posts': posts})

# 我的文章
@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'posts/post_list.html', {'posts': posts})

# 創建文章
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form, 'is_update': False})

# 更新文章
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied("您沒有權限修改這篇文章")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form, 'is_update': True})

# 刪除文章
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied("您沒有權限刪除這篇文章")
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

# 喜歡文章
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = LikePost.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', pk=pk)

# 收藏文章
@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    bookmark, created = BookmarkPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
    return redirect('post_detail', pk=pk)

# 我喜歡的文章
@login_required
def my_liked_posts(request):
    liked_posts = Post.objects.filter(likes__user=request.user)
    return render(request, 'posts/my_liked_posts.html', {'posts': liked_posts})

# 我收藏的文章
@login_required
def my_bookmarked_posts(request):
    bookmarked_posts = Post.objects.filter(bookmarks__user=request.user)
    return render(request, 'posts/my_bookmarked_posts.html', {'posts': bookmarked_posts})