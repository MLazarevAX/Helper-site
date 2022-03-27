from django import forms
from locallibrary.models import Book, Author, Reviews
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    ''' Форма отзыва'''
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'