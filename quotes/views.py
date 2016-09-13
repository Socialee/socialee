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
    
    context = {
        "form": form,
    }
    
    return render(request, "create_quote.html", context)