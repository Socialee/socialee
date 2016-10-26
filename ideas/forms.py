from collections import OrderedDict
from django import forms
from django.utils.translation import ugettext_lazy as _	
from allauth.account.forms import *
from .models import Idea, User
from django.conf import settings
from django.core.mail import send_mail


class IdeaForm(BaseSignupForm):

    picture = forms.ImageField( required=False )
    title = forms.CharField( required=False, widget = forms.TextInput( attrs={ 'autofocus': 'autofocus' }))
    description = forms.CharField( required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}))

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        fields_key_order = ['picture', 'title', 'description', 'email']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

        self.fields['email'].required = False

        self.fields['picture'].label = _('Idee als Bild')
        self.fields['title'].label = _('Titel')
        self.fields['description'].label = _('Beschreibung')

        self.fields['picture'].help_text = _('Wenn Du magst')
        self.fields['title'].help_text = _('Wenn Du magst')
        self.fields['description'].help_text = _('Wenn Du magst')

    def clean(self):
        super(IdeaForm, self).clean()

        return self.cleaned_data

    def custom_signup(self, request, user):
        if user.email:
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            request.session["pass"] = password
        request.session["idea_signup"] = True
        return super(IdeaForm, self).custom_signup(request, user)

    def save(self, request):
        # this is copied from allauth SignupForm
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user


# class IdeaForm(forms.ModelForm):
#     class Meta:
#         model = Idea
#         fields = ('picture', 'title', 'description')

#         labels = {
#             'picture': _('Idee als Bild'),
#             'title': _('Titel'),
#             'description': _('Beschreibung'),
#         }
#         help_texts = {
#             'picture': _('Wenn Du magst'),
#             'title': _('Wenn Du magst'),
#             'description': _('Wenn Du magst'),
#         }