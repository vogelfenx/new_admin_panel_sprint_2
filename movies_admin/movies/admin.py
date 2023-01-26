from django.contrib import admin

from movies.models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass
