from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^test/', test),
    (r'^', test),
)
