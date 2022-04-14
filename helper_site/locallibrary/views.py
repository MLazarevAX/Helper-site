from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import *
from django.views.generic import ListView, DetailView, View
from services.additional import get_context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms.forms import NewBookForm, ReviewForm


# Create your views here.

class WantedBook(ListView):
    model = BookWanted


class ReadnowBook(ListView):
    model = BookReadnow


class BooksDetail(DetailView):
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


class AddReview(View):
    ''' Отзывы пользователей '''

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.book_id = pk
            form.save()

        print(request.POST)
        return redirect(book.get_absolute_url())


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
