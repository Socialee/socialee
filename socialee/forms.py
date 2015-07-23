# from allauth.account.forms import SignupForm
from django import forms

class SignupForm(forms.Form):
	first_name = forms.CharField(label='Vorname', widget=forms.TextInput(attrs={'placeholder': 'Vorname'}), max_length=30)
	last_name = forms.CharField(label='Nachname', widget=forms.TextInput(attrs={'placeholder': 'Nachname'}), max_length=30)
	# newsletter = forms.BooleanField()


	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		# user.profile.newsletter = self.cleaned_data['newsletter']  # TODO
		user.save()

