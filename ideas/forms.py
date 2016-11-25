from django import forms
from collections import OrderedDict
from register.forms import *

from django.utils.translation import ugettext_lazy as _ 


class IdeaForm(EmailRegisterForm):

    picture = forms.ImageField( required=False, widget = forms.FileInput( attrs={'class' : 'input_with_img'} ) )
    picturefile = forms.CharField( #Add room throws DoesNotExist error
                            widget=forms.HiddenInput,       
                            required=False,
                            label='')
    title = forms.CharField( required=False, widget = forms.TextInput( attrs={ 'autofocus': 'autofocus' }))
    description = forms.CharField( required=False, widget=forms.Textarea(attrs={'cols': 80, 'rows': 5, 'max_length':1500, 'class':'input_with_bound'}))

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        fields_key_order = ['picture', 'picturefile', 'title', 'description', 'email']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

        self.fields['email'].required = False
        self.fields['picture'].label = _('Idee als Bild')
        self.fields['title'].label = _('Ideen-Titel')
        self.fields['description'].label = _('Beschreibung der Idee')

        self.fields['picture'].help_text = _('Wenn du eins hast')
        self.fields['title'].help_text = _('Wenn du magst')
        self.fields['description'].help_text = _('Wenn du Lust hast')

    def custom_signup(self, request, user):
        request.session["idea_register"] = True
        return super(IdeaForm, self).custom_signup(request, user)