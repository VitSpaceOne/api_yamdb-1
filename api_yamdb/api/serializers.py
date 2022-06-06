import datetime
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from django.db.models import Avg

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def validate_genre(self, value):
        for slug in value:
            if Genre.objects.get(slug=slug).exists():
                continue
            return value
        raise serializers.ValidationError("Указанный жанр не существует")

    def validate_category(self, value):
        if (
            self.request.data.get('category')
            and Category.objects.get(slug=value).exists()
        ):
            return value
        raise serializers.ValidationError("Указанная категория не существует")

    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value

    def get_rating(self, obj):
        if not obj.reviews.all().exists():
            return None
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        request = self.context.get('request')
        title_id = request.parser_context.get('kwargs').get('title_id')
        title = get_object_or_404(Title, id=title_id)
        user = request.user
        if (
            user.reviews.filter(title=title).exists()
            and request.method == 'POST'
        ):
            raise serializers.ValidationError("Нельзя оставить второй отзыв")
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError(
                'Оценка за пределами допустимого диапазона'
            )
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')
