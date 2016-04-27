import os
import requests

from django.conf import settings
from django.views.generic import TemplateView

from allauth.account.views import RedirectAuthenticatedUserMixin, SignupView

from .models import Project, Input, Output


# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        return context


class Home(BaseView, SignupView):
    template_name = 'home.html'


class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'


class WelcomePage(BaseView, TemplateView):
    template_name = 'welcome.html'


class StartPage(BaseView, TemplateView):
    template_name = 'start.html'


class ProjectOverview(BaseView, TemplateView):
    template_name = 'project_overview.html'