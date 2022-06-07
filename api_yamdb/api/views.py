from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Review, Title
from users.permissions import Admin, Moderator, ReadOnly, Superuser, User

from .filters import TitleFilter
from .serializers import (CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitlesSerializer)
from .viewsets import CategoryGenreViewSet, TitleReviewCommentViewSet


class CategoriesViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(TitleReviewCommentViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [Superuser | Admin | ReadOnly]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = Category.objects.get(slug=self.request.data.get('category'))
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        category = Category.objects.get(slug=self.request.data.get('category'))
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)


class ReviewsViewSet(TitleReviewCommentViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [Superuser | Admin | Moderator | User | ReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(TitleReviewCommentViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [Superuser | Admin | Moderator | User | ReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
