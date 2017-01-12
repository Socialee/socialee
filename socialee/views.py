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

from ideas.models import Idea
from .models import Project, Input, Output, Profile, CommonGround, Conversation, Message
from .forms import *

from taggit.utils import parse_tags, edit_string_for_tags


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


class Styleguide(BaseView, TemplateView):
    template_name = 'styleguide.html'

    def get_context_data(self, **kwargs):
        context = super(Styleguide, self).get_context_data(**kwargs)

        return context        

# Project-Views

# CRUD CREATE PROJECT
class StartProject(BaseView, CreateView):
    template_name = 'instance_create.html'
    model = Project
    form_class = StartProjectForm

    def get(self, request, *args, **kwargs):
        super(StartProject, self).get(request, *args, **kwargs)
        form = self.form_class()
        idea = None
        if 'idea' in kwargs:
            idea = Idea.objects.get(id=kwargs['idea'])
            form = self.form_class(initial={
                'title': idea.title,
                'description': idea.description,
                        })
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form, idea=idea))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            ret = super(StartProject, self).post(request, *args, **kwargs)
            if not self.object.picture:
                idea = Idea.objects.get(id=kwargs['idea'])
                if idea.picture:
                    self.object.use_pic(idea)
            tags = form.cleaned_data['tags']
            self.object.tags.add(*tags)
            
            outputs = form.cleaned_data['socialee_outputs'].split(",")
            outputs = list(filter(None, outputs))
            for i in outputs:
                Output.objects.get_or_create(title=i.strip(), owner=request.user.current_instance)

            inputs = form.cleaned_data['socialee_inputs'].split(",")
            inputs = list(filter(None, inputs))
            for i in inputs:
                Input.objects.get_or_create(title=i.strip(), owner=request.user.current_instance)


            if 'idea' in kwargs:
               idea = Idea.objects.get(id=kwargs['idea'])
               idea.active = False
               idea.save()
            return ret
        else:
            return self.form_invalid(form)

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
    template_name = 'instance_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        return context


# CRUD UPDATE PARTICULAR PROJECT
class ProjectUpdateView(BaseView, UpdateView):
    template_name = 'instance_update.html'
    model = Project
    form_class = EditProjectForm

    def get(self, request, *args, **kwargs):
        super(ProjectUpdateView, self).get(request, *args, **kwargs)
        form = self.form_class(initial={
            'socialee_outputs': ', '.join([str(o.title) for o in self.object.socialee_output.all()]),
            'socialee_inputs': ', '.join([str(i.title) for i in self.object.socialee_input.all()])
                    }, instance=self.object)
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():

            outputs = form.cleaned_data['socialee_outputs'].split(",")
            outputs = list(filter(None, outputs))
            outputs = list(map(str.strip, outputs))
            # delete all that were removed
            Output.objects.filter(owner=self.object).exclude(title__in=outputs).delete()
            for i in outputs:
                Output.objects.get_or_create(title=i, owner=self.object)

            inputs = form.cleaned_data['socialee_inputs'].split(",")
            inputs = list(filter(None, inputs))
            inputs = list(map(str.strip, inputs))
            # delete all that were removed
            Input.objects.filter(owner=self.object).exclude(title__in=inputs).delete()
            for i in inputs:
                Input.objects.get_or_create(title=i, owner=self.object)

            return super(ProjectUpdateView, self).post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)

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



# Profile-Views

# Update Profile: User updates own profile
# Delete Profile: User deletes own profile
# Profile View: Public Profile View for other users
# Welcome View: Landing-Page for User and overview

class StartProfile(BaseView, CreateView):
    template_name = 'instance_update.html'
    model = Profile
    form_class = EditProfileForm

    def get(self, request, *args, **kwargs):
        super(StartProfile, self).get(request, *args, **kwargs)
        form = self.form_class(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'username': request.user.username
                    })
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        valid_data = super(StartProfile, self).form_valid(form)
        user.instances.update(current=False)
        form.instance.current = True
        return valid_data

    def get_context_data(self, **kwargs):
        context = super(StartProfile, self).get_context_data(**kwargs)

        return context


