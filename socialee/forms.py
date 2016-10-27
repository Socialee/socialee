from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *

from django import forms
from .models import Project, Profile, Input, Output, User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *

from taggit.forms import TagWidget


class StartProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline')
        labels = {
            'title': _('Projekttitel'),
            'tagline': _('Untertitel'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Socialee'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Das soziale Netzwerk für Ideen und Projekte'}),
        }

class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description', 'tags')
        labels = {
            'title': _('Gib deiner Idee einen Namen...'),
            'tagline': _('... und einen Untertitel.'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Socialee'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Das soziale Netzwerk für Ideen und Projekte'}),
        }


class EditProfileForm(forms.ModelForm):
    model = Profile
    fields = ('tagline', 'description', 'picture', 'phone', 'plz', 'newsletter', 'tags')
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    socialee_outputs = forms.CharField(required=False)
    socialee_inputs = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Profile
        fields = ('tagline', 'description', 'picture', 'phone', 'plz', 'newsletter', 'tags')
        widgets = {
            'tags': TagWidget(),
        }


# class InviteForm(forms.ModelForm):
#     class Meta:
#         model = Invite
#         fields = ('full_name', 'email', 'message')
#         labels = {
#             'full_name': _('Vor- & Nachname'),
#             'email': _('Deine Email-Adresse'),
#             'message': _('Deine Nachricht'),
#         }
#         widgets = {
#             'full_name': forms.TextInput(attrs={'placeholder': ''}),
#             'email': forms.TextInput(attrs={'placeholder': ''}),
#             'message': forms.Textarea(
#                 attrs={'placeholder': ''}),
#         }


class SocialeeLoginForm(LoginForm): # Changing labels of default Allauth Login Form (note ACCOUNT_FORMS in settings.py)
    def __init__(self, *args, **kwargs):
        super(SocialeeLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'tri tra trullala'})
    password = PasswordField(label=_("Dein Passwort"))
