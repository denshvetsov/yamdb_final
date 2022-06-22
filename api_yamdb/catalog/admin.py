from django.contrib.admin import ModelAdmin, register

from .models import Category, Genre, Title


@register(Title)
class TitleAdmin(ModelAdmin):
    list_display = (
        'pk', 'category', 'name', 'year', 'display_genres')
    search_fields = ('name',)
    list_filter = ('name',)

    def display_genres(self, obj):
        return '\n'.join(
            str(name) for name in obj.genre.values_list('name', flat=True)
        )


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}


@register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
