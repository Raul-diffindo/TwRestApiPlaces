from django import forms

from models import Place, Trend, Tweet

class PlaceForm(forms.ModelForm):
    """
    Place model form
    """
    class Meta:
        model = Place
        fields = ('name', 'code', 'woeid')

class TrendForm(forms.ModelForm):
    """
    Trend model form
    """
    class Meta:
        model = Trend
        fields = ('name', 'query', 'slug', 'url', 'trend_created_at', 'importance', 'promoted', 'place')

class TweetForm(forms.ModelForm):
    """
    Tweet model form
    """
    class Meta:
        model = Tweet
        fields = ('tweet_published_at', 'language', 'retweets_count', 'from_username', 'user_screen_name',
                  'user_profile_image', 'tweet', 'trend')