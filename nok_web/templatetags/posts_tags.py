from classytags.core import Options
from classytags.helpers import AsTag
from classytags.arguments import Argument
from django import template
from django.db.models import Count

from nok_web.models import *

register = template.Library()


@register.simple_tag()
def posts_tags():
    return Tags_Posts.objects.all()


@register.simple_tag()
def all_posts_cat():
    return Post_cat.objects.all()



@register.simple_tag()
def popular_posts():
    return Post.objects.order_by('-count_views')



class LastPosts(AsTag):
    name = 'last_posts'

    options = Options(
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def render_tag(self, context, varname, name=name):
        last_posts = Post.objects.all()[:3]
        if varname:
            context[varname] = last_posts
            return ''
        else:
            context[name] = last_posts
            return ''

register.tag(LastPosts)