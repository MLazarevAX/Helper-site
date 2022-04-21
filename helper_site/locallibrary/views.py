from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, View
from services.additional import get_context
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms.forms import NewBookForm, ReviewForm, RatingForm


class GenreYear:
    '''Жанры и года выхода фильмов'''

    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Book.objects.filter(draft=False).values("year")


# Create your views here.
class WantedBook(ListView):
    model = BookWanted


class ReadnowBook(ListView):
    model = BookReadnow


class BooksDetail(GenreYear, DetailView):
    model = Book
    template_name = 'locallibrary/books/book_detail.html'

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_queryset(self):
        a = Book.objects.filter(draft=False)
        return Book.objects.filter(draft=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        ip = self.get_client_ip(self.request)
        rating = Book.objects.filter(ratings__ip=ip, id=self.object.pk).values('ratings__star')
        if rating:
            context['rating_book'] = str(rating[0].get('ratings__star'))
        else:
            context['rating_book'] = None
        return context


class Books(GenreYear, ListView):
    model = Book
    template_name = 'locallibrary/books/book_list.html'
    paginate_by = 3


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


class FilterBooksView(GenreYear, ListView):
    template_name = 'locallibrary/books/book_list.html'
    paginate_by = 3

    ''' Фильтр книг '''

    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('genre')])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Book.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"book": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                book_id=int(request.POST.get("book")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
