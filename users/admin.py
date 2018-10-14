from django.contrib import admin

from users.models import Teler


@admin.register(Teler)
class TelerAdmin(admin.ModelAdmin):
    fields = ('user', 'profile_picture', 'date_of_birth', 'mobile_number', 'gender', 'email_verified')
    readonly_fields = ('user',)
