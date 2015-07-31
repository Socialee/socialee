# from allauth.account.forms import SignupForm
from django import forms
from .models import Project, Profile, UserEntry


class SignupForm(forms.Form):
	project_title = forms.CharField(label='Projekt?', widget=forms.TextInput(attrs={'placeholder': 'place'}), required=False, max_length=5000)
	dream_title = forms.CharField(label='Dream?', widget=forms.TextInput(attrs={'placeholder': 'place'}), required=False, max_length=5000)
	wish_title = forms.CharField(label='Wish?', widget=forms.TextInput(attrs={'placeholder': 'place'}), required=False, max_length=5000)

	first_name = forms.CharField(label='Vorname', widget=forms.TextInput(attrs={'placeholder': 'Vorname'}), max_length=30)
	last_name = forms.CharField(label='Nachname', widget=forms.TextInput(attrs={'placeholder': 'Nachname'}), max_length=30)
	# newsletter = forms.BooleanField()


	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()

		# HACK
		user = UserEntry(id=user.id)

		profile = Profile.objects.create(user=user)
		# user.profile.newsletter = self.cleaned_data['newsletter']  # TODO
		#import ipdb; ipdb.set_trace()
		project = Project.objects.create(title=self.cleaned_data['project_title'])

		project.profiles.add(profile)
		project.save()


#class ProjectForm(forms.ModelForm):
#	class Meta:
#		model = Project
#		fields = ['title']


#class DreamForm(forms.ModelForm):
#	class Meta:
#		model = Dream
#		fields = ['title']


#class WishForm(forms.ModelForm):
#	class Meta:
#		model = Wish
#		fields = ['title']