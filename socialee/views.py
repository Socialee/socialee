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
        if self.object.created_by == self.request.user:
            self.request.user.instances.update(current=False)
            self.object.current = True
            self.object.save()

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



# class Socialeebhaber(BaseView, UpdateView):
#     template_name = 'project_card_element.html'

#     def post(self, request, *args, **kwargs):
#         project_id = request.POST.get('project_id')

#         project = Project.objects.get(id=project_id)
#         if project in request.user.profile.liked_projects.all():
#             request.user.profile.liked_projects.remove(project)
#             project.profiles.remove(request.user)
#         else:
#             project.profiles.add(request.user)
#             request.user.profile.liked_projects.add(project)

            

#         return render(request, self.template_name, {'project' : project} )


class Follow(BaseView, CreateView):
    template_name = 'follow.html'

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id')

        instance = CommonGround.objects.get(id=instance_id)
        if hasattr(instance, 'profile'):
            instance = Profile.objects.get(id=instance_id)
            if instance in self.request.user.current_instance.follows_profiles.all():
                self.request.user.current_instance.follows_profiles.remove(instance)
            else:
                self.request.user.current_instance.follows_profiles.add(instance)
        elif hasattr(self, 'project'):
            instance = Project.objects.get(id=instance_id)
            if instance in self.request.user.current_instance.follows_projects.all():
                self.request.user.current_instance.follows_profiles.remove(instance)
            else:
                self.request.user.current_instance.follows_projects.add(instance)

        return render(request, self.template_name, {'to_follow' : instance} )

class Comment(BaseView, UpdateView):
    template_name = 'follow.html'

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
        instance = self.request.user.current_instance
        message = Message.objects.create(conversation=conv, by_instance=instance, message=comment )
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
                    }, instance=request.user.current_instance)
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
        return reverse('profile_view', kwargs = {"slug": self.request.user.current_instance.slug})

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
        print(context)

        if self.object.created_by == self.request.user:
            self.request.user.instances.update(current=False)
            self.object.current = True
            self.object.save()
        return context

    # this should go once we can create profiles and projects
    def get(self, request, *args, **kwargs):
        try:
            return super(ProfileView, self).get(request, *args, **kwargs)
        except:
            self.object = Profile.objects.create(created_by=self.request.user)
            return self.render_to_response(self.get_context_data(
                object=self.object))




# Welcome View: Landing-Page for User and overview
class WelcomePage(BaseView, ListView):
    template_name = 'welcome.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)
        if self.request.user.instances.count() and not self.request.user.instances.filter(current=True):
            instance = self.request.user.instances[0]
            instance.current = True
            instance.save()

        return context
