from django.contrib import admin

from .models import Category, Title, Genre, Review, Comment
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'email',
        'bio'
    )
    search_fields = ('email',)
    list_filter = ('email',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'category'
    )
    search_fields = ('name',)
    list_filter = ('name', 'genre')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'score',
        'pub_date'
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'review_id',
        'text',
        'author',
        'pub_date'
    )


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
