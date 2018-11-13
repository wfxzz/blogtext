from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):   # 分类
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):       # 标签
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文，我们使用了 TextField。
    body = models.TextField()

    views = models.PositiveIntegerField(default=0)

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField(default=timezone.now)
    modified_time = models.DateTimeField(default=timezone.now)

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 关联
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):     # 得到自己的id
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Uesr(models.Model):
    """用户表"""

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)  # unique唯一，不能重复
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:                  # 定义用户按创建时间的反序排列，也就是最近的最先显示；
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
# Create your models here.
