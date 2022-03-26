from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, DetailView, View
from services.additional import get_context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms.forms import NewBookForm, NewAuthorForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin




class WantedBook(ListView):
    model = BookWanted


class ReadnowBook(ListView):
    model = BookReadnow


class BooksDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'locallibrary/books/book_detail.html'

    def get_queryset(self):
        a = Book.objects.filter(draft=False)
        return Book.objects.filter(draft=False)


class Books(ListView):
    model = Book
    template_name = 'locallibrary/books/book_list.html'



class BooksByReadersListView(LoginRequiredMixin, ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = Book
    template_name = 'locallibrary/readersbook_list.html'
    paginate_by = 10
    category_name = Genre.objects.all()

    def get_context_data(self, **kwargs):
        return get_context(self, BooksByReadersListView,
                           'category_names', self.category_name, **kwargs)

    def get_queryset(self):
        read = Book.objects.filter(reader=self.request.user)
        return read


@login_required
def new_book(request, slug):
    book_inst = get_object_or_404(Book, slug=slug)

    if request.method == 'POST':
        form = NewBookForm(request.POST)

        if form.is_valid():
            book_inst.title = form.cleaned_data['new_title']
            book_inst.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = NewBookForm()

    return render(request, 'locallibrary/new_book.html', {'form': form, 'bookinst': book_inst})

