from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from users.utils.emails import send_email_activation_email
from users.auth_mixins import TelerLogOutRequiredMixin
from users.forms import UserLoginForm, UserSignUpForm
from users.models import Teler


class TelerSignInView(TelerLogOutRequiredMixin, LoginView):
    redirect_url = reverse_lazy('users:signed_in')
    redirect_error_message = 'You have already signed in.'
    authentication_form = UserLoginForm
    template_name = 'registration/teler_signin.html'

    def get_success_url(self):
        return reverse_lazy('users:signed_in')


class TelerSignUpView(TelerLogOutRequiredMixin, FormView):
    redirect_url = reverse_lazy('users:signed_in')
    redirect_error_message = 'You have already signed up.'
    form_class = UserSignUpForm
    template_name = 'registration/teler_signup.html'

    def post(self, request, *args, **kwargs):
        sign_up_form = UserSignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save(commit=False)
            user.username = user.email
            user.save()

            teler = Teler(user=user,
                          mobile_number=sign_up_form.cleaned_data['mobile_number'],
                          date_of_birth=sign_up_form.cleaned_data['date_of_birth'],
                          gender=sign_up_form.cleaned_data['gender']
                          )
            teler.save()
            send_email_activation_email(user, get_current_site(self.request))
            messages.info(request=request,
                          message='You will need to activate your email address before you can sign in.' \
                                  + ' Please check your emails.')
            return redirect(to=reverse_lazy('users:signin'))

        return super().post(request, *args, **kwargs)


class TelerSignedInView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/teler_signed_in.html'
    login_url = reverse_lazy('users:signin')


class TelerUserSignout(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('users:signin')
    template_name = 'registration/teler_signed_out.html'
    next_page = reverse_lazy('users:signin')

    def get_next_page(self):
        messages.info(request=self.request,
                      message='You have successfully signed out.')
        return super().get_next_page()
