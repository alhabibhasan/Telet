from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PersonSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('You already have an account.',
                                        code='exists')


