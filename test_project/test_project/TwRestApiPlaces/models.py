import json
import urllib
import urllib2, re
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import defaultfilters
from dateutil.parser import *
from datetime import datetime
from django.utils.timezone import utc

from exceptions import YahooSearchException, TwitterRestAPIException
from settings import *
from tw_authentication import TwAuthentication

class Place(models.Model):
    """
    Place Model
    """
    created_at = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=2, null=True, blank=True, unique=True)
    woeid = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = u'Places'

    def __unicode__(self):
        if self.woeid:
            return u"%s, %i" % (self.name, self.woeid)
        else:
            return u"%s" % (self.name)

    def get_woeid_from_yahoo(self):
        """
        Search and return the WOEID number of this place using Yahoo API. With this number we can obtain the top
        10 trending topics from Twitter.
        """
        if self.woeid is None:
            json_data = json.load(urllib2.urlopen(YAHOO_QUERY_WOEID_URL + self.name + YAHOO_QUERY_WOEID_FORMAT))

            if json_data['query']['results']['place'][0]['name'] == self.name:
                self.woeid = json_data['query']['results']['place'][0]['woeid']
                self.save()

            else:
                raise YahooSearchException(1000)

        return self.woeid


    def get_trends(self, exclude_hashtags = False, get_tweets = True, result_type = 'mixed', count = '15'):
        """
        Return the top 10 trending topics from Twitter using Rest API for a specific WOEID.
        """
        client_authenticated = TwAuthentication()

        if exclude_hashtags:
            json_data = client_authenticated.get_client().request(BASE_URL + SEARCH_TRENDS_URL + str(self.woeid) +
                                                                  EXCLUDE_HASHTAGS)
        else:
            json_data = client_authenticated.get_client().request(BASE_URL + SEARCH_TRENDS_URL + str(self.woeid))

        if json_data[0].status == 200:
            tendencias_json = json.loads(json_data[1].replace('null', '"null"'))
            cont_importance = 1

            for trend_item in tendencias_json[0]['trends']:

                new_trend = Trend(
                    name = u''+trend_item['name'],
                    query = u''+trend_item['query'],
                    url = trend_item['url'],
                    importance = cont_importance,
                    place = self,
                )

                new_trend.set_promoted(trend_item['promoted_content'])
                new_trend.set_trend_created_at(tendencias_json[0]['created_at'])
                new_trend.save()

                cont_importance += 1

                #Update Tweets
                if get_tweets:
                    new_trend.get_tweets(new_trend.name, self.code, result_type, count)

        else:
            raise TwitterRestAPIException(json_data[0].status)




