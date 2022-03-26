from django.contrib import admin
from .models import Book, Genre, Author, BookWanted, BookReadnow
# Register your models here.
from mptt.admin import MPTTModelAdmin
# from myproject.myapp.models import Node


admin.site.register(Genre, MPTTModelAdmin)
admin.site.register(Author)
admin.site.register(BookWanted)
admin.site.register(BookReadnow)

class WantedInline(admin.TabularInline):
    model = BookWanted
    extra = 0

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'slug']
    inlines = [WantedInline]
