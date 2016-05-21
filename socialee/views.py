import os, random
import requests
import random

from django.conf import settings
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.mail import send_mail

from allauth.account.views import RedirectAuthenticatedUserMixin, SignupView

from .models import Project, Input, Output
from .forms import StartProjectForm, InviteForm
from quotes.models import Quote


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


class ProjectDetailview(BaseView, TemplateView):
    template_name = 'project_template.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailview, self).get_context_data(**kwargs)

        return context


class UserProfile(BaseView, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)

        return context


def Invite_me(request):
    form = InviteForm(request.POST or None)
    context = {
        "form": form,
    }

    if request.method=='POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.success(request, 'Danke für Deine Nachricht! Wir melden uns.')
            form_email = form.cleaned_data.get("email")
            form_message = form.cleaned_data.get("message")
            form_full_name = form.cleaned_data.get("full_name")
            subject = 'Ladet mich ein!'
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, 'hello@socialee.de']
            contact_message = "%s: %s via %s"%( 
                    form_full_name, 
                    form_message, 
                    form_email)
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