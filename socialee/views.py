import os, random
import requests
import random

from allauth.account.views import RedirectAuthenticatedUserMixin

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

from .models import Project, Input, Output, Profile, CommonGround, Conversation, Message
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
class ProjectView(BaseView, DetailView):
    template_name = 'project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)

        return context


# CRUD UPDATE PARTICULAR PROJECT
class ProjectUpdateView(BaseView, UpdateView):
    template_name = 'project_update.html'
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


class Comment(BaseView, CreateView):
    template_name = 'comment.html'

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        common_id = request.POST.get('common_id')
        reply_id = request.POST.get('reply_id')

        if reply_id:
            reply = Message.objects.get(id=reply_id)
        else:
            common = CommonGround.objects.get(id=common_id)
            conv, created = Conversation.objects.get_or_create(slug=common.slug)
            if created:
                common.conversation = conv
                common.save()
        message = Message.objects.create(conversation=conv, by_user=request.user, message=comment )
        message.save()
            

        return render(request, self.template_name, {'comment' : message} )

# Profile-Views

# Update Profile: User updates own profile
# Delete Profile: User deletes own profile
# Profile View: Public Profile View for other users
# Welcome View: Landing-Page for User and overview


# Update Profile: User updates own profile
class ProfileUpdateView(BaseView, UpdateView):
    template_name = 'profile_update.html'
    model = Profile
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



class ProfileView(BaseView, DetailView):
    template_name = 'profile_view.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        #context['user_project_list'] = Project.objects.filter(created_by=context["profile"].user)
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
