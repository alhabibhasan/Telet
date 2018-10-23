from datetime import date

from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy

from users.utils.emails import send_email_activation_email
from users.models import CustomUser, Teler


class TestSendingEmails(TestCase):

    def test_sending_email_confirmation_email(self):
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

        rf = RequestFactory()
        request = rf.get(reverse_lazy('users:signin'))

        self.assertEqual(send_email_activation_email(user, get_current_site(request)), 1)




