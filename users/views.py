from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from users.forms import UserLoginForm, UserSignUpForm
from users.models import Teler


class TelerLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('users:user-logged-in')


class TelerSignUpView(FormView):
    form_class = UserSignUpForm
    template_name = 'signup.html'

    def post(self, request, *args, **kwargs):
        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            print(sign_up_form.data)
            user = sign_up_form.save(commit=False)
            user.username = user.email
            user.is_active = True  # TODO: Change once we've implemented emails
            user.save()

            teler = Teler(user=user,
                          mobile_number=sign_up_form.cleaned_data['mobile_number'],
                          date_of_birth=sign_up_form.cleaned_data['date_of_birth'],
                          gender=sign_up_form.cleaned_data['gender']
                          )
            teler.save()

            return redirect(to=reverse_lazy('users:user-login'))

        messages.warning(request,
                         'The form was filled in incorrectly, please try again. ' + str(sign_up_form.error_messages))
        return redirect(to=reverse_lazy('users:user-signup'))


class TelerLoggedInView(LoginRequiredMixin, TemplateView):
    template_name = 'logged-in.html'
    login_url = reverse_lazy('users:user-login')


class TelerUserLogout(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users:user-login')
    template_name = 'logged-out.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request=self.request,
                      template_name=self.template_name)
