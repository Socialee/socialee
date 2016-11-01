from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ('title','author')

    def __init__(self, *args, **kwargs):
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = "Ich habe fertig."
        self.fields['title'].label = "Das Zitat:"
        self.fields['author'].widget.attrs['placeholder'] = "Giovanni Trapattoni"
        self.fields['author'].label = "Wer hat\'s gesagt?"
