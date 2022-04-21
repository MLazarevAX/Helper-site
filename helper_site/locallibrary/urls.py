from . import views
from django.urls import path, register_converter
from . import converters

register_converter(converters.SlugRus, 'ruslug')

urlpatterns = [
    path('', views.Books.as_view(), name='books-list'),
    path(r'mybooks/', views.BooksByReadersListView.as_view(), name='my-books'),
    path("filter/", views.FilterBooksView.as_view(), name='filter'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add-review'),
    path('book/<ruslug:slug>', views.BooksDetail.as_view(), name='book-detail'),
    path('book/<ruslug:slug>/new/', views.new_book, name='new-book'),
]

urlpatterns += [
    path('wanted/', views.WantedBook.as_view(), name='wanted'),
    path('readnow/', views.ReadnowBook.as_view(), name='readnow'),

]
