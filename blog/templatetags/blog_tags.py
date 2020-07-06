from django import template
from django.utils.safestring import mark_safe

from ..models import Post
from django.db.models import Count
import markdown
register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_post.html')
def show_latest_post(count=5):
    latest_post = Post.published.order_by('-publish')[:count]
    return {'latest_post':latest_post}


@register.simple_tag()
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        tm = Count('comments')).order_by('-tm')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))