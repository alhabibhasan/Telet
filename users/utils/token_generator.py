from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from users.models import Teler


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):

        teler = Teler.objects.get(user=user)

        return (six.text_type(user.id) + six.text_type(teler.email_verified) + str(timestamp))


account_activation_token_generator = AccountActivationTokenGenerator()
