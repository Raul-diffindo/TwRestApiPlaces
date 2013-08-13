
"""
YAHOO Direct YQL Settings
-------------------------
use percent encoding in the url

YAHOO_QUERY_WOEID_URL
    is a first part of complete URL for obtain WOEID number for specific place name.

YAHOO_QUERY_WOEID_FORMAT
    is where we can indicate the format for the response. For the moment only is possible the json format.
    Do not change for the moment.

Example:
    http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D%22Place%20Spain%22&format=json

See:
    http://developer.yahoo.com/yql/

"""
YAHOO_QUERY_WOEID_URL = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.places%20where%20text%3D%22Place%20'

YAHOO_QUERY_WOEID_FORMAT = '%22&format=json'


"""
Twitter REST API Settings.
---------------------------------

Put here your Twitter App access for API REST.
See your Twitter user/deveoper apps at https://dev.twitter.com/user/login?destination=docs


"""

CONSUMER_KEY = 'LwI1IORzO7nT4lUgXJtmHQ'

CONSUMER_SECRET = '5RywhXGbxelm1FsTCTWYsw7d585OMaTNI8b2gwDwo'

ACCESS_TOKEN = '418102122-DuBnnlwwF7T9v6uMhoohz1Knprl6ulbJF7jpvWyI'

ACCESS_TOKEN_SECRET = 'rfPWP6fjJf9kK7vcjTnhyO8WMPKyjJXg6t3WcJoIrc'

"""
Twitter REST API Settings.
---------------------------------
"""

BASE_URL = 'https://api.twitter.com/1.1/'

SEARCH_TRENDS_URL = 'trends/place.json?id='

SEARCH_TWEETS_URL = 'search/tweets.json'

EXCLUDE_HASHTAGS = '&exclude=hashtags'



