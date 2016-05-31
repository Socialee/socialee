from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *

from django import forms
from .models import Project, Profile, UserEntry, Input, Output, Invite

from crispy_forms.helper import FormHelper


class StartProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')
        labels = {
            'title': _('Projekttitel'),
            'tagline': _('Untertitel'),
            'description': _('Beschreibung'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Socialee'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Das soziale Netzwerk für Ideen und Projekte'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Beschreibe dein Projekt oder Deine Idee. Du kannst diese Sachen später jederzeit ändern.'}),
        }


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