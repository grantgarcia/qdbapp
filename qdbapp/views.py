from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

    # Filter by channel / username
    filter_query = {'%s__exact' % k: v for k, v in kwargs.iteritems()}
    quotes = Quote.objects.filter(**filter_query).order_by('-timestamp')

    # Filter by search query
    if 'q' in request.GET:
        
        # Functions used for searching
        must_contain = lambda quote: word.lower() in quote.body.lower()
        must_not_contain = lambda quote: word[1:].lower() not in quote.body.lower()
        
        # Make the query available to the template
        data['query'] = request.GET['q']
        
        # Iterate over search terms
        for word in request.GET['q'].split():
            # Negated terms
            if word.startswith('-'):
                quotes = filter(must_not_contain, quotes)
            # Regular terms
            else:
                quotes = filter(must_contain, quotes)
    
    # Filter by page
    quote_pages = Paginator(quotes, 20)
    try:
        data['quotes'] = quote_pages.page(request.GET.get('page'))
    except PageNotAnInteger:
        data['quotes'] = quote_pages.page(1)
    except EmptyPage:
        data['quotes'] = quote_pages.page(quote_pages.num_pages)

    # Build query string for pagination URLs
    paginate_query = request.GET.copy()
    if 'page' in paginate_query:
        del paginate_query['page']
    data['paginate_query'] = paginate_query.urlencode()
    if data['paginate_query']:
        data['paginate_query'] += '&'

    return render(request, 'quotes.html', data)


def add(request):

    data = {'pagename': 'add'}

    return render(request, 'add.html', data)
