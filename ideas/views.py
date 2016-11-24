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
            email = form.cleaned_data.get('email')
            user = request.user
            if not email:
                try:
                    email = request.user.email
                except:
                    email = "Anonym"

            message_to_us = _("Es gibt eine neue Idee auf Socialee.\n\nTitel: %(title)s\nBeschreibung: %(description)s\n\nvon Email-Adresse: %(email)s\n\n")\
            % {'title': str(title),
            'description': str(description),
            'email': str(email),
            }
            if settings.PROD:
                send_mail(
                    'Neue Idee auf Socialee!',
                    message_to_us,
                    settings.SERVER_EMAIL,
                    ['team@socialee.de',],
                    fail_silently=False,
                )
            message_to_them = _("Danke für deine Idee! Wir gucken sie uns an. Das dauert nicht länger als einen Tag.")
            if not email == "Anonym":
                send_mail(
                    'Deine Idee auf Socialee!',
                    message_to_them,
                    settings.SERVER_EMAIL,
                    [email,],
                    fail_silently=False,
                )
            if not email and hasattr(request.user, 'email'):
                email = request.user.email
            ret = super(CreateIdea, self).post(request, *args, **kwargs)
            if pic or title or description:
                messages.success(request, 'Danke! Wir gucken uns Deine Idee an und veröffentlichen sie so schnell wie möglich.')
                newIdea = Idea.objects.create( picture = pic, title = title, description = description, author=email )
                newIdea.save()
            else:
                return self.form_invalid(form)
            return ret
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateIdea, self).get_context_data(**kwargs)
        context['ideas_count'] = Idea.objects.all().count()
        return context



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







