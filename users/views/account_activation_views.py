from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, FormView

from users.utils.emails import send_email_activation_email
from users.utils.token_generator import account_activation_token_generator
from users.auth_mixins import TelerLogOutRequiredMixin
from users.forms import SendEmailActivationForm
from users.models import CustomUser, Teler


class TelerUserActivation(TelerLogOutRequiredMixin, TemplateView):
    redirect_url = reverse_lazy('users:signed_in')
    redirect_error_message = 'You have already activated your account.'

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
            login(request=request, user=user)
            return redirect(reverse_lazy('users:signed_in'))

        messages.error(request=request,
                       message='Unfortunately that link didn\'t work, please request another one and try again.')
        return redirect(reverse_lazy('users:signin'))


class TelerSendEmailActivationEmailView(TelerLogOutRequiredMixin, FormView):
    redirect_url = reverse_lazy('users:signed_in')
    redirect_error_message = 'You have already activated your account.'

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