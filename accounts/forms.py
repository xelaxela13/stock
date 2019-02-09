from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'location', 'password1', 'password2',)
        widgets = {
            'location': forms.HiddenInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email.split('@')[0]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
