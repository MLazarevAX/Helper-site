from django.contrib import admin
from .models import Book, Genre, Author, Wanted, Readnow
# Register your models here.
from mptt.admin import MPTTModelAdmin
# from myproject.myapp.models import Node


admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(Author)
admin.site.register(Wanted)
admin.site.register(Readnow)

class WantedInline(admin.TabularInline):
    model = Wanted
    extra = 0

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_filter = ['title', 'description', 'author', 'genre', 'url', "country", ]
    inlines = [WantedInline]

    list_display = ['title', 'description', 'genre', 'slug']

