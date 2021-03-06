from allauth.account.views import SignupView

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView, DetailView, TemplateView, ListView
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allauth.utils import build_absolute_uri

from .forms import *
from .models import Idea, Comment
from socialee.models import Message


class CreateIdea(SignupView):
    template_name = 'create_idea.html'
    form_class = IdeaForm
    success_url = reverse_lazy('idea_list')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        title = context.get('title')
        description = context.get('description')

        if 'message' in kwargs:
            message = Message.objects.get(id=kwargs['message'])
            description = message.message
        form = self.form_class(initial={
                'title': title,
                'description': description,
                        })
        old_reload = context.get('reload')
        super(CreateIdea, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data( form=form, reload=old_reload ))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            pic = None
            if len(request.FILES) != 0:
                pic = request.FILES['picture']
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            private = form.cleaned_data.get('private')

            ret = super(CreateIdea, self).post(request, *args, **kwargs)

            if pic or title or description:
                email = form.cleaned_data.get('email')
                authorUser = None
                if not email:
                    email = 'Anonym'

                if hasattr(request.user, 'email'):
                    email = request.user.email

                
                newIdea = Idea.objects.create( picture = pic, title = title, description = description, author=email, authorUser=authorUser, private=private )

                allert = 'Wieder eine gute, Deine Idee.'
                # check if we have a valid email to send to
                if not email == 'Anonym':
                    self.send_mail_to_creator(email=email, context={'idea_url':build_absolute_uri(request, newIdea.get_absolute_url())})
                    authorUser = User.objects.get(email=email)
                    allert += ' Check mal dein E-Mail-Postfach!'

                if settings.PROD:
                    self.send_mail_to_us(title, description, email)
                # set message to inform user it was successful
                messages.success(request, allert)
            else:
                return self.form_invalid(form)
            return ret
        else:
            if form.has_error('email', code='email_taken'):
                request.session['reload'] = 'true'
                request.session['title'] = form.data['title']
                request.session['description'] = form.data['description']
                request.session['private'] = form.data['private']
                # request.session['picturefile'] = form.data['picturefile']
                return self.response_for_email_taken(request, form=form, login=form.data['email'])
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateIdea, self).get_context_data(**kwargs)
        context['ideas_count'] = Idea.objects.all().count()
        if 'reload' in self.request.session:
            context['reload'] = self.request.session.pop('reload')
            if 'title' in self.request.session:
                context['title'] = self.request.session.pop('title')
            if 'description' in self.request.session:
                context['description'] = self.request.session.pop('description')
            if 'picturefile' in self.request.session:
                context['picturefile'] = self.request.session.pop('picturefile')
            if 'private' in self.request.session:
                context['private'] = self.request.session.pop('private')
        return context


    def send_mail_to_creator(self, email, context):
        message_to_them = render_to_string('email/email_thank_you_idea.txt', context=context)
        send_mail(
            'Deine Idee auf Socialee!',
            message_to_them,
            settings.SERVER_EMAIL,
            [email,],
            fail_silently=True,
        )

    def send_mail_to_us(self, title, description, email):
        context = {'title': str(title), 'description': str(description), 'email': str(email)}
        message_to_us = render_to_string('email/email_new_idea.txt', context)
        send_mail(
            'Neue Idee auf Socialee!',
            message_to_us,
            settings.SERVER_EMAIL,
            ['team@socialee.de',],
            fail_silently=True,
        )

    @method_decorator(login_required)
    def response_for_email_taken(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(args, kwargs))


class IdeaListView(ListView):
    template_name = 'idea_list.html'
    context_object_name = 'idea_list'
    # model = Idea
    queryset = Idea.objects.filter(enabled=True, private=False)



class Like(TemplateView):
    template_name = 'idea_card.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        idea_id = request.POST.get('idea_id')

        instance = Idea.objects.get(id=idea_id)
        
        if self.request.user.is_authenticated():
            if self.request.user in instance.likes.all():
                instance.likes.remove(self.request.user)
            else:
                instance.likes.add(self.request.user)

        return render(request, self.template_name, {'idea' : instance } )


class Commentate(TemplateView):
    template_name = 'snippet_ideas_comment.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        idea_id = request.POST.get('idea_id')
        comment = request.POST.get('comment')
        comment_obj= None

        instance = Idea.objects.get(id=idea_id)
        
        if request.user.is_authenticated():
            comment_obj = Comment.objects.create(to_idea=instance, by_user=self.request.user, message=comment)
            if instance.author and instance.author != 'Anonym':
                context = {
                    'object_title': 'Deine Idee',
                    'comment': comment_obj, 
                    'object': instance,
                    'object_dat' : 'Deiner Idee',
                    'object_url': build_absolute_uri(request, instance.get_absolute_url()) }
                self.send_mail_to_creator(email=instance.author, context=context)

        return render(request, self.template_name, {'comment' : comment_obj, 'idea': instance } )

    def send_mail_to_creator(self, email, context):
        message_to_creator = render_to_string('email/email_new_comment.txt', context=context)
        send_mail(
            'Deine Idee auf Socialee!',
            message_to_creator,
            settings.SERVER_EMAIL,
            [email,],
            fail_silently=True,
        )


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea_detail.html'


class IdeaEditView(UpdateView):
    template_name = 'edit_idea.html'
    model = Idea
    # fields = ['picture', 'title', 'description', 'private']
    form_class = IdeaEditForm

    def get_success_url(self):
        slug = self.request.user
        return reverse('welcome', kwargs={'slug': slug})


class IdeaDeleteView(DeleteView):
    model = Idea
    template_name = 'idea_confirm_delete.html'

    def get_success_url(self):
        slug = self.request.user
        return reverse('welcome', kwargs={'slug': slug})

