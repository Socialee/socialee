from django import forms

from .models import Password


class PasswordAdminForm(forms.ModelForm):
    """
    Form class for administering passwords in the admin
    """
    class Meta:
        model = Password
        fields = '__all__'


class PasswordForm(forms.Form):
    """
    Form class for inputting shared passwords
    """
    password = forms.CharField(widget=forms.PasswordInput)
    url = forms.CharField(widget=forms.HiddenInput, required=False)

    def clean_password(self):
        """
        Validates that the password is a current password
        """
        user_pass = self.cleaned_data.get('password')
        matches = Password.objects.filter(password=user_pass)
        if not matches:
            raise forms.ValidationError("Your password does not match.")
