from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .viewsets import (
    ListCreateDeleteViewSet,
    ListCreateRetrieveUpdateDeleteViewSet
)
from .serializers import (
    CategoriesSerializer, CommentsSerializer,
    GenresSerializer, ReviewsSerializer, TitlesSerializer
)

from reviews.models import Category, Genre, Title, Review
from users.permissions import Owner, Modertor, Superuser, Admin, ReadOnly


class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = PageNumberPagination


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    pagination_class = PageNumberPagination


class TitlesViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [Superuser | Admin | ReadOnly]
    pagination_class = PageNumberPagination


class ReviewViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [Superuser | Admin | ReadOnly | Owner | Modertor]

    def get_queryset(self):
        title = get_object_or_404(Title, self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def get_perform_create(self, serializer):
        title = get_object_or_404(Title, self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [Superuser | Admin | ReadOnly | Owner | Modertor]

    def get_queryset(self):
        review = get_object_or_404(Review, self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def get_perform_create(self, serializer):
        review = get_object_or_404(Review, self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
