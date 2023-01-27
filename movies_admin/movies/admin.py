from django.contrib import admin

from movies.models import Filmwork, Genre, GenreFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmWorkInline,)
