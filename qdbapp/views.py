from django.shortcuts import render
from qdbapp.models import Quote

def quotes(request, **kwargs):
    
    sort = request.GET.get('sort', 'newest')
    channel = kwargs.get('channel')
    username = kwargs.get('username')
    
    pagename = ''
    if not channel and not username:
        pagename = sort

    data = {'pagename': pagename}

    filter_query = {'%s__exact' % k: v for k, v in kwargs.iteritems()}
    data['quotes'] = Quote.objects.filter(**filter_query)

    return render(request, 'quotes.html', data)
