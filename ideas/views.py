from allauth.account.views import SignupView

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView, DetailView
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Idea, Comment


class CreateIdea(SignupView):
    template_name = 'create_idea.html'
    form_class = IdeaForm
    success_url = reverse_lazy('idea_list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            pic = None
            if len(request.FILES) != 0:
                pic = request.FILES['picture']
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            ret = super(CreateIdea, self).post(request, *args, **kwargs)

            if pic or title or description:
                email = form.cleaned_data.get('email', 'Anonym')

                if hasattr(request.user, 'email'):
                    email = request.user.email

                # check if we have a valid email to send to
                if not email == 'Anonym':
                    self.send_mail_to_creator(email)

                if settings.PROD:
                    self.send_mail_to_us(title, description, email)
                
                newIdea = Idea.objects.create( picture = pic, title = title, description = description, author=email )
                newIdea.save()

                # set message to inform user it was successful
                messages.success(request, 'Danke! Wir gucken uns Deine Idee an und veröffentlichen sie so schnell wie möglich.')
            else:
                return self.form_invalid(form)
            return ret
        else:
            if form.has_error('email', code='email_taken'):
                request.session['reload'] = 'true'
                request.session['title'] = form.data['title']
                request.session['description'] = form.data['description']
                request.session['picturefile'] = form.data['picturefile']
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
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = self.form_class(initial={
                'title': context.get('title'),
                'description': context.get('description'),
                'picturefile': context.get('picturefile')
                        })
        old_reload = context.get('reload')
        super(CreateIdea, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data( form=form, reload=old_reload ))

    def send_mail_to_creator(self, email):
        message_to_them = render_to_string('email/email_thank_you_idea.txt')
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


def idea_list(request):
    context = {
    }
    
    return render(request, "idea_list.html", context)


class Like(UpdateView):
    template_name = 'idea_card.html'

    def post(self, request, *args, **kwargs):
        idea_id = request.POST.get('idea_id')

        instance = Idea.objects.get(id=idea_id)
        comment = True;
        
        if self.request.user in instance.likes.all():
            comment = False
            instance.likes.remove(self.request.user)
        else:
            instance.likes.add(self.request.user)

        return render(request, self.template_name, {'idea' : instance, 'do_comment' : comment } )


class Commentate(UpdateView):
    template_name = 'idea_card.html'

    def post(self, request, *args, **kwargs):
        idea_id = request.POST.get('idea_id')
        comment = request.POST.get('comment')

        instance = Idea.objects.get(id=idea_id)
        
        Comment.objects.create(to_idea=instance, by_user=self.request.user, message=comment)
        
        return render(request, self.template_name, {'idea' : instance } )


class IdeaDetailView(DetailView):
    model = Idea
    template_name = 'idea_detail.html'

class IdeaEditView(UpdateView):
    template_name = 'edit_idea.html'
    model = Idea
    fields = ['picture', 'title', 'description']
    def get_success_url(self):
        slug = self.request.user
        return reverse('welcome', kwargs={'slug': slug})






