from unicodedata import name
import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


# Custom template tag que devuelve todos los post activos en el blog
@register.simple_tag
def total_posts():
 return Post.published.count()


#Custom template tag que devuelve un template nuevo y su contexto serán los últimos 5 posts publicados
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


