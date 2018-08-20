from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView

from accounts.forms.person import PersonSignUpForm


class PersonSignUpView(FormView):
    form_class = PersonSignUpForm
    template_name = 'person/signup.html'
