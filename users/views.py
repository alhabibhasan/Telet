from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import FormView, TemplateView

from Telet.utils.emails import send_email_confirmation_email
from Telet.utils.token_generator import account_activation_token_generator
from users.forms import UserLoginForm, UserSignUpForm
from users.models import Teler, CustomUser


class TelerSignInView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'signin.html'

    def get_success_url(self):
        user = self.authentication_form.get_user()
        context = super().get_context_data()
        context['user'] = user
        return render(template_name=self.template_name, context=context)


class TelerSignUpView(FormView):
    form_class = UserSignUpForm
    template_name = 'signup.html'

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
            send_email_confirmation_email(user, get_current_site(self.request))
            messages.info(request=request,
                          message='You will need to activate your email address before you can sign in.'
                                  + ' Please check your emails.')
            return redirect(to=reverse_lazy('users:signin'))

        messages.warning(request,
                         'The form was filled in incorrectly, please try again. ' + str(sign_up_form.error_messages))
        return redirect(to=reverse_lazy('users:signup'))


class TelerSignedInView(LoginRequiredMixin, TemplateView):
    template_name = 'signed-in.html'
    login_url = reverse_lazy('users:signin')


class TelerUserSignout(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('users:signin')
    template_name = 'signed-out.html'
    next_page = reverse_lazy('users:signin')

    def get_next_page(self):
        messages.info(request=self.request,
                      message='You have successfully signed out.')
        return super().get_next_page()


class TelerUserActivation(TemplateView):

    def get(self, request, uidb64, token):
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
            return redirect(reverse_lazy('users:signed-in'))

        messages.error(request=request,
                       message='Unfortunately that link didn\'t work, please request another one and try again.')
        return redirect(reverse_lazy('users:signin'))
