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

class NewsletterForm(BaseSignupForm):
    class Meta:
         fields = ('username', 'email')

    message = forms.CharField(label= _('Deine Nachricht'), required=False, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = _('Dein Name')
        self.fields['username'].required = False
        self.fields['username'].widget = forms.TextInput( 
            attrs={'placeholder': _('Name'), 'autofocus': 'autofocus'})
        self.fields['email'].label = _('Deine Email-Adresse')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div( Fieldset(
                 '',
                'username', 
                'email',
                'message'
            ), css_class="fieldWrapper"),
            Div(
            ButtonHolder(
                Submit('submit', 'Save', css_class='s-button-form self')
            ), css_class="row align-center")
        )

    def clean(self):
        super(NewsletterForm, self).clean()

        return self.cleaned_data

    def save(self, request):
        # this is copied from allauth SignupForm
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user



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
