from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField

from users.models import CustomUser, Teler


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'autofocus': True}, ),
        label="Email"
    )

    class Meta(AuthenticationForm):
        model = CustomUser



class UserCreationForm(UserCreationForm):
    """
    TODO: Add profile image field once you set up some backend storage for images.
    """
    mobile_phone = forms.CharField(max_length=20)

    date_of_birth = forms.DateField(help_text=" Format: DD/MM/YYYY",
                                    input_formats=[
                                        '%d/%m/%Y'
                                    ])
    gender = forms.ChoiceField(choices=Teler.gender_choices)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(username=email).exists():
            raise forms.ValidationError("You've already signed up!",
                                        code='exists'
                                        )
        return email

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',
                  'first_name',
                  'last_name',
                  'gender',
                  'date_of_birth',
                  'mobile_phone',
                  )

        widgets = {
            'first_name': forms.TextInput,
            'last_name': forms.TextInput,
            'gender': forms.Select,
            'email': forms.EmailInput,
            'mobile': forms.CharField,
            'password1': forms.PasswordInput,
            'password2': forms.PasswordInput,

        }


class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'email',
                  )
