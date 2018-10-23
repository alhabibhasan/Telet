import time
from datetime import date
from django.test import TestCase

from Telet.utils.token_generator import account_activation_token_generator
from users.models import CustomUser, Teler


class TestTokenGeneratorHashValueFunction(TestCase):

    def test_hash_value_return(self):
        user = CustomUser(email='test@telet.com',
                          first_name='Test',
                          last_name='User',
                          is_active=False)
        user.set_password('random_password_123')
        user.save()

        teler = Teler(user=user,
                      mobile_number='07946493658',
                      date_of_birth=date(year=1998, month=1, day=1),
                      email_verified=False)
        teler.save()

        timestamp = time.time()

        hash_value = account_activation_token_generator._make_hash_value(user, timestamp)

        self.assertEqual(hash_value, str(user.id) + str(teler.email_verified) + str(timestamp))

