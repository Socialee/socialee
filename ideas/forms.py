from django import forms

from .models import Idea


class IdeaForm_first(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('picture',)


class IdeaForm_second(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'description')


class IdeaForm_third(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('author',)