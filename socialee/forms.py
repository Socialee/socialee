# from allauth.account.forms import SignupForm
import os

from django import forms
from .models import Project, Profile, UserEntry, Wish, Dream, Input, Output


class SignupForm(forms.Form):
	dream_title = forms.CharField(label='Wenn es an nichts fehlen würde, nicht an Geld, nicht an Zeit, was würdest Du tun? Wofür brennst Du?', widget=forms.Textarea(attrs={'placeholder': 'Neil und Moritz würden mit einem Trecker quer durch Deutschland fahren. Socialee würde eine Webseite bauen, die diese Frage stellt.','rows':4}), required=False, max_length=5000)
	wish_title = forms.CharField(label='Du hast 5000 Zeichen. Lass Dich ruhig aus.', widget=forms.Textarea(attrs={'placeholder': '','rows':4}), required=False, max_length=5000)
	project_title = forms.CharField(label='Socialee sammelt Ideen und Projekte. Und wir bauen ein Netzwerk drumrum und dazwischen.', widget=forms.Textarea(attrs={'placeholder': 'Corinna arbeitet mit Flüchtlingen, Waldemar produziert tolle Kondome. Socialee sagt: "Stellt euch mal ein soziales Netzwerk vor!"','rows':4}), required=False, max_length=5000)	
	output_title = forms.CharField(label='Und, was fehlt Dir? Welches Bedürfnis wird nicht befriedigt?', widget=forms.Textarea(attrs={'placeholder': 'Susi fehlt ein Fahrrad. Helge fehlt eine Freundin. Socialee fehlt noch ein Frontendler. ','rows':4}), required=False, max_length=5000)	
	input_title= forms.CharField(label='Wenn wir uns mal kurz entspannen, fällt uns wieder ein, was wir so alles gut können. Uh, wie gut Du bist!', widget=forms.Textarea(attrs={'placeholder': 'Petra kann Autos reparieren und Peter arbeitet gerne mit Kindern. Fadhumo kann Flüchtlinge motivieren und Socialee kann ganz gut zuhören.','rows':4}), required=False, max_length=5000)	

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

		if len (self.cleaned_data['project_title']):
			project = Project.objects.create(title=self.cleaned_data['project_title'])
			project.profiles.add(profile)
			project.save()

		if len (self.cleaned_data['wish_title']):
			wish = Wish.objects.create(title=self.cleaned_data['wish_title'])
			wish.profiles.add(profile)
			wish.save()

		if len (self.cleaned_data['dream_title']):
			dream = Dream.objects.create(title=self.cleaned_data['dream_title'])
			dream.profiles.add(profile)
			dream.save()

		if len (self.cleaned_data['input_title']):
			input = Input.objects.create(title=self.cleaned_data['input_title'])
			input.profiles.add(profile)
			input.save()

		if len (self.cleaned_data['output_title']):
			output = Output.objects.create(title=self.cleaned_data['output_title'])
			output.profiles.add(profile)
			output.save()


# class ProjectForm(forms.ModelForm):
# 	class Meta:
# 		model = Project
# 		fields = ['title']

#class DreamForm(forms.ModelForm):
#	class Meta:
#		model = Dream
#		fields = ['title']


#class WishForm(forms.ModelForm):
#	class Meta:
#		model = Wish
#		fields = ['title']