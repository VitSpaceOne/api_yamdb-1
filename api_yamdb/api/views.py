from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from users.permissions import Admin, ReadOnly, Owner
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategoriesSerializer, CommentsSerializer, GenresSerializer, ReviewsSerializer, TitlesSerializer
)

from reviews.models import Category, Genre, Title, Review


class ListCreateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, 
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = (
        Admin,
        IsAuthenticatedOrReadOnly
    )

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name', 'slug')


class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class ListCreateRetrieveUpdateDeleteViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [Owner&Admin|ReadOnly]
    filter_backends = (filters.SearchFilter)
    search_fields = ('genre__slug', 'category__slug', 'name', 'year')


class TitlesViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)


class ReviewViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = ReviewsSerializer

      

class CommentViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = CommentsSerializer