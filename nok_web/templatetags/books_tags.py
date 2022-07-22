from django import template
from classytags.core import Options
from classytags.helpers import AsTag
from classytags.arguments import Argument
from django.db.models import Count

from nok_web.models import *

register = template.Library()

@register.simple_tag(name='all_books_cats')
def get_all_book_cat():
    return Book_category.objects.all()

@register.simple_tag()
def all_book_cat_count():
    return Book_category.objects.all().count()


@register.simple_tag()
def all_books():
    return Books.objects.all()[:3]

@register.simple_tag()
def popular_books():
    return Books.objects.order_by('-books_view')[:6]

@register.simple_tag()
def genre_books():
    return Genre.objects.all()

@register.simple_tag()
def tags_books():
    return Tags_Books.objects.all()


class LastBooks(AsTag):
    name = 'last_books'

    options = Options(
        'as',
        Argument('varname', required=False, resolve=False)
    )

    def render_tag(self, context, varname, name=name):
        last_books = Books.objects.all()[:5]
        if varname:
            context[varname] = last_books
            return ''
        else:
            context[name] = last_books
            return ''

register.tag(LastBooks)








