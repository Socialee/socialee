from django.http import HttpResponse
from django.shortcuts import render

from .forms import QuoteForm
from .models import Quote


def create_quote(request):
	form = QuoteForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()

	context = {
		"form": form,
	}
	
	return render(request, "create_quote.html", context)