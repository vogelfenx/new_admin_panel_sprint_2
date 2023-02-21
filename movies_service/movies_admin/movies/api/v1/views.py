from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet:
        genres = ArrayAgg('genres__name', distinct=True)
        actors = ArrayAgg(
            'persons__full_name',
            filter=Q(persons__personfilmwork__role=PersonFilmwork.RoleTypes.ACTOR),
            distinct=True,
        )
        directors = ArrayAgg(
            'persons__full_name',
            filter=Q(persons__personfilmwork__role=PersonFilmwork.RoleTypes.DIRECTOR),
            distinct=True,
        )
        writers = ArrayAgg(
            'persons__full_name',
            filter=Q(persons__personfilmwork__role=PersonFilmwork.RoleTypes.WRITER),
            distinct=True,
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

    def get_context_data(self, *, object_list=None, **kwargs):
        filmworks = list(object_list if object_list is not None else self.object_list)
        context = {
            'results': filmworks,
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
