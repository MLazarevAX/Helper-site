from . import views
from django.urls import path, register_converter
from . import converters

register_converter(converters.SlugRus, 'ruslug')

urlpatterns = [
    path('wanted/', views.WantedBook.as_view(), name='wanted'),
    path('readnow/', views.ReadnowBook.as_view(), name='readnow'),

]

urlpatterns += [
    path(r'mybooks/', views.BooksByReadersListView.as_view(), name='my-books'),
    path('books/', views.Books.as_view(), name='books-list'),
    path('book/<ruslug:slug>', views.BooksDetail.as_view(), name='book-detail'),
    path('book/<ruslug:slug>/new/', views.new_book, name='new-book'),
]