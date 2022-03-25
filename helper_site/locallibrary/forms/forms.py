from django import forms
from locallibrary.models import Book, Author
from django.core.exceptions import ValidationError



class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class NewAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'