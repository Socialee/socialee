from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *

from django import forms
from .models import Project, Profile, UserEntry, Input, Output, Invite, User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *


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
    fields = ('picture', 'phone', 'plz', 'newsletter')
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Ändere hier Dein Profil.',
                'username', 'email', 'first_name', 'last_name',
                'picture',
                'phone',
                'plz',
                'newsletter'

            ),
            ButtonHolder(
                Submit('submit', 'Save')
            )
        )
    class Meta:
        model = Profile
        #fields = '__all__'
        fields = ('picture', 'phone', 'plz', 'newsletter')


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ('full_name', 'email', 'message')
        labels = {
            'full_name': _('Wenn Du Lust hast: Vor- & Nachname'),
            'email': _('Muss sein: Deine Email-Adresse'),
            'message': _('Wenn Du Lust hast: Was würdest Du tun, wenn Du wüsstest, Du könntest nicht scheitern?'),
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Peter oder Petra?'}),
            'email': forms.TextInput(attrs={'placeholder': 'Wir sind die Guten, Deine Email-Adresse ist bei uns sicher. Und alles andere auch.'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Schwierige Frage? Na, Du kannst auch was anderes schreiben.\n\nErzähl und doch, wie Du von Socialee gehört hast und warum Du dabei sein möchtest. Oder wenn Du sogar schon eine Projektidee hast, erzähle uns davon! Wir lesen das wirklich. Und vielleicht sind wir ja begeistert und machen dann was zusammen!'}),
        }


class SocialeeLoginForm(LoginForm): # Changing labels of default Allauth Login Form (note ACCOUNT_FORMS in settings.py)
    def __init__(self, *args, **kwargs):
        super(SocialeeLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'tri tra trullala'})
    password = PasswordField(label=_("Dein Passwort"))
