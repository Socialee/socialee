from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import Idea


def create_idea(request):
    form = IdeaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        # messages.success(request, 'neue Idee gespeichert')
        return HttpResponseRedirect(reverse(review_idea, args=(instance.id,)))
    
    context = {
        "form": form,
    }
    
    return render(request, "create_idea.html", context)


def review_idea(request,id):
    instance = get_object_or_404(Idea, id=id)
    context = {
        "idea": instance,
        }
    return render(request, "review_idea.html", context)


def idea_list(request):
    idea_list = Idea.objects.filter(active=True).order_by('-subm_date')
    context = {
        "idea_list": idea_list,
    }
    
    return render(request, "idea_list.html", context)