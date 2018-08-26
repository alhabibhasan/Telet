from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(blank=False, max_length=255)
    last_name = models.CharField(blank=False, max_length=255)
    email = models.EmailField(blank=False, max_length=255, unique=True)
    username = models.CharField(blank=False, max_length=255, unique=True)


class Teler(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, default=None, unique=True)
    profile_picture = models.URLField(blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=False)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other')
    )
    gender = models.CharField(blank=False, max_length=1, choices=gender_choices)
    email_verified = models.BooleanField(default=False)
