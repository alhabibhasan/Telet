from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import reverse_lazy

from users.auth_mixins import TelerLogOutRequiredMixin

class TelerPasswordReset(TelerLogOutRequiredMixin):
    redirect_url = reverse_lazy('users:signed_in')
    redirect_error_message = 'To change your password, use the change password option.'


class TelerPasswordResetView(TelerPasswordReset, PasswordResetView):
    email_template_name = 'emails/html/password_reset_email.html'
    subject_template_name = 'emails/plain_text/password_reset_subject'
    template_name = 'registration/teler_password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')


class TelerPasswordResetDoneView(TelerPasswordReset, PasswordResetDoneView):
    template_name = 'registration/teler_password_reset_done.html'


class TelerPasswordResetConfirmView(TelerPasswordReset, PasswordResetConfirmView):
    template_name = 'registration/teler_password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class TelerPasswordResetCompleteView(TelerPasswordReset, PasswordResetCompleteView):
    template_name = 'registration/teler_password_reset_complete.html'