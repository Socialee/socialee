import datetime, random
from django import template
from quotes.models import Quote

register = template.Library()

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def random_quote():
    quotes = Quote.objects.filter(active=True)
    if quotes:
        all_active_quotes = list(Quote.objects.filter(active=True))
        random_quote = random.choice(all_active_quotes)

        return {'title':random_quote.title, 'author':random_quote.author}

    else:
        return '...'

