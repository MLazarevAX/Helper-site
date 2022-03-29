from django.apps import AppConfig


class LocallibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locallibrary'

class BooksConfig(AppConfig):
    name = 'locallibrary'
    verbose_name = "Книги"
