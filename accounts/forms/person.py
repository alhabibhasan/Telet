from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PersonSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'size': 35, 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
