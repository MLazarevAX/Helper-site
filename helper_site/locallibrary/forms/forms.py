from django import forms
from locallibrary.models import Book, Author, Reviews, RatingStar, Rating
from django.core.exceptions import ValidationError
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class ReviewForm(forms.ModelForm):
    ''' Форма отзыва'''
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', 'captcha')
        widgets ={
            'name': forms.TextInput(attrs={"class": "form-control border"}),
            'email': forms.EmailInput(attrs={"class": "form-control border"}),
            'text': forms.Textarea(attrs={"class": "form-control border"}),
        }

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
