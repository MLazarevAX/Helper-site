from django import forms
from contact.models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """Форма заполнения контактной информацией"""
    captcha = ReCaptchaField()
    class Meta:
        model = Contact
        fields =('email', 'captcha')
        widgets = {
            "email": forms.TextInput(attrs={
                "class": "editContent",
                "placeholder": "Your Email..."})
        }
        labels = {
            "email": "",
        }