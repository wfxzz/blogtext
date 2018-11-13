# 存放自定义的模板标签代码。
from django import template
from ..models import Post,Category

register = template.Library()


@register.simple_tag  # 最新文章模板标签
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag  # 归档模板标签
def archives():      # 返回一个列表，精确到月 降序按月归档
    return Post.objects.dates('created_time', 'day', order='DESC')


@register.simple_tag
def get_categories():  # 分类模板标签
    return Category.objects.all()