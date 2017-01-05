from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *

from django import forms
from .models import Project, Profile, Input, Output, User
from django.utils.safestring import mark_safe


from taggit.forms import TagWidget


class StartProjectForm(forms.ModelForm):
    fields = ('title', 'tagline', 'description', 'picture', 'tags')
    socialee_outputs = forms.CharField(required=False)
    socialee_inputs = forms.CharField(required=False)
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description', 'picture', 'tags')
        labels = {
            'title': _('Titel des Projektes'),
            'tagline': _('Motto, Slogan oder Tagline'),
            'tags': _('Beschreibe dein Projekt mit ein paar Schlagworten'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': ''}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Das soziale Netzwerk für Ideen und Projekte'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': TagWidget(attrs={'placeholder': 'Berliner Ökohipster, vegane Sojalatte'}),
        }

class EditProjectForm(forms.ModelForm):
    socialee_outputs = forms.CharField(required=False, label='Was bietet das Projekt?')
    socialee_inputs = forms.CharField(required=False, label='Was benötigt das Projekt?')
    class Meta:
        model = Project
        fields = ['picture', 'title', 'tagline', 'tags', 'location', 'description', 'video', 'longdescription', 'history', ]
        labels = {
            'title': _('Titel'),
            'tagline': _('Motto, Slogan oder Tagline'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Socialee'}),
            'tagline': forms.TextInput(attrs={'placeholder': 'Das soziale Netzwerk für Ideen und Projekte'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': TagWidget(attrs={'placeholder': 'Eine durch Komma getrennte Schlagwortliste.'}),
        }


class EditProfileForm(forms.ModelForm):
    model = Profile
    fields = ('tagline', 'description', 'picture', 'phone', 'plz', 'newsletter', 'tags')
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
            'tags': TagWidget(attrs={'placeholder': 'Eine durch Komma getrennte Schlagwortliste.'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class SocialeeLoginForm(LoginForm): # Changing labels of default Allauth Login Form (note ACCOUNT_FORMS in settings.py)
    
    def __init__(self, *args, **kwargs):
        super(SocialeeLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'placeholder': ""})
        self.fields['login'].label = "E-Mail-Adresse"
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': mark_safe("***")})
        self.fields['password'].label = "Passwort"
