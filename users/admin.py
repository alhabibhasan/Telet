from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from users.forms import UserCreationForm
from users.models import CustomUser


class UserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name')


class UserAdmin(UserAdmin):
    add_form = UserCreationForm

    prepopulated_fields = {'username': ('first_name', 'last_name', 'email')}

    add_fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',),
        }),
    )


admin.site.register(CustomUser, UserAdmin)
