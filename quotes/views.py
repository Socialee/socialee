import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .forms import QuoteForm
from .models import Quote


def create_quote(request):
    form = QuoteForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, 'Danke! Wir gucken uns Dein Zitat an und veröffentlichen es, sofern es jugendfrei ist.')
        return HttpResponseRedirect('/')

    # else: # TODO: Gibt zwei mal error zurück, wenn form nicht ausgefüllt wird. (zb. bei raus hier)
    #   messages.error(request, 'Oh, da ist was schiefgelaufen.')
    
    context = {
        "form": form,
    }
    
    return render(request, "create_quote.html", context)


def show_all_quotes(request):
    quotes = Quote.objects.filter(active=True)
    
    if quotes:
        all_active_quotes = list(Quote.objects.filter(active=True))
        context = {
        "all_quotes": all_active_quotes
        }

        return render(request, "show-all-quotes.html", context)