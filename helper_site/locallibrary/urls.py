from . import views
from django.urls import path, converters, register_converter
from . import converters

register_converter(converters.SlugRus, 'ruslug')

urlpatterns = [
    path('', views.index, name='index'),
    path('wanted/', views.WantedBook.as_view(), name='wanted'),
    path('readnow/', views.ReadnowBook.as_view(), name='readnow'),
    path('books/<ruslug:slug>', views.BooksDetail.as_view(),  name='book-detail'),
]
