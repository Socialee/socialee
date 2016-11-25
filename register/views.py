import mailchimp

from django.contrib.auth.models import Group
from allauth.account.decorators import verified_email_required
from allauth.account.signals import email_confirmed
from allauth.account.views import SignupView, PasswordChangeView
from django.dispatch import receiver
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from .forms import *

class HomePasswordChangeView(PasswordChangeView):
    """
    Custom class to override the password change view to redirect to "/" 
    """

    success_url = "/"

password_change = HomePasswordChangeView.as_view()


class NewsletterSignup(SignupView):

    form_class = NewsletterForm
    template_name = 'register.html'

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
            # msg = 'Danke'
            # if message:
            #     msg += ' für Deine Nachricht'
            # if name:
            #     msg += ', '+names[0].capitalize()
            # msg +='! Wir freuen uns über dein Interesse.'

            # messages.success(request, msg)

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

    if email_address.user.groups.filter(name='signed_up_for_newsletter').exists():
            
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

        e = None # used for malichimp error handling, has to be assigned before being called

        try:
            m.lists.subscribe(id=MAILCHIMP_LIST_ID, email=email, merge_vars=merge_vars, double_optin=False)
            send_mail("Sign up -> mailchimp", 
                "%s via %s \n%s"%( 
                "name", 
                email,
                e
                ), 
                from_email, 
                to_email,
                fail_silently=True)
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