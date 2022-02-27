from django.contrib import admin
from .models import Book, Genre, Autor, Wanted, Readnow
# Register your models here.
from mptt.admin import MPTTModelAdmin
# from myproject.myapp.models import Node


admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(Autor)
admin.site.register(Wanted)
admin.site.register(Readnow)

class WantedInline(admin.TabularInline):
    model = Wanted
    extra = 0

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_filter = ['title', 'description', "autor", 'genre', 'url', "country"]
    inlines = [WantedInline]
