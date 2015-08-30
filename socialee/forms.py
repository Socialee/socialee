from allauth.account.forms import SignupForm

from django import forms
from .models import Project, Profile, UserEntry, Input, Output


class MySignupForm(SignupForm):
    "A specialized signup form to ask for extra fields."

    project_title = forms.CharField(label='Socialee sammelt Ideen und Projekte. Und wir bauen ein Netzwerk drumrum und dazwischen.', widget=forms.Textarea(attrs={'placeholder': 'Corinna arbeitet mit Flüchtlingen, Waldemar produziert tolle Kondome. Socialee sagt: "Stellt euch mal ein soziales Netzwerk vor!"','rows':4}), required=False, max_length=5000)
    output_title = forms.CharField(label='Und, was fehlt Dir? Welches Bedürfnis wird nicht befriedigt?', widget=forms.Textarea(attrs={'placeholder': 'Susi fehlt ein Fahrrad. Helge fehlt eine Freundin. Socialee fehlt auch noch alles Mögliche. ','rows':4}), required=False, max_length=5000)
    input_title= forms.CharField(label='Wenn wir uns mal kurz entspannen, fällt uns wieder ein, was wir so alles gut können. Uh, wie gut Du bist!', widget=forms.Textarea(attrs={'placeholder': 'Petra kann Autos reparieren und Peter arbeitet gerne mit Kindern. Fadhumo kann Flüchtlinge motivieren und Socialee kann ganz gut zuhören.','rows':4}), required=False, max_length=5000)

    first_name = forms.CharField(label='Vorname', widget=forms.TextInput(attrs={'placeholder': 'Vorname'}), max_length=30)
    last_name = forms.CharField(label='Nachname', widget=forms.TextInput(attrs={'placeholder': 'Nachname'}), max_length=30)
    # newsletter = forms.BooleanField()

    def save(self, request):
        user = super().save(request)

        if "first_name" in self.cleaned_data:
            user.first_name = self.cleaned_data['first_name']
        if "last_name" in self.cleaned_data:
            user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class MyHomeSignupForm(MySignupForm):
    "A specialized signup form to not require some fields for signup on home."

    # Optional PLZ, used for Flüchlingspaten.
    plz = forms.CharField(label='PLZ', required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'Bitte trage hier Deine Postleitzahl ein.'}),
                          max_length=5)
    # Optional referrer project, used for Flüchlingspaten.
    ref_project = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password1"]
        del self.fields["password2"]
        del self.fields["first_name"]
        del self.fields["last_name"]

    def save(self, request):
        user = super().save(request)
        # HACK
        user = UserEntry(id=user.id)

        # Create profile with optional PLZ from socialee_project_slider.html.
        profile = Profile(user=user)
        if "plz" in self.cleaned_data:
            profile.plz = self.cleaned_data["plz"]
        profile.save()

        if self.cleaned_data['project_title']:
            project = Project.objects.create(title=self.cleaned_data['project_title'])
            project.profiles.add(profile)
            project.save()

        if self.cleaned_data['ref_project']:
            project, created = Project.objects.get_or_create(title=self.cleaned_data['ref_project'])
            project.profiles.add(profile)
            project.save()

        if self.cleaned_data['input_title']:
            input = Input.objects.create(title=self.cleaned_data['input_title'])
            input.profile = profile
            input.save()

        if self.cleaned_data['output_title']:
            output = Output.objects.create(title=self.cleaned_data['output_title'])
            output.profile = profile
            output.save()

        return user
