from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import Idea


def create_idea(request):
    form = IdeaForm_first(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, 'neue Idee gespeichert')
        next_url = str(instance.id) + '/details'
        return HttpResponseRedirect(next_url)
    
    context = {
        "form": form,
    }
    
    return render(request, "create_idea.html", context)


def idea_details(request, id=None):
    instance = get_object_or_404(Idea, id=id)
    form = IdeaForm_second(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, 'Super, deine Details wurden gespeichert!')

        return HttpResponseRedirect(reverse('idea_author', args=[instance.id]))
    
    context = {
        "form": form,
        "idee": instance,
    }
    
    return render(request, "idea_details.html", context)


def idea_author(request, id=None):
    instance = get_object_or_404(Idea, id=id)
    form = IdeaForm_third(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.save()
        messages.success(request, 'Danke! Wir gucken uns Deine Idee an und veröffentlichen sie dann.')
        return HttpResponseRedirect('/')
    
    context = {
        "form": form,
    }
    
    return render(request, "idea_email.html", context)


def idea_list(request):
    idea_list = Idea.objects.filter(active=True).order_by('-subm_date')
    context = {
        "idea_list": idea_list,
    }
    
    return render(request, "idea_list.html", context)