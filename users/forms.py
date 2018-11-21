from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField

from users.models import CustomUser, Teler

class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'email',
                  )


class SendEmailActivationForm(forms.Form):
    email = forms.EmailField()
