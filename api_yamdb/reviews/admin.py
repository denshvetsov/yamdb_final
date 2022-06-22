from django.contrib.admin import ModelAdmin, register

from .models import Comments, Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('pk', 'title', 'author', 'score', 'text', 'pub_date')


@register(Comments)
class CommentsAdmin(ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('review',)
