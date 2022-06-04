from rest_framework import filters, mixins, viewsets
from users.permissions import Admin, ReadOnly, Superuser
from django_filters.rest_framework import DjangoFilterBackend


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [Superuser | Admin | ReadOnly]

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'slug')


class ListCreateRetrieveUpdateDeleteViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = [Superuser | Admin | ReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('genre__slug', 'category__slug', 'name', 'year')
