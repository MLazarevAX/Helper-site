from django.db import models


# Create your models here.
class Autor(models.Model):
    first_name = models.CharField(max_length=40, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=40, verbose_name='Отчество', blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Readers(models.Model):
    login = models.CharField(max_length=50, verbose_name='Логин', null=False, blank=False)
    first_name = models.CharField(max_length=40, verbose_name='Имя')

    def __str__(self):
        return self.login

class Genre(models.Model):
    name = models.CharField(max_length=40, verbose_name='Категория')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField()
    autor = models.ManyToManyField(Autor, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True)
    url = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    year = models.IntegerField(verbose_name="year of publishing")
    image = models.ImageField(upload_to='articles/')

    reader = models.ManyToManyField(Readers, verbose_name="Readers the book")

    def __str__(self):
        return f"Название {self.title}, Автор: {self.autor}"


class Wanted(models.Model):
    name = models.ForeignKey(Books, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Хочу прочесть')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name

class Readnow(models.Model):
    name = models.ForeignKey(Books, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='Читаю сейчас')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name