import os, random
import requests
import random
import mailchimp

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
from django.dispatch import receiver


from allauth.account.views import *
from allauth.account.forms import *
from allauth.account.decorators import verified_email_required
from allauth.account.signals import email_confirmed

from .models import Project, Input, Output, Profile
from .forms import *

User = get_user_model()

# Overwrite/disable dispatch method of RedirectAuthenticatedUserMixin (endless redirect on /).
def dispatch_no_redirect(self, request, *args, **kwargs):
    return super(RedirectAuthenticatedUserMixin, self).dispatch(request, *args, **kwargs)
RedirectAuthenticatedUserMixin.dispatch = dispatch_no_redirect


# General-Views

class BaseView:
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)

        return context


class Home(BaseView, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        # make sure the profile exists
        if self.request.user.is_authenticated():
            self.request.user.profile

        return context


class NewsletterSignup(SignupView):
    form_class = NewsletterForm
    template_name = 'invite_me.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #TODO fix naming let the user type in any name
        # unique username 
        # do this in  is_valid function?
        if form.is_valid():
            ret = super(NewsletterSignup, self).post(request, *args, **kwargs)
            raw_email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            name = form.cleaned_data.get("first_name")
            names = name.split(" ")
            msg = 'Danke'
            if message:
                msg += ' für Deine Nachricht'
            if name:
                msg += ', '+names[0].capitalize()
            msg +='! Wir halten Dich auf dem laufenden.'

            messages.success(request, msg)

            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, 'hello@socialee.de']


            # send the email
            subject = 'Ladet mich ein!'
            contact_message = "%s via %s schreibt:\n\n %s"%( 
                    name, 
                    raw_email,
                    message)
            some_html_message = """
            <h1>Hallo Mo!</h1>
            """
            send_mail(subject, 
                    contact_message, 
                    from_email, 
                    to_email,
                    fail_silently=True)
            return ret

        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(NewsletterSignup, self).get_context_data(**kwargs)

        return context


#mailchimp stuff
MAILCHIMP_API_KEY = '115737b5c3cf0d9a848011ab122b5c7f-us9'
MAILCHIMP_LIST_ID = 'c5c441594e'

@receiver(email_confirmed, dispatch_uid="socialee.allauth.email_confirmed")
def email_confirmed_(email_address, **kwargs):
    # try to add user to mailchimp

    #TODO fix naming
            
    email = {'email': email_address.email}

    fname = email_address.user.first_name
    lname = email_address.user.last_name

    merge_vars = {
        'FNAME': fname,
        'LNAME': lname,
        }

    m = mailchimp.Mailchimp(MAILCHIMP_API_KEY)

    from_email = settings.EMAIL_HOST_USER
    to_email = [from_email, 'hello@socialee.de']

    try:
        m.lists.subscribe(id=MAILCHIMP_LIST_ID, email=email, merge_vars=merge_vars, double_optin=False)
    #This is the worst error handling ever
    except mailchimp.Error as e:
        send_mail("Faild to sign up -> mailchimp", 
            "%s via %s \n%s"%( 
            "name", 
            email,
            e
            ), 
            from_email, 
            to_email,
            fail_silently=True)


class Impressum(BaseView, TemplateView):
    template_name = 'impressum.html'

    def get_context_data(self, **kwargs):
        context = super(Impressum, self).get_context_data(**kwargs)

        return context        

# Project-Views

# CRUD CREATE PROJECT
class StartProject(BaseView, CreateView):
    template_name = 'start_project.html'
    model = Project
    form_class = StartProjectForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        valid_data = super(StartProject, self).form_valid(form)
        form.instance.managers.add(user)
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
    template_name = 'project_view.html'
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
        user = self.request.user # erfragt den derzeitigen user
        obj = super(ProjectUpdateView, self).get_object(*args, **kwargs)
        if obj.created_by == user or user in obj.managers.all():
            return obj
        else:
            raise Http404



class Socialeebhaber(BaseView, UpdateView):
    template_name = 'project_card_element.html'

    def post(self, request, *args, **kwargs):
        project_id = request.POST.get('project_id')

        project = Project.objects.get(id=project_id)
        if project in request.user.profile.liked_projects.all():
            request.user.profile.liked_projects.remove(project)
            project.profiles.remove(request.user)
        else:
            project.profiles.add(request.user)
            request.user.profile.liked_projects.add(project)

            

        return render(request, self.template_name, {'project' : project} )



# Profile-Views

# Update Profile: User updates own profile
# Retrieve Profile: User watches detail-view of own profile or profile of others
# Delete Profile: User deletes own profile
# Profile View: Public Profile View for other users
# Welcome View: Landing-Page for User and overview


# Update Profile: User updates own profile
class ProfileUpdateView(BaseView, UpdateView):
    template_name = 'user_profile_update.html'
    model = Profile
    # form_class = EditProfileForm
    form_class = EditProfileForm

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        super(ProfileUpdateView, self).get(request, *args, **kwargs)
        form = self.form_class(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username
                    }, instance=request.user.profile)
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)

        request.user.username = request.POST['username']
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.email = request.POST['email']
        request.user.save()

        return super(ProfileUpdateView, self).post(request, *args, **kwargs)
        

    def get_success_url(self):
        return reverse('profile_view', kwargs = {"slug": self.request.user.profile.slug})

    # Nur der Admin und die Manager des Projektes kann Änderungen vornehmen
    # def get_object(self, *args, **kwargs):
    #     user = self.request.user # erfragt den derzeitigen user
    #     obj = super(ProfileUpdateView, self).get_object(*args, **kwargs)
    #     if obj.created_by == user or user in obj.managers.all():
    #         return obj
    #     else:
    #         raise Http404



# Retrieve Profile: User watches detail-view of own profile or profile of others
class ProfileDetailView(BaseView, DetailView):
    template_name = 'user_profile_detail.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)

        return context


class ProfileView(BaseView, DetailView):
    template_name = 'profile_view.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_project_list'] = Project.objects.filter(created_by=context["profile"].user)

        return context


# Welcome View: Landing-Page for User and overview
class WelcomePage(BaseView, ListView):
    template_name = 'welcome.html'
    model = Project

    def get_context_data(self, **kwargs):
        # make sure the profile exists
        if self.request.user.is_authenticated():
            self.request.user.profile
        context = super(WelcomePage, self).get_context_data(**kwargs)
        context['user_project_list'] = Project.objects.filter(created_by=self.request.user)

        return context
