from django import forms
from register.forms import *
from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _ 


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
