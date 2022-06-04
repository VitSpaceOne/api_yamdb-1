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

from reviews.models import Category, Genre, Title
from users.permissions import Owner, Modertor


class CategoriesViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)


class ReviewViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (Owner | Modertor)

    def get_queryset(self):
        title = get_object_or_404(self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def get_perform_create(self, serializer):
        title = get_object_or_404(self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ListCreateRetrieveUpdateDeleteViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (Owner | Modertor)

    def get_queryset(self):
        review = get_object_or_404(self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def get_perform_create(self, serializer):
        review = get_object_or_404(self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
