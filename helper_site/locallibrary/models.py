from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Autor(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Genre(MPTTModel):
    name = models.CharField(max_length=40, verbose_name='Жанр')
    slug = models.SlugField(max_length=100, null=True, blank=True)
    parent = TreeForeignKey('self',
                            related_name='children',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150,
                             null=False,
                             blank=False)
    description = models.TextField()
    autor = models.ManyToManyField(Autor,
                              null=True,
                              blank=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, blank=True)
    url = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    year = models.IntegerField(verbose_name="year of publishing", blank=True, null=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    slug = models.SlugField(max_length=100, null=True, blank=True)
    reader = models.ManyToManyField(User,
                                    blank=True,
                                    null=False)

    def __str__(self):
        return f"Название {self.title}, Автор: {self.autor}"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])




class Wanted(models.Model):
    name = models.ForeignKey(Book,
                             on_delete=models.SET_NULL,
                             blank=False, null=True,
                             )
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name.title



class Readnow(models.Model):
    name = models.ForeignKey("Book",
                             on_delete=models.SET_NULL,
                             blank=False, null=True,
                             )
    slug = models.SlugField(max_length=100, blank=True, null=True)
    def __str__(self):
        return self.name.title
