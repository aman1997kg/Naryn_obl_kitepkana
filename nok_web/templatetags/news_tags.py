from django import template
from classytags.core import Options
from classytags.helpers import AsTag
from classytags.arguments import Argument
from django.db.models import Count

from nok_web.models import *

register = template.Library()


@register.simple_tag()
def all_news_tags():
    return Tags_News.objects.all()


@register.simple_tag()
def all_news_cat():
    return News_cat.objects.all()


@register.simple_tag()
def popular_news():
    return News.objects.order_by('-count_views')


class Lastnews(AsTag):
    name = 'last_news'

    options = Options(
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def render_tag(self, context, varname, name=name):
        last_news = News.objects.all()[:3]
        if varname:
            context[varname] = last_news
            return ''
        else:
            context[name] = last_news
            return ''

register.tag(Lastnews)
