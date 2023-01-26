from django.contrib import admin

from movies.models import Genre, Filmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    pass
