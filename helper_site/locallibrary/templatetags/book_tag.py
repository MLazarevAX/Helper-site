from django import template
from locallibrary.models import Genre, Book


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
