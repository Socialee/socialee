from allauth.account.forms import LoginForm

from django.utils.translation import ugettext_lazy as _

from allauth.account.forms import *

from django import forms
# from .models import Project, Profile, Input, Output, User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *



class NewsletterForm(BaseSignupForm):

    class Meta:
         fields = ('email')

    first_name = forms.CharField(label= _('Vor & Nachname'), required=False, widget = forms.TextInput( 
            attrs={ 'autofocus': 'autofocus'}))
    message = forms.CharField(label= _("Möchtest Du sonst noch was loswerden?<br class='show-for-medium'/> Dies ist die Gelegenheit."), required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5, 'style':'resize: none;'}))
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = _('Deine Email-Adresse')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div( Fieldset(
                 '',
                'first_name', 
                'email',
                'message'
            ), css_class="fieldWrapper"),
            Div(
            ButtonHolder(
                Submit('submit', 'Ich will dabei sein', css_class='s-button-form self')
            ), css_class="row align-center")
        )
        self.helper.field_template = 'field.html'

    def clean(self):
        super(NewsletterForm, self).clean()

        return self.cleaned_data

    def custom_signup(self, request, user):
        if user.first_name:
            names = user.first_name.split(" ")
            if len(names)>1:
                user.last_name = names[-1]
                user.first_name = " ".join(names[:-1])
                user.save()
        return super(NewsletterForm, self).custom_signup(request, user)

    def save(self, request):
        # this is copied from allauth SignupForm
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user
