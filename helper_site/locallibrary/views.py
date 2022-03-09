from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from services.additional import get_context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    '''
    функция отображения для домашней страницы сайта
    '''
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    books = list(Book.objects.all().select_related('genre'))
    category_name = Genre.objects.all()
    return render(request,
                  'locallibrary/index.html',
                  context={
                      'books': books,
                      'category_names': category_name,
                      'num_visits': num_visits,
                  })

class WantedBook(ListView):
    model = Wanted

class ReadnowBook(ListView):
    model = Readnow

class BooksDetail(LoginRequiredMixin, DetailView):
    model = Book
    category_name = Genre.objects.all()

    def get_context_data(self, **kwargs):
        return get_context(self, BooksDetail, 'category_names', self.category_name, **kwargs)

    def get_queryset(self):
        inst = Book.objects.filter(slug=self.kwargs['slug'])
        return inst

class Books(ListView):
    model = Book
    category_name = Genre.objects.all()
    paginate_by = 2

    def get_context_data(self, **kwargs):
        return get_context(self, Books, 'category_names', self.category_name, **kwargs)


class BooksByReadersListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Book
    template_name ='locallibrary/readersbook_list.html'
    paginate_by = 10
    category_name = Genre.objects.all()

    def get_context_data(self, **kwargs):
        return get_context(self, BooksByReadersListView,
                           'category_names', self.category_name, **kwargs)

    def get_queryset(self):
        return Book.objects.filter(reader=self.request.user).order_by('title')