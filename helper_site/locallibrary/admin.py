from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Book, Genre, Author, BookWanted, BookReadnow, Reviews
# Register your models here.
from mptt.admin import DraggableMPTTAdmin

# from myproject.myapp.models import Node

class BookAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Book
        fields = '__all__'


admin.site.register(
    Genre,
    DraggableMPTTAdmin,
    list_display=['id', 'name', 'slug', 'parent'],
    list_display_links=['name'],
)

admin.site.register(Author)
admin.site.register(BookWanted)
admin.site.register(BookReadnow)


class WantedInline(admin.TabularInline):
    model = BookWanted
    extra = 0


class ReviewsInline(admin.StackedInline):
    model = Reviews
    extra = 1


@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_image', 'slug', 'draft']
    inlines = [WantedInline, ReviewsInline]
    readonly_fields = ['get_image', ]
    list_filter = ['title', 'country']
    list_editable = ['draft']
    form = BookAdminForm
    save_on_top = True
    save_as = True
    fieldsets = (
        (None, {
            'fields': (("authors", "genres"),)
        }),
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': (('description', 'country'),)
        }),
        (None, {
            'fields': (("poster", "get_image"),)
        }),
        (None, {
            'fields': (('year', 'reader'),)
        }),
        ("options", {
            'fields': (('url', 'draft'),)
        }),
    )




@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к книге"""
    list_display = ("name", "email", "parent", "book", "id")
    readonly_fields = ("name", "email")
