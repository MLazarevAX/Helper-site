from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from autoslug import AutoSlugField
from uuslug import uuslug
from services.additional import instance_slug, replace_space_with_character
from django.urls import reverse
from django.utils.safestring import mark_safe


# Create your models here.

class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Author(models.Model):
    """Автор"""
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(MPTTModel):
    """ Жанр """
    name = models.CharField(max_length=40, verbose_name='Жанр')
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self',
                            related_name='children',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True, )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Genre, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    """Книга"""
    title = models.CharField("Название", max_length=150)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    authors = models.ManyToManyField(Author,
                                     verbose_name="автор",
                                     related_name="book_autor",
                                     default="Неизвестный")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    country = models.CharField("Страна",
                               max_length=150,
                               blank=True,
                               null=True)

    poster = models.ImageField("Постер",
                               upload_to='articles/',
                               blank=True,
                               null=True)

    year = models.PositiveSmallIntegerField("Дата публикации",
                                            default=2000,
                                            blank=True,
                                            null=True)

    slug = AutoSlugField(max_length=70,
                         db_index=True,
                         unique=True,
                         populate_from=instance_slug,
                         slugify=replace_space_with_character)

    url = models.CharField("Ссылка на книгу",
                           max_length=150,
                           blank=True,
                           null=True)
    reader = models.ManyToManyField(User, blank=True)
    draft = models.BooleanField("Черновик", default=False)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.slug, instance=self)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_image(self):
        if self.poster:
            return mark_safe(f'<img src={self.poster.url} width="100" height="110"')
        else:
            return '(Нет изображения)'

    get_image.short_description = "Постер"
    get_image.allow_tags = True

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.CASCADE, blank=True, null=True
    )
    book = models.ForeignKey(Book, verbose_name="Книга", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.book}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class BookWanted(models.Model):
    """Хочу прочесть"""
    name = models.ForeignKey(Book,
                             on_delete=models.SET_NULL,
                             blank=False,
                             null=True,
                             )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Хочу прочитать"
        verbose_name_plural = "Хочу прочитать"


class BookReadnow(models.Model):
    """Читаю сейчас"""
    name = models.ForeignKey("Book",
                             on_delete=models.SET_NULL,
                             blank=False, null=True,
                             )

    def __str__(self):
        return self.name.title

    class Meta:
        verbose_name = "Читаю сейчас"
        verbose_name_plural = "Читаю сейчас"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="книга", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.book}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"
