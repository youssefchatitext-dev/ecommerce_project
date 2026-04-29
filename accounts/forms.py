from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PendingSignup


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if PendingSignup.objects.filter(username=username).exists():
            raise forms.ValidationError("Un compte est deja en attente de confirmation avec ce nom d'utilisateur.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est deja utilisee.")
        if PendingSignup.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte est deja en attente de confirmation avec cette adresse email.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Adresse email")
    first_name = forms.CharField(required=False, label="Prenom")
    last_name = forms.CharField(required=False, label="Nom")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class StyledPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={"placeholder": "Entrez votre mot de passe actuel"}),
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Choisissez un nouveau mot de passe"}),
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Retapez le nouveau mot de passe"}),
    )
