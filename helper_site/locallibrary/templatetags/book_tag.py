from django import template
from locallibrary.models import Genre, Book
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()


@register.simple_tag()
def get_genre():
    """Вывод всех категорий"""
    return Genre.objects.all()


@register.inclusion_tag('locallibrary/tags/last_book.html')
def get_last_books(count=5):
    """Вывод последних книг"""
    books = Book.objects.order_by("id")[:count]
    return {"last_book": books}


@register.filter(needs_autoscape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<strong> %s </strong> %s' % (esc(first), esc(other))
    return mark_safe(result)
