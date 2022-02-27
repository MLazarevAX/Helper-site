from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('wanted/', views.WantedBook.as_view(), name='wanted'),
    path('readnow/', views.Readnow, name='readnow'),
    path('books/<int:id>', views.BooksDetail,  name='book-detail'),
]
