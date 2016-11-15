from allauth.account.forms import *
from collections import OrderedDict
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _ 
from register.forms import *


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


class NewsletterForm(EmailRegisterForm):

    first_name = forms.CharField( required=False, widget = forms.TextInput( 
            attrs={ 'autofocus': 'autofocus'}))
    message = forms.CharField( required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5, 'style':'resize: none;'}))
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('Deine Email-Adresse')
        self.fields['email'].help_text = _('Das brauchen wir')

        fields_key_order = ['first_name', 'email', 'message', 'newsletter']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

        self.fields['first_name'].label = _('Vor & Nachname')
        self.fields['message'].label = _("Möchtest Du sonst noch was loswerden?<br class='show-for-medium'/> Dies ist die Gelegenheit.")

        self.fields['first_name'].help_text = _('Wenn Du magst')
        self.fields['message'].help_text = _('Wenn Du magst')

    def custom_signup(self, request, user):
        request.session["message_register"] = True
        return super(NewsletterForm, self).custom_signup(request, user)
