from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'qdbapp.views.quotes'),
    url(r'^c/(?P<channel>([^/]+))/?$', 'qdbapp.views.quotes'),
    url(r'^u/(?P<username>([^/]+))/?$', 'qdbapp.views.quotes'),

    #url(r'^search/?', include('haystack.urls')),
)
