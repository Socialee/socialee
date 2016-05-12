import os, random
import requests

from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse

from allauth.account.views import RedirectAuthenticatedUserMixin, SignupView

import random
from .models import Project, Input, Output

from .forms import StartProjectForm

from quotes.models import Quote


# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        quotes = Quote.objects.filter(active=True)
        if quotes:
            all_active_quotes = list(Quote.objects.filter(active=True))
            context['random_quote'] = random.choice(all_active_quotes)
        return context


class Home(BaseView, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        return context


class WelcomePage(BaseView, TemplateView):
    template_name = 'welcome.html'

    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)

        return context


class StartProject(BaseView, TemplateView):
    template_name = 'start_project.html'

    def get_context_data(self, **kwargs):
        context = super(StartProject, self).get_context_data(**kwargs)
        form = StartProjectForm()
        context['startprojectform'] = {"form": form,}

        return context


class ProjectOverview(BaseView, TemplateView):
    template_name = 'project_overview.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectOverview, self).get_context_data(**kwargs)

        return context


class UserProfile(BaseView, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)

        return context


class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'

    def get_context_data(self, **kwargs):
        context = super(Impressum, self).get_context_data(**kwargs)

        return context