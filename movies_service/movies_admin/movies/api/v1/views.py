from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesApiMixin:
    """Mixin for movies api views."""

    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet:
        """Return prepared filmworks queryset.

        Returns:
            QuerySet: filmworks
        """
        genres = ArrayAgg('genres__name', distinct=True)

        person_roles = [
            PersonFilmwork.RoleTypes.ACTOR,
            PersonFilmwork.RoleTypes.DIRECTOR,
            PersonFilmwork.RoleTypes.WRITER,
        ]

        (actors, directors, writers) = (
            ArrayAgg(
                'persons__full_name',
                filter=Q(persons__personfilmwork__role=role),
                distinct=True,
            ) for role in person_roles
        )

        filmworks = Filmwork.objects.values(
            'id', 'title', 'description', 'creation_date', 'rating',
            'type',
        ).annotate(
            genres=genres,
            actors=actors,
            directors=directors,
            writers=writers,
        )
        return filmworks

    def render_to_response(self, context: list[dict]) -> JsonResponse:
        """Return jsonified filmworks context.

        Args:
            context (list[dict]): List of filmworks as dictionary

        Returns:
            JsonResponse: response with jsonified context
        """
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """List Api view for movies."""

    paginate_by = 50

    def get_context_data(self, *, object_list: QuerySet = None) -> dict:
        """Prepare the context for the response.

        Args:
            object_list (QuerySet, optional): list of movies. Defaults to None.

        Returns:
            dict: prepared context for the response
        """
        filmworks = object_list if object_list is not None else self.object_list

        paginator, page, filmworks, _ = self.paginate_queryset(
            filmworks,
            self.paginate_by,
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(filmworks),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Detail Api view for a movie."""

    model = Filmwork
    http_method_names = ['get']

    def get_context_data(self, **kwargs) -> dict:
        """Return the movie object as a dictionary.

        Returns:
            dict: the movies object.
        """
        movie = kwargs['object']
        return movie
