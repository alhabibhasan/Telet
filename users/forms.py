from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import CustomUser


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'email',
                  )


class UserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name',
                  'last_name',
                  'email',
                  )
