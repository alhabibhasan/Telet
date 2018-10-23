# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Telet.utils.token_generator import account_activation_token_generator
from users.models import Teler


class TestUserAccountActivation(TestCase):
    def setUp(self):
        self.test_user_1 = get_user_model().objects.create_user(email='telet@test1.com', username='telet@test1.com', )
        self.test_user_1.set_password('12345')
        self.test_user_1.save()

        self.test_teler_1 = Teler.objects.create(user=self.test_user_1,
                                                 gender='M',
                                                 mobile_number='07940236488',
                                                 date_of_birth=date(year=1998, month=4, day=11),
                                                 )
        self.test_teler_1.save()

    def test_user_activation(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user_1.pk)).decode('UTF-8')
        token = account_activation_token_generator.make_token(self.test_user_1)

        self.assertFalse(self.test_teler_1.email_verified)

        response = self.client.get(reverse_lazy('users:activate',
                                                kwargs={
                                                    'uidb64': uidb64,
                                                    'token': token
                                                }))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/users/signed-in/')
        # reload the latest teler object

        test_teler_1 = Teler.objects.get(user=self.test_user_1)

        self.assertTrue(test_teler_1.email_verified)

    def test_non_existant_user_activation(self):
        uidb64 = urlsafe_base64_encode(force_bytes('1213')).decode('UTF-8')
        token = account_activation_token_generator.make_token(self.test_user_1)

        response = self.client.get(reverse_lazy('users:activate',
                                                kwargs={
                                                    'uidb64': uidb64,
                                                    'token': token
                                                }))

        messages = list(get_messages(response.wsgi_request))

        # check the messages
        self.assertEqual(str(messages[0]),
                         'Unfortunately that link didn\'t work, please request another one and try again.')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/users/signin/')

    def test_send_activation_email_form_view(self):
        data = {
            'email': 'telet@test1.com',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url='/users/signin/')

        messages = list(get_messages(response.wsgi_request))

        # check the messages
        self.assertEqual(str(messages[0]),
                         'An activation email was sent again, please check you emails.')

    def test_send_activation_email_form_view_with_invalid_email(self):
        data = {
            'email': 'test',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'registration/teler_send_email_activation.html')


    def test_send_activation_email_form_view_with_email_non_existant(self):
        data = {
            'email': 'test@user.net',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url='/users/signin/')

        messages = list(get_messages(response.wsgi_request))

        # check the messages
        self.assertEqual(str(messages[0]),
                         'An activation email was sent again, please check you emails.')
