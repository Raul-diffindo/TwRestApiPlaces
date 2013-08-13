
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import oauth2 as oauth

class SingletonTwAuthentication(object):
    """
    Singleton Pattern for OAUTH Twitter Authentication Process
    """

    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
            token = oauth.Token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
            cls._instance = object.__new__(cls)
            cls._client = oauth.Client(consumer, token)

        return cls._instance

class TwAuthentication(SingletonTwAuthentication):

    def get_client(self):
        return self._client
