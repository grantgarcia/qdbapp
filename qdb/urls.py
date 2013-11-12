from django.conf.urls import patterns, include, url

urlpatterns = patterns('qdbapp.views',
    url(r'^$', 'quotes'),
    url(r'^c/(?P<channel>([^/]+))/?$', 'quotes'),
    url(r'^u/(?P<username>([^/]+))/?$', 'quotes'),
)
