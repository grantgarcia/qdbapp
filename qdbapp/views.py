from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.shortcuts import render, redirect

from qdbapp.models import Quote

# http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django/5976065#5976065
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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

class QuoteForm(ModelForm):
    
    class Meta:
        model = Quote
        fields = ['body', 'channel', 'username']

    def clean_channel(self):
        self.cleaned_data['channel'] = self.cleaned_data['channel'].lstrip('#')
        return self.cleaned_data['channel']

def add(request):

    if request.method == 'POST':
        quote_form = QuoteForm(request.POST)
        if quote_form.is_valid():
            quote = quote_form.save(commit=False)
            quote.ip = get_client_ip(request)
            quote.save()
            return redirect('/')
    else:
        quote_form = QuoteForm()
    
    data = {'pagename': 'add', 'quote_form': quote_form}
    return render(request, 'add.html', data)
