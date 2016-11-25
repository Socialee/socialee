from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from django.utils.translation import ugettext_lazy as _ 


class AdvancedMailAccountAdapter(DefaultAccountAdapter):

    error_messages = {
        'email_taken':
        _("Es gibt schon jemand mit dieser Email"),
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
        # all infos stored in the session can be used in the email template
        if user.email:
            # give ths user the temp password to send to the user
            password = User.objects.make_random_password()
            user.set_password(password)
            request.session["pass"] = password

        request.session["email_register"] = True
        newsletter = form.cleaned_data.get("newsletter")
        if newsletter:
            newsletter_group, created = Group.objects.get_or_create(name='signed_up_for_newsletter')
            user.groups.add(newsletter_group)
            request.session["newsletter"] = True

        if user.first_name:
            # try to get the last name out of the field
            names = user.first_name.split(" ")
            if len(names)>1:
                user.last_name = names[-1]
                user.first_name = " ".join(names[:-1])

        if user.email:
            user.save()

    def respond_email_verification_sent(self, request, user):
        if user.email:
            return HttpResponseRedirect(reverse('account_email_verification_sent'))
        else:
            return HttpResponseRedirect(reverse('idea_list'))