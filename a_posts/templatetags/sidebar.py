from django.template import Library
from ..models import Tag, Post, Comment
from django.db.models import Count

register=Library()

@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None, user=None):
    categories= Tag.objects.all()
    top_post= Post.objects.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')[:3]
    top_comment= Comment.objects.annotate(like_count=Count('likes')).filter(like_count__gt=0).order_by('-like_count')[:3]
    context={
        'categories':categories,
        'tag': tag,
        'top_post':top_post,
        'user':user,
        'top_comment':top_comment,
    }
    return context
