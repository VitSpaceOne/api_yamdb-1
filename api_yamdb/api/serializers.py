from rest_framework import serializers

from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)

from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
