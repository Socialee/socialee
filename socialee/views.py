import os, random
import requests
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, UpdateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin


from allauth.account.views import *
from allauth.account.forms import *
from allauth.account.decorators import verified_email_required

from .models import Project, Input, Output
from .forms import *
from quotes.models import Quote

from .utils.multiform import MultiFormsView



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


# CRUD CREATE PROJECT
class StartProject(BaseView, CreateView):
    template_name = 'start_project.html'
    model = Project
    form_class = StartProjectForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super(StartProject, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(StartProject, self).get_context_data(**kwargs)

        return context


# CRUD RETRIEVE PROJECT
class ProjectOverview(BaseView, ListView):
    template_name = 'project_overview.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectOverview, self).get_context_data(**kwargs)

        return context


class ProjectDetailView(BaseView, DetailView):
    template_name = 'project_template.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        return context


class UserProfile(MultiFormsView):
    template_name = 'user_profile.html'
    form_classes = {
        'change': ChangePasswordForm,
        }
    success_url = reverse_lazy("user_profile")

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['test'] = "testing"

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
            contact_message = "%s via %s:\n%s"%( 
                    form_full_name, 
                    form_email,
                    form_message, 
                    )
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