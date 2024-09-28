"""User admin forms."""
from django import forms
from django.utils.translation import gettext as _

from apps.users.models import User


class UserCreationForm(forms.ModelForm):
    """User creation form."""
    password1 = forms.CharField(
        label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('retype password'), widget=forms.PasswordInput)

    class Meta:
        """Form metadata."""
        model = User
        fields = ['email']

    def clean_password2(self):
        """Password validation."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("passwords don`t match"))
        return password2

    def save(self, commit=True):
        """Save with password update."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
