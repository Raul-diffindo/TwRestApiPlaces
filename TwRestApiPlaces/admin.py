
from django.contrib import admin

from models import *
from forms import *

class PlaceAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Place.
    """

    list_display = (
        'name',
        'code',
        'woeid',
    )
    search_fields = (
        'name',
        'code',
        'woeid',
    )
    list_filter = (
        'code',
    )
    form = PlaceForm
admin.site.register(Place, PlaceAdmin)


class TrendAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Trend.
    """

    list_display = (
        'name',
        'query',
        'slug',
        'url',
        'trend_created_at',
        'importance',
        'promoted',
        'place'
    )
    search_fields = (
        'name',
        'place',
    )
    list_filter = (
        'place',
    )
    form = TrendForm
admin.site.register(Trend, TrendAdmin)


class TweetAdmin(admin.ModelAdmin):
    """
    ModelAdmin for Tweet.
    """

    list_display = (
        'tweet_published_at',
        'language',
        'retweets_count',
        'from_username',
        'user_screen_name',
        'user_profile_image',
        'tweet',
        'trend'
    )
    search_fields = (
        'language',
        'from_username',
        'trend',
    )
    list_filter = (
        'trend',
    )
    form = TweetForm
admin.site.register(Tweet, TweetAdmin)