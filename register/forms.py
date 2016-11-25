from allauth.account.forms import *
from collections import OrderedDict
from django import forms
from django.utils.translation import ugettext_lazy as _ 
from register.forms import *


class EmailRegisterForm(SignupForm):

    class Meta:
         fields = ('email')

    newsletter = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        super(EmailRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('E-Mail-Adresse')


class NewsletterForm(EmailRegisterForm):

    first_name = forms.CharField( required=False, widget = forms.TextInput( 
            attrs={ 'autofocus': 'autofocus'}))
    message = forms.CharField( required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5, 'style':'resize: none;'}))
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        fields_key_order = ['first_name', 'email', 'message', 'newsletter']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

        self.fields['email'].label = _('E-Mail-Adresse')
        self.fields['email'].help_text = _('Das brauchen wir')
        self.fields['email'].widget = forms.TextInput(attrs={'placeholder': ""})

        self.fields['first_name'].label = _('Vor- & Nachname')
        self.fields['first_name'].help_text = _('Wenn Du magst')

        self.fields['message'].label = _("Möchtest Du sonst noch was loswerden? Dies ist die Gelegenheit.")
        self.fields['message'].help_text = _('Wenn Du magst')

        self.fields['newsletter'].label = _('Newsletter abonnieren')

    def custom_signup(self, request, user):
        request.session["message_register"] = True
        return super(NewsletterForm, self).custom_signup(request, user)
