import os, random
import requests
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin


from allauth.account.views import *
from allauth.account.forms import *
from allauth.account.decorators import verified_email_required

from .models import Project, Input, Output, Profile
from .forms import *

User = get_user_model()

# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        return context


class Home(BaseView, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        return context


class WelcomePage(BaseView, ListView):
    template_name = 'welcome.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)

        return context


# CRUD CREATE PROJECT
class StartProject(BaseView, CreateView):
    template_name = 'start_project.html'
    model = Project
    form_class = StartProjectForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        valid_data = super(StartProject, self).form_valid(form)
        # form.instance.managers.add(user)

        return valid_data

    def get_context_data(self, **kwargs):
        context = super(StartProject, self).get_context_data(**kwargs)

        return context


# CRUD LIST OF ALL PROJECTS
class ProjectOverview(BaseView, ListView):
    template_name = 'project_overview.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectOverview, self).get_context_data(**kwargs)

        return context


# CRUD RETRIEVE PARTICULAR PROJECT
class ProjectDetailView(BaseView, DetailView):
    template_name = 'project_template.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        return context


# CRUD UPDATE PARTICULAR PROJECT
class ProjectUpdateView(BaseView, UpdateView):
    template_name = 'edit_project.html'
    model = Project
    form_class = EditProjectForm

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView, self).get_context_data(**kwargs)

        return context

    # Nur der Admin und die Manager des Projektes kann Änderungen vornehmen
    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(ProjectUpdateView, self).get_object(*args, **kwargs)
        if obj.created_by == user or user in obj.managers.all():
            return obj
        else:
            raise Http404


# def user_profile(request):
#     user = get_object_or_404(User, username=request.user)
#     profile, created = Profile.objects.get_or_create(user=user)
#     context = {
#     "profile": profile,
#     }
#     return render (request, 'user_profile.html', context)

class User_profileView(BaseView, UpdateView):
    template_name = 'user_profile.html'
    model = Profile
    form_class = None
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(User_profileView, self).get_context_data(**kwargs)

        return context


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    context = {
    "profile": profile,
    }
    return render (request, 'profile_view.html', context)


def Invite_me(request):
    form = InviteForm(request.POST or None)
    context = {
        "form": form,
    }

    if request.method=='POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Danke für Deine Nachricht! Wir melden uns ganz bald.')
            form_email = form.cleaned_data.get("email")
            form_message = form.cleaned_data.get("message")
            form_full_name = form.cleaned_data.get("full_name")
            subject = 'Ladet mich ein!'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, 'hello@socialee.de']
            contact_message = "%s via %s schreibt:\n\n %s"%( 
                    form_full_name, 
                    form_email,
                    form_message)
            some_html_message = """
            <h1>Hallo Mo!</h1>
            """
            send_mail(subject, 
                    contact_message, 
                    from_email, 
                    to_email,
                    fail_silently=True)

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'invite_me.html', context)


class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'

    def get_context_data(self, **kwargs):
        context = super(Impressum, self).get_context_data(**kwargs)

        return context        