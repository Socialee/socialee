import os, random
import requests

from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse

from allauth.account.views import RedirectAuthenticatedUserMixin, SignupView

import random
from .models import Project, Input, Output

from .forms import StartProjectForm

# from quotes import views
from quotes.models import Quote


# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['quotes'] = list(Quote.objects.filter(active=True))
        context['random_quote'] = random.choice(context['quotes'])

        return context

    # def get_queryset(self): # get_queryset ist für ListViews obligatorisch
    #     """Return the last five published questions. (Not including those set to be published in the future.)"""
    #     x = Question.objects.filter(pub_date__lte=timezone.now())
    #     y = x.order_by('-pub_date')[:5]

    #     return y

class Home(BaseView, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['template'] = '"000" Landingpage (/) (home.html)' # zu testzwecken

        return context


class WelcomePage(BaseView, TemplateView):
    template_name = 'welcome.html'

    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)
        context['template'] = '"100" Welcomepage (/welcome/) (welcome.html)' # zu testzwecken

        return context


class StartProject(BaseView, TemplateView):
    template_name = 'start_project.html'

    def get_context_data(self, **kwargs):
        context = super(StartProject, self).get_context_data(**kwargs)
        context['template'] = '"101" Start_Projekt (/startproject/) (startproject.html)' # zu testzwecken
        form = StartProjectForm()
        context['startprojectform'] = {"form": form,}

        return context


class ProjectOverview(BaseView, TemplateView):
    template_name = 'project_overview.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectOverview, self).get_context_data(**kwargs)
        context['template'] = '"001" Projektübersicht (/projects/) (project_overview.html)' # zu testzwecken

        return context


class UserProfile(BaseView, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['template'] = '"300" User Profilseite (/userID/profile/ (user_profile.html))' # zu testzwecken

        return context


class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'

    def get_context_data(self, **kwargs):
        context = super(Impressum, self).get_context_data(**kwargs)
        context['template'] = '"00x" Impressum (/impressum) (impressum.html)' # zu testzwecken

        return context