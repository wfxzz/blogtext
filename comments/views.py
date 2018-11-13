from django.shortcuts import render, get_object_or_404, redirect, reverse
from blog.models import Post, Uesr

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    if not request.session.get('is_login', None):
        return redirect(reverse('blog:login'))
    post = get_object_or_404(Post, pk=post_pk)  # 文章
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment1 = form.save(commit=False)  # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment1.post = post
            comment1.save()
            return redirect(post)
        else:
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return redirect(request, 'blog/detail.html', context=context)
    return redirect(post)
# Create your views here.
