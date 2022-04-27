from modeltranslation.translator import register, TranslationOptions
from .models import Category, Author, Genre, Book


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'middle_name')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Book)
class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')
