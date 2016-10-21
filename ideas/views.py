from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView

from .forms import *
from .models import Idea


class CreateIdea(CreateView):
    model = Idea
    template_name = 'create_idea.html'
    form_class = IdeaForm
    success_url = reverse_lazy('idea_list')


def idea_list(request):
    idea_list = Idea.objects.filter(active=True).order_by('-subm_date')
    context = {
        "idea_list": idea_list,
    }
    
    return render(request, "idea_list.html", context)