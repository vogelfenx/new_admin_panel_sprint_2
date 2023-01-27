from django.contrib import admin

from movies.models import Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры фильма'


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    verbose_name = 'Персона'
    verbose_name_plural = 'Персоны фильма'


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmworkInline)
