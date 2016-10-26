from django import forms

from collections import OrderedDict

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *
from django.contrib.auth.models import User, Group


class EmailRegisterForm(BaseSignupForm):

    class Meta:
         fields = ('email')

    newsletter = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super(EmailRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('Deine Email-Adresse')

    def clean(self):
        super(EmailRegisterForm, self).clean()

        return self.cleaned_data

    def custom_signup(self, request, user):
        if user.email:
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            request.session["pass"] = password
        request.session["email_register"] = True
        newsletter = self.cleaned_data.get("newsletter")
        if newsletter:
            newsletter_group, created = Group.objects.get_or_create(name='signed_up_for_newsletter')
            user.groups.add(newsletter_group)
            request.session["newsletter"] = True
        if user.first_name:
            names = user.first_name.split(" ")
            if len(names)>1:
                user.last_name = names[-1]
                user.first_name = " ".join(names[:-1])
                user.save()
        return super(EmailRegisterForm, self).custom_signup(request, user)

    def save(self, request):
        # this is copied from allauth SignupForm
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user