# Update Profile: User updates own profile
class ProfileUpdateView(BaseView, UpdateView):
    template_name = 'instance_update.html'
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
            'socialee_outputs': ', '.join([str(o.title) for o in request.user.current_instance.socialee_output.all()]),
            'socialee_inputs': ', '.join([str(i.title) for i in request.user.current_instance.socialee_input.all()])
                    }, instance=request.user.current_instance.profile)
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            #request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            #request.user.email = form.cleaned_data['email']
            request.user.save()
            
            outputs = form.cleaned_data['socialee_outputs'].split(",")
            outputs = list(filter(None, outputs))
            outputs = list(map(str.strip, outputs))
            # delete all that were removed
            Output.objects.filter(owner=self.object).exclude(title__in=outputs).delete()
            for i in outputs:
                Output.objects.get_or_create(title=i, owner=self.object)

            inputs = form.cleaned_data['socialee_inputs'].split(",")
            inputs = list(filter(None, inputs))
            inputs = list(map(str.strip, inputs))
            # delete all that were removed
            Input.objects.filter(owner=self.object).exclude(title__in=inputs).delete()
            for i in inputs:
                Input.objects.get_or_create(title=i, owner=self.object)


            return super(ProfileUpdateView, self).post(request, *args, **kwargs)
        else:
            return self.form_invalid(form)
        

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
    template_name = 'instance_view.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        follower = self.object.inst_follower.all()
        friends = None
        if self.request.user.instances.filter(current=True):
            friends = self.object.inst_follows.filter( id__in=follower ).exclude(id=self.request.user.current_instance.id)

        context['friends'] = friends

        return context


# Welcome View: Landing-Page for User and overview
class WelcomePage(ListView):
    template_name = 'welcome.html'
    model = Idea


class Follow(BaseView, CreateView):
    template_name = 'snippet_follow.html'

    def post(self, request, *args, **kwargs):
        instance_id = request.POST.get('instance_id')

        instance = CommonGround.objects.get(id=instance_id)
        if self.request.user.instances.filter(current=True):
            if instance in self.request.user.current_instance.inst_follows.all():
                self.request.user.current_instance.inst_follows.remove(instance)
            else:
                self.request.user.current_instance.inst_follows.add(instance)
        else:
            if instance in self.request.user.follows.all():
                self.request.user.follows.remove(instance)
            else:
                self.request.user.follows.add(instance)
        

        return render(request, self.template_name, {'to_follow' : instance} )



class Comment(BaseView, UpdateView):
    template_name = 'snippet_comment.html'

    def post(self, request, *args, **kwargs):
        comment = request.POST.get('comment')
        instance_id = request.POST.get('instance_id')
        reply_id = request.POST.get('reply_id')
        by_instance = None
        by_user = None

        #for notification
        actor = None
        action_object = None
        target = None
        recipient = None

        if self.request.user.instances.filter(current=True):
            by_instance = self.request.user.current_instance
            actor = by_instance.created_by
        else:
            by_user = self.request.user
            actor = by_user

        if reply_id:
            reply = Message.objects.get(id=reply_id)
            message = Message.objects.create(reply_to=reply, by_instance=by_instance, by_user=by_user, message=comment )
            action_object = message
            target = reply
        else:
            instance = CommonGround.objects.get(id=instance_id)
            conv, created = Conversation.objects.get_or_create(slug=instance.slug)
            if created:
                instance.conversation = conv
                instance.save()
            message = Message.objects.create(conversation=conv, by_instance=by_instance, by_user=by_user, message=comment )
            action_object = message
            target = instance

        action.send(actor, action_object=instance, target=instance, verb='posted', description=comment, recipient=recipient)

        return render(request, self.template_name, {'comment' : message} )

class ActAs(BaseView, UpdateView):

    def post(self, request, *args, **kwargs):
        instance_slug = request.POST.get('instance_slug')
        self.request.user.instances.update(current=False)

        if self.request.user.instances.filter(slug=instance_slug):
            instance = self.request.user.instances.get(slug=instance_slug)
            instance.current = True
            instance.save()
            instance_slug = instance.short_name()
        else:
            if request.user.first_name:
                instance_slug =  request.user.first_name
            else:
                instance_slug = request.user.email

        return HttpResponse(instance_slug)
