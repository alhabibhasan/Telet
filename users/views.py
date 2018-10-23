from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, TemplateView

from Telet.utils.emails import send_email_activation_email
from Telet.utils.token_generator import account_activation_token_generator
from users.forms import UserLoginForm, UserSignUpForm, SendEmailActivationForm
from users.models import Teler, CustomUser


class TelerSignInView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'registration/teler_signin.html'

    def get_success_url(self):
        return reverse_lazy('users:signed_in')


class TelerSignUpView(FormView):
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

        messages.warning(request,
                         'The form was filled in incorrectly, please try again. ' + str(sign_up_form.error_messages))
        return redirect(to=reverse_lazy('users:signup'))


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


class TelerUserActivation(TemplateView):

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def get(self, request, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))

            user = CustomUser.objects.get(id=uid)

            teler = Teler.objects.get(user=user)

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, Teler.DoesNotExist):
            user = None
            teler = None

        if user is not None and teler is not None and \
                account_activation_token_generator.check_token(user=user, token=token):
            user.is_active = True
            user.save()

            teler.email_verified = True
            teler.save()

            messages.info(request=request,
                          message='You have successfully verified your email address. Welcome!')
            login(request=request,user=user)
            return redirect(reverse_lazy('users:signed_in'))

        messages.error(request=request,
                       message='Unfortunately that link didn\'t work, please request another one and try again.')
        return redirect(reverse_lazy('users:signin'))


class TelerPasswordResetView(PasswordResetView):
    email_template_name = 'emails/html/password_reset_email.html'
    subject_template_name = 'emails/plain_text/password_reset_subject'
    template_name = 'registration/teler_password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')


class TelerPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/teler_password_reset_done.html'


class TelerPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/teler_password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class TelerPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/teler_password_reset_complete.html'


class TelerSendEmailActivationEmailView(FormView):
    form_class = SendEmailActivationForm
    template_name = 'registration/teler_send_email_activation.html'
    success_url = reverse_lazy('users:signin')

    def form_valid(self, form):
        if form.is_valid():
            try:
                user = CustomUser.objects.get(username=form.cleaned_data['email'])
            except CustomUser.DoesNotExist:
                user = None

            if user is not None:
                send_email_activation_email(user, get_current_site(self.request))
            messages.info(request=self.request,
                          message='An activation email was sent again, please check you emails.')
            return super().form_valid(form)




