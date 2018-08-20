from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView

from accounts.forms.person import PersonSignUpForm


class PersonSignUpView(FormView):
    form_class = PersonSignUpForm
    template_name = 'person/signup.html'

    def post(self, request, *args, **kwargs):
        form = PersonSignUpForm(request.POST)
        return HttpResponse(form.is_valid())
