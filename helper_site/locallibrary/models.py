from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from autoslug import AutoSlugField
from uuslug import uuslug
from services.additional import instance_slug, replace_space_with_character
# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Genre(MPTTModel):
    name = models.CharField(max_length=40, verbose_name='Жанр')
    slug = models.SlugField(max_length=100, null=False, blank=True, default="")
    parent = TreeForeignKey('self',
                            related_name='children',
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Genre, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150,
                             null=False,
                             blank=False)
    description = models.TextField()
    author = models.ManyToManyField(Author, default="Неизвестный")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True)
    url = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    year = models.IntegerField(verbose_name="year of publishing", blank=True, null=True)
    image = models.ImageField(upload_to='articles/',
                              blank=True,
                              null=True,)

    slug = AutoSlugField(max_length=70,
                         db_index=True,
                         unique=True,
                         populate_from=instance_slug,
                         slugify=replace_space_with_character)

    reader = models.ManyToManyField(User, blank=True,)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.slug, instance=self)
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f"Название {self.title}"

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.slug])




class Wanted(models.Model):
    name = models.ForeignKey("Book",
                             on_delete=models.SET_NULL,
                             blank=False, null=True,
                             )

    def __str__(self):
        return self.name.title



class Readnow(models.Model):
    name = models.ForeignKey("Book",
                             on_delete=models.SET_NULL,
                             blank=False, null=True,
                             )
    def __str__(self):
        return self.name.title
