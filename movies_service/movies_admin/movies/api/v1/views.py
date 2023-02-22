from typing import Any

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork, PersonFilmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 10

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.request.GET.get('page'):
            self.paginate_by = None
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
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

    def get_context_data(self, *, object_list: QuerySet = None, **kwargs: Any) -> dict:
        filmworks = object_list if object_list is not None else self.object_list
        if self.paginate_by:
            paginator, page, filmworks, _ = self.paginate_queryset(
                filmworks,
                self.paginate_by,
            )

            context = {
                'count': paginator.count,
                'total_pages': paginator.num_pages,
            }

            if page.has_previous():
                context.update({
                    'prev': page.previous_page_number(),
                })
            if page.has_next():
                context.update({
                    'next': page.next_page_number(),
                })

        else:
            context = {
                'count': filmworks.count(),
            }

        context.update({
            'results': list(filmworks),
        })

        return context

    def render_to_response(self, context: dict, **response_kwargs: Any) -> JsonResponse:
        return JsonResponse(context)
