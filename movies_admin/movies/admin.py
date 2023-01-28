from django.contrib import admin

from movies.models import Filmwork, Genre, Person, GenreFilmwork, PersonFilmwork


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = 'Жанр'
    verbose_name_plural = 'Жанры фильма'


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    verbose_name = 'Персона'
    verbose_name_plural = 'Персоны фильма'



@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline, PersonFilmworkInline)

    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = ('type', )

    search_fields = ('title', 'description', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

