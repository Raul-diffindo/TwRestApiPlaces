from django.core.context_processors import csrf
from django.db.utils import IntegrityError
from django.shortcuts import render_to_response
from django.template import RequestContext
from TwRestApiPlaces.models import *

def test(request):
    test_place = None
    try:
        test_place = Place.objects.create(name = 'Spain', code = 'es')
    except IntegrityError as e:
        #Write to log file e exception
        pass

    if not test_place: test_place = Place.objects.get(name = 'Spain')

    try:
        test_place.get_woeid_from_yahoo()
    except YahooSearchException as e:
        #Write to log file e exception
        pass

    #Get Actual Trends Of Spain Place
    test_place.get_trends()

    context = {
        'Places': Place.objects.all(),
        'Trends_Spain': test_place.trend_set.all(),
    }
    context.update(csrf(request))
    return render_to_response('test.html', context, RequestContext(request))