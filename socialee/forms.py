from allauth.account.forms import LoginForm

from django import forms
from .models import Project, Profile, UserEntry, Input, Output


# class QuoteForm(forms.ModelForm):
#     class Meta:
#         model = Quote
#         fields = ('title', 'author')


class StartProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')
    

class MyLoginForm(LoginForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')
