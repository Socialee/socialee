from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _ 


class AdvancedMailAccountAdapter(DefaultAccountAdapter):

    error_messages = {
        'email_taken':
        _("Es gibt schon jemand mit dieser email"),
    }
    
    def send_mail(self, template_prefix, email, context):
        if 'email_register' in self.request.session:
            self.request.session.pop('email_register')
            context["email_register"] = True
        if 'idea_register' in self.request.session:
            self.request.session.pop('idea_register')
            context["idea_register"] = True
        if 'message_register' in self.request.session:
            self.request.session.pop('message_register')
            context["message_register"] = True
        context["pass"] = self.request.session.pop('pass')
        msg = self.render_mail(template_prefix, email, context)
        msg.send()

    def save_user(self, request, user, form, commit=True):
        super(AdvancedMailAccountAdapter, self).save_user(request, user, form, False)
        if user.email:
            user.save()

    def respond_email_verification_sent(self, request, user):
        if user.email:
            return HttpResponseRedirect(reverse('account_email_verification_sent'))
        else:
            return HttpResponseRedirect(reverse('idea_list'))