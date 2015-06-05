from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    context = {}
    template = 'home.html'
    return render(request, template, context)


class Cafe(TemplateView):
	template_name = 'cafe.html'