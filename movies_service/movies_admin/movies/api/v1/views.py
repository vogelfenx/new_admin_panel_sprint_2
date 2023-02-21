from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']

    # def get(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     context = self.get_context_data()
    #     return self.render_to_response(context)

    def get_queryset(self) -> QuerySet:
        # filmwork = Filmwork.objects.values()
        filmworks = Filmwork.objects.values()
        return filmworks

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = object_list if object_list is not None else self.object_list
        filmworks = list(object_list)
        # filmworks = [filmwork for filmwork in filmworks_queryset]
        context = {
            'results': filmworks,
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
