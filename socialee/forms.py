from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from django import forms
from .models import Project, Profile, UserEntry, Input, Output, Invite


# class QuoteForm(forms.ModelForm):
#     class Meta:
#         model = Quote
#         fields = ('title', 'author')


class StartProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')
    

class MyLoginForm(LoginForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('full_name', 'email', 'message')
        labels = {
            'full_name': _('Vor- & Nachname (freiwillig)'),
            'email': _('Deine Email-Adresse'),
            'message': _('Erzähl uns was! (freiwillig)'),
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Peter oder Petra Musterfraumann?'}),
            'email': forms.TextInput(attrs={'placeholder': 'Deine Email-Adresse ist bei uns sicher.'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Erzähl uns, wie Du von Socialee gehört hast und warum Du dabei sein möchtest. Wenn Du sogar schon eine Projektidee hast, erzähle uns davon! Wir lieben Ideen.'}),
        }
        # help_texts = {
        #     'full_name': _('Some useful help text.'),
        # }