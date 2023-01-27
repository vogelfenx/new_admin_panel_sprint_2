import uuid

from django.db import models


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


class Filmwork(UUIDMixin, TimeStampedMixin):

    class FilmworkTypes(models.TextChoices):
        MOVIE = 'F', 'Фильм'
        TV_SHOW = 'S', 'ТВ-Шоу'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    creation_date = models.DateField('Дата выхода', blank=True)
    rating = models.FloatField('Рейтинг', blank=True)
    type = models.CharField('Тип', max_length=1, choices=FilmworkTypes.choices)

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title
