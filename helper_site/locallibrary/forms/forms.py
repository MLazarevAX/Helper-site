from django import forms
from locallibrary.models import Book, Author, Reviews, RatingStar, Rating
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


class RatingForm(forms.ModelForm):
    ''' Форма добавления рейтинга '''
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
