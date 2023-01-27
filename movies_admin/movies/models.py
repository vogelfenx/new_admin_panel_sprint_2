import uuid

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('Имя', max_length=255)
    description = models.TextField('Описание', blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField('Полное имя', max_length=255)

    class Meta:
        db_table = 'content"."person'
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkTypes(models.TextChoices):
        MOVIE = 'F', 'Фильм'
        TV_SHOW = 'S', 'ТВ-Шоу'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    creation_date = models.DateField('Дата выхода', blank=True)
    rating = models.FloatField('Рейтинг', blank=True, validators=[
        MinValueValidator(0),
        MaxValueValidator(100),
    ])
    type = models.CharField('Тип', max_length=1, choices=FilmworkTypes.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
