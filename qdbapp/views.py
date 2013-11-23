from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from qdbapp.models import Quote

def default_context():
    return settings.QDB_SETTINGS.copy()

def do_or_404(action, catch=BaseException):
    try:
        return action()
    except catch:
        raise Http404

# http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django/5976065#5976065
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def single_quote(request, quote_id):
    quote_id = do_or_404(lambda: int(quote_id))

    context = default_context()
    context['title'] = 'Quote #%d' % quote_id
    context['quotes'] = [do_or_404(lambda: Quote.objects.get(id__exact=quote_id))]
    
    return render(request, 'quotes.html', context)

def quotes(request, **kwargs):    
    sort = request.GET.get('sort', 'newest')
    channel = kwargs.get('channel')
    username = kwargs.get('username')
    
    pagename = ''
    if not channel and not username:
        pagename = sort
    
    context = default_context()
    context['pagename'] = pagename

    # Filter by channel / username
    filter_query = {'%s__exact' % k: v for k, v in kwargs.iteritems()}
    quotes = Quote.objects.filter(**filter_query).order_by('-timestamp')

    # Filter by search query
    if 'q' in request.GET:
        
        # Functions used for searching
        must_contain = lambda quote: word.lower() in quote.body.lower()
        must_not_contain = lambda quote: word[1:].lower() not in quote.body.lower()
        
        # Make the query available to the template
        context['query'] = request.GET['q']
        
        # Iterate over search terms
        for word in request.GET['q'].split():
            # Negated terms
            if word.startswith('-'):
                quotes = filter(must_not_contain, quotes)
            # Regular terms
            else:
                quotes = filter(must_contain, quotes)
    
    # Filter by page
    quote_pages = Paginator(quotes, context['quotes_per_page'])
    try:
        context['quotes'] = quote_pages.page(request.GET.get('page'))
    except PageNotAnInteger:
        context['quotes'] = quote_pages.page(1)
    except EmptyPage:
        context['quotes'] = quote_pages.page(quote_pages.num_pages)

    # Build query string for pagination URLs
    paginate_query = request.GET.copy()
    if 'page' in paginate_query:
        del paginate_query['page']
    context['paginate_query'] = paginate_query.urlencode()
    if context['paginate_query']:
        context['paginate_query'] += '&'

    return render(request, 'quotes.html', context)

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
    
    context = default_context()
    context['pagename'] = 'add'
    context['quote_form'] = quote_form

    return render(request, 'add.html', context)

def vote(request, quote_id, direction):
    if request.method != 'POST':
        raise SuspiciousOperation

    quote_id = do_or_404(lambda: int(quote_id))
    direction = do_or_404(lambda: {'up': 1, 'down': -1}[direction])
    quote = do_or_404(lambda: Quote.objects.get(id__exact=quote_id))
    
    # Register the vote
    quote.add_vote(request.secretballot_token, direction)
    
    # Reload the quote to get the new vote count
    quote = Quote.objects.get(id__exact=quote_id)

    return HttpResponse(str(quote.vote_total))