class Trend(models.Model):
    """
    Trend Model
    """
    created_at = models.DateTimeField(auto_now_add = True)
    name = models.CharField(max_length=200)
    query = models.CharField(max_length=200)
    slug = models.SlugField()
    url = models.URLField()
    trend_created_at = models.DateTimeField(null = True)
    importance = models.SmallIntegerField()
    promoted = models.BooleanField()

    place = models.ForeignKey(Place)

    class Meta:
        ordering = ['-trend_created_at']
        verbose_name_plural = u'Trends'

    def get_trend_name_cleaned(self):
        return re.sub('[^A-Za-z0-9]+', '', u''+ str(self.name.replace('#','').encode('ascii', 'ignore')))


    def __unicode__(self):
        return u"%s, %s, %s" % (self.name, self.place.name, self.url)

    def set_promoted(self, promoted_field):
        """
        If field of request to Tw Rest Api return null in promoted field, this trend is not a trend prmoted
        """
        if promoted_field == 'null':
            self.promoted = False
        else:
            self.promoted = True

    def set_trend_created_at(self, datetime_string):
        try:
            self.trend_created_at = parse(datetime_string).replace(tzinfo=utc)
        except ValueError:
            self.trend_created_at = datetime.now()

    def exist_trend(self, *args, **kwargs):
        """
        A trend is the same if the DateTime created in Twitter is the same and query, name and place matches.
        """
        try:
            trend_created = Trend.objects.get(trend_created_at = self.trend_created_at,
                                              query = self.query,
                                              name = self.name,
                                              place = self.place,
                                            )
            trend_created.importance = self.importance
            super(Trend, self).save(*args, **kwargs)
            return True

        except ObjectDoesNotExist:
            return False

    def save(self, *args, **kwargs):
        """
        If not exist the Trend in DB actually we do the save
        """
        if not self.exist_trend():
            self.slug = defaultfilters.slugify(self.name)
            super(Trend, self).save(*args, **kwargs)



    def get_tweets(self, q, lang, result_type, count):
        """
        Returns a collection of relevant Tweets matching a specified query.
        Parameters:
        q. Trend name.
        lang. Restricts tweets to the given language. See http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        result_type. mixed: Include both popular and real time results in the response.
                     recent: return only the most recent results in the response.
                     popular: return only the most popular results in the response.
        count. The number of tweets to return per page, up to a maximum of 100. Defaults to 15
        """
        client_authenticated = TwAuthentication()

        parameters = {
            'q': self.get_trend_name_cleaned(),
            'lang': lang,
            'result_type': result_type,
            'count': count,
        }

        json_data = client_authenticated.get_client().request(BASE_URL + SEARCH_TWEETS_URL + '?' + urllib.urlencode(parameters))

        if json_data[0].status == 200:
            tweets_json = json.loads(json_data[1].replace('null', '"null"'))
            for tweet_item in tweets_json['statuses']:

                new_tweet = Tweet(
                    tweet_twitter_id = tweet_item['id_str'],
                    language = tweet_item['lang'],
                    retweets_count = tweet_item['retweet_count'],
                    from_username = u''+ str(tweet_item['user']['name'].encode('ascii', 'ignore')),
                    from_userid = tweet_item['user']['id_str'],
                    user_screen_name = u''+ str(tweet_item['user']['screen_name'].encode('ascii', 'ignore')),
                    user_profile_image = tweet_item['user']['profile_image_url'],
                    tweet = u''+ str(tweet_item['text'].encode('ascii', 'ignore')),
                    trend = self,
                )

                new_tweet.set_tweet_published_at(tweet_item['created_at'])
                new_tweet.save()

        else:
            raise TwitterRestAPIException(json_data[0].status)




class Tweet(models.Model):
    """
    Tweet Model
    """
    created_at = models.DateTimeField(auto_now_add = True)
    tweet_twitter_id = models.CharField(max_length=150)
    tweet_published_at = models.DateTimeField()
    language = models.CharField(max_length=4)
    retweets_count = models.IntegerField()
    from_username = models.CharField(max_length=150)
    from_userid = models.CharField(max_length=50)
    user_screen_name = models.CharField(max_length=150)
    user_profile_image = models.URLField(max_length=250)
    tweet = models.CharField(max_length=160)

    trend = models.ForeignKey(Trend)

    class Meta:
        ordering = ['-tweet_published_at']
        verbose_name_plural = u'Tweets'

    def __unicode__(self):
        return u"%s, %s, %s" % (self.trend.place.name, self.trend.name, self.tweet)

    def exist_tweet(self, *args, **kwargs):
        """
        A tweet is the same if the trend is the same, language is te same, was published at the same time and twitter
        id matches.
        """
        try:
            tweet_created = Tweet.objects.get(trend = self.trend,
                                              tweet_published_at = self.tweet_published_at,
                                              language = self.language,
                                              tweet_twitter_id = self.tweet_twitter_id,
                                            )
            tweet_created.retweets_count = self.retweets_count
            super(Tweet, self).save(*args, **kwargs)

            return True

        except ObjectDoesNotExist:
            return False

    def set_tweet_published_at(self, datetime_string):
        try:
            self.tweet_published_at = parse(datetime_string).replace(tzinfo=utc)
        except ValueError:
            self.tweet_published_at = datetime.now()

    def save(self, *args, **kwargs):
        """
        If not exist the tweet in DB actually we do the save
        """
        tweet_created = self.exist_tweet()
        if not tweet_created:
            super(Tweet, self).save(*args, **kwargs)


    def get_mentions(self):
        """
        Return a list of users mentioned in tweet
        """
        mentions = []
        patron_mentions = re.compile('(^|[^@\w])+@([A-Za-z0-9_]+)')
        for m in patron_mentions.finditer(self.tweet):
            mentions.append(m.group().strip())

        return mentions
