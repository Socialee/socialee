from django import forms
from collections import OrderedDict
from register.forms import *
from django.forms import *

from .models import Idea

from django.utils.translation import ugettext_lazy as _ 


class IdeaForm(EmailRegisterForm):

    picture = ImageField( required=False, widget = FileInput( attrs={'class' : 'input_with_img'} ) )
    picturefile = CharField( #Add room throws DoesNotExist error
                            widget=HiddenInput,       
                            required=False,
                            label='')
    title = CharField( required=False, widget = TextInput( attrs={ 'autofocus': 'autofocus' }))
    description = CharField( required=False, widget=Textarea(attrs={'cols': 80, 'rows': 5, 'max_length':1500, 'class':'input_with_bound'}))
    YESNO_CHOICES = ((1, 'Ja'),(0, 'Nein')) 
    private = ChoiceField(
                     choices=YESNO_CHOICES, widget=RadioSelect
                )

    def __init__(self, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        fields_key_order = ['picture', 'picturefile', 'title', 'description', 'private', 'email']
        self.fields = OrderedDict((k, self.fields[k]) for k in fields_key_order)

        self.fields['email'].required = False
        self.fields['picture'].label = _('')
        self.fields['title'].label = _('Ideen-Titel')
        self.fields['description'].label = _('Beschreibung der Idee')
        self.fields['private'].label = _('Möchtest du, dass nur du diese Idee sehen kannst? Du kannst das später jederzeit ändern.')
        self.fields['private'].initial = 0

        self.fields['picture'].help_text = _('')
        self.fields['title'].help_text = _('')
        self.fields['description'].help_text = _('')

    def custom_signup(self, request, user):
        request.session["idea_register"] = True
        return super(IdeaForm, self).custom_signup(request, user)


class IdeaEditForm(ModelForm):

    class Meta:
        model = Idea
        fields = ('picture', 'title', 'description', 'private')
        labels = {
            'picture' : _('Idee als Bild'),
            'title': _('Ideen-Titel'),
            'description' : _('Beschreibung der Idee'),
            'private' :  _(' Private Idee? '),
        }
        widgets = {
            'picture' : ClearableFileInput( attrs={'class' : 'input_with_img'} ),
            'title': TextInput( attrs={ 'autofocus': 'autofocus' }),
            'description' : Textarea(attrs={'cols': 80, 'rows': 5, 'max_length':1500, 'class':'input_with_bound'}),
        }

