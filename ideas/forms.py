from django import forms
from django.utils.translation import ugettext_lazy as _	
from .models import Idea


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('picture', 'title', 'description')

        labels = {
            'picture': _('Idee als Bild'),
            'title': _('Titel'),
            'description': _('Beschreibung'),
        }
        help_texts = {
            'picture': _('Wenn Du magst'),
            'title': _('Wenn Du magst'),
            'description': _('Wenn Du magst'),
        }