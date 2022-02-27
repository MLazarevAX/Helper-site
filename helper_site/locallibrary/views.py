from django.shortcuts import render
from .models import *
from django.views.generic import ListView


# Create your views here.

def index(requests):
    '''
    функция отображения для домашней страницы сайта
    '''
    num_books = Book.objects.all()
    category_name = Genre.objects.all()
    num_wanted = Wanted.objects.all()
    num_readnow = Readnow.objects.all()

    return render(requests,
                  'locallibrary/index.html',
                  context={
                      'num_books': num_books,
                      'category_names': category_name,
                      'num_wanted': num_wanted,
                      'num_readnow': num_readnow,
                  })


class WantedBook(ListView):
    model = Wanted



class ReadnowBook:
    pass


class BooksDetail:
    pass
