from django.conf.urls import patterns, include, url

urlpatterns = patterns('qdbapp.views',
    url(r'^$', 'quotes'),
    url(r'^c/(?P<channel>([^/]+))/?$', 'quotes'),
    url(r'^u/(?P<username>([^/]+))/?$', 'quotes'),
    url(r'^q/(?P<quote_id>([0-9]+))/?$', 'single_quote'),
    url(r'^add/?$', 'add'),
    url(r'^vote/(?P<quote_id>([0-9]+))/(?P<direction>(up|down))/?$', 'vote'),
)
