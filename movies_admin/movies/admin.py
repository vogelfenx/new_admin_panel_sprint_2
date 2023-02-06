from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from movies.models import (Filmwork, Genre, GenreFilmwork, Person,
                           PersonFilmwork)


class GenreFilmWorkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name_plural = _('genres')
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    verbose_name_plural = _('persons')
    autocomplete_fields = ('person',)


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


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_filmworks')
    search_fields = ('full_name', 'personfilmwork__film_work__title')

    @admin.display(ordering='filmwork__title', description='Кинопроизведения')
    def get_filmworks(self, person):
        """Return filmworks of the given person.

        Args:
            person: a person object

        Returns:
            SafeString: the list of filmworks html wrapped
        """
        filmworks_html_list = ''
        for filmwork in person.filmworks.all():
            filmwork_url = reverse('admin:movies_filmwork_change', args=[filmwork.id])
            filmworks_html_list = f"""
                                  {filmworks_html_list}
                                  <li><a href="{filmwork_url}">{filmwork.title}</a></li>
                                  """

        filmworks_html_list = f'<ul>{filmworks_html_list}</ul>'
        return mark_safe(filmworks_html_list)
