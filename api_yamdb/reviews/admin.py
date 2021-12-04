from django.contrib import admin

from .models import Categories, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    list_editable = ('role',)
    search_fields = ('username', 'role')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('title', 'text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('review', 'text',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )

    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )

    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'categories',
    )

    list_editable = ('name', 'description', 'categories', 'year')
    search_fields = ('name', 'year', 'genre', 'categories')


admin.site.register(User, UserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Title, TitleAdmin)
