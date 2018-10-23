from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Telet.utils.token_generator import account_activation_token_generator

sender_email = 'hello@telet.com'


def send_email_activation_email(user, domain):
    """
    This function will send an email confirmation email to a specified user
    :param user: The user object to email
    :param domain: The current domain name
    :return: Will return 1 if email was sent successfully
    """
    context = {
        'user':user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode('UTF-8'),
        'token': account_activation_token_generator.make_token(user),
    }
    plain_text_message = render_to_string(
        'emails/plain_text/confirm_email.txt',
        context
    )
    result = send_mail(
        subject='Telet - Confirm Email',
        message=plain_text_message,
        from_email=sender_email,
        recipient_list=[user.email, ],
    )

    return result