# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.utils import json

from users.models import Teler
from users.utils.token_generator import account_activation_token_generator
from users.views.account_activation_views import TelerUserActivation


class TestUserAccountActivation(APITestCase):

    # Init the factory object
    factory = APIRequestFactory()

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

        self.test_user_2 = get_user_model().objects.create_user(email='telet@test2.com', username='telet@test2.com', )
        self.test_user_2.set_password('12345')
        self.test_user_2.save()

        self.test_teler_2 = Teler.objects.create(user=self.test_user_2,
                                                 gender='M',
                                                 mobile_number='07940236488',
                                                 date_of_birth=date(year=1998, month=4, day=11),
                                                 )
        self.test_teler_2.save()

    def test_user_activation(self):

        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user_1.pk)).decode('UTF-8')
        token = account_activation_token_generator.make_token(self.test_user_1)

        self.assertFalse(self.test_teler_1.email_verified)

        data = {
            'uidb64': uidb64,
            'token': token
        }

        request = self.factory.post('users/activate/', kwargs=data,
                                    data=json.dumps(data),
                                    content_type='application/json')

        view = TelerUserActivation.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # reload the latest teler object

        test_teler_1 = Teler.objects.get(user=self.test_user_1)

        self.assertTrue(test_teler_1.email_verified)

    def test_non_existant_user_activation(self):

        uidb64 = urlsafe_base64_encode(force_bytes('1213')).decode('UTF-8')
        token = account_activation_token_generator.make_token(self.test_user_1)

        self.assertFalse(self.test_teler_1.email_verified)

        data = {
            'uidb64': uidb64,
            'token': token
        }

        request = self.factory.post('users/activate/', kwargs=data,
                                    data=json.dumps(data),
                                    content_type='application/json')

        view = TelerUserActivation.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_bad_token_user_activation(self):

        # uses the wrong token for the user
        uidb64 = urlsafe_base64_encode(force_bytes(self.test_user_1.pk)).decode('UTF-8')
        token = account_activation_token_generator.make_token(self.test_user_2)

        self.assertFalse(self.test_teler_1.email_verified)

        data = {
            'uidb64': uidb64,
            'token': token
        }

        request = self.factory.post('users/activate/', kwargs=data,
                                    data=json.dumps(data),
                                    content_type='application/json')

        view = TelerUserActivation.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_send_activation_email_form_view(self):
        data = {
            'email': 'telet@test1.com',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 200)

    def test_send_activation_email_form_view_with_invalid_email(self):
        data = {
            'email': 'test',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 400)

    def test_send_activation_email_form_view_with_email_non_existant(self):
        data = {
            'email': 'test@user.net',
        }

        response = self.client.post(reverse_lazy('users:send_activation_email'), data=data)

        self.assertEqual(response.status_code, 200)
