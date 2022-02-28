from django.urls.converters import SlugConverter

class SlugRus(SlugConverter):
    regex = '[-a-zA-Zа-яёА-ЯЁ0-9_]+'


