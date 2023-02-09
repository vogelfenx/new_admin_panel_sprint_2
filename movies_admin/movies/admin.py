from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest

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

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Overwrite get_queryset method.

        Args:
            request (HttpRequest): http request

        Returns:
            QuerySet: QuerySet of Persons
        """
        queryset = super(PersonAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related(
            Prefetch('filmworks', queryset=Filmwork.objects.distinct())
        )
        return queryset

    @admin.display(description=_('Filmworks'))
    def get_filmworks(self, person):
        """Return filmworks of the given person.

        Args:
            person: a person object

        Returns:
            SafeString: the list of filmworks html wrapped
        """
        filmworks_html_list = ''
        person_filmworks = person.filmworks.all()

        for filmwork in person_filmworks:
            filmwork_url = reverse('admin:movies_filmwork_change', args=[filmwork.id])
            filmworks_html_list = f"""
                                  {filmworks_html_list}
                                  <li><a href="{filmwork_url}">{filmwork.title}</a></li>
                                  """

        filmworks_html_list = f'<ul>{filmworks_html_list}</ul>'
        return mark_safe(filmworks_html_list)
