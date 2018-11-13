from django.shortcuts import render, get_object_or_404, redirect,reverse
from . import models
import markdown
from comments.forms import CommentForm
from .forms import UserForm, RegisterForm


def index(request):
    post_list = models.Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(models.Post, pk=pk)

    post.increase_views()

    post.body = markdown.markdown(post.body, extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month, day):
    post_list = models.Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    created_time__day=day
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(models.Category,pk=pk)
    post_list = models.Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def login(request):
    # if request.session.get('is_login', None):
    #     return redirect(reverse('blog:index'))

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Uesr.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect(reverse('blog:index'))
                else:
                    message = '密码不正确！'
            except:
                message = '用户名不存在！'
        return render(request, 'blog/login.html', locals())

    login_form = UserForm()
    return render(request, 'blog/login.html', locals())


def register(request):
    # if request.session.get('is_login', None):
    #     return redirect(reverse('blog:index'))
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = "两次密码不同！"
                return render(request, 'blog/register.html', locals())
            else:
                same_name_user = models.Uesr.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已存在！"
                    return render(request, 'blog/register.html', locals())
                same_email_user = models.Uesr.objects.filter(email=email)
                if same_email_user:
                    message = "邮箱已被注册！"
                    return render(request, 'blog/register.html', locals())

                new_user = models.Uesr.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect(reverse('blog:login'))  # 自动跳转到登陆界面
    register_form = RegisterForm()
    return render(request, 'blog/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()  # 删除
    return redirect(reverse('blog:login'))
# Create your views here.
