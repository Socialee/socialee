from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class AdvancedMailAccountAdapter(DefaultAccountAdapter):
    
    def send_mail(self, template_prefix, email, context):
        if self.request.session["idea_signup"]:
            context["pass"] = self.request.session["pass"]
            context["idea_signup"] = True
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