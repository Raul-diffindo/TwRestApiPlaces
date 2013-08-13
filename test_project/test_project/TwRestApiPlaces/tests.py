
from django.test import TestCase

from models import Place, Trend, Tweet

class PlaceTestCase(TestCase):

    def setUp(self):
        Place.objects.create(name = 'World', code = 'en', woeid = '1')
        Place.objects.create(name = 'World-two', code = 'en')

    def test_trend_search(self):
        my_place = Place.objects.get(name = 'World-two')
        self.assertEqual(my_place.get_woeid_from_yahoo(), 'The place can search Woeid from Yahoo')
        self.assertEqual(my_place.get_trends(), 'The place can search Trends from Twitter')