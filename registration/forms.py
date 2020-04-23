from django import forms
from django.contrib.auth.forms import UserCreationForm

from registration.models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
