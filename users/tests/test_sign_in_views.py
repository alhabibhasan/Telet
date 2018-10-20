# Create your tests here.
from datetime import date

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from users.models import Teler


class TestPatientSignIn(TestCase):

    def setUp(self):
        test_user_1 = get_user_model().objects.create_user(email='telet@test1.com', username='telet@test1.com', )
        test_user_1.set_password('12345')
        test_user_1.save()

        test_teler_1 = Teler.objects.create(user=test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11)
                                            )
        test_teler_1.save()


    def test_sign_in_valid_details(self):
        data = {
            'username': 'telet@test1.com',
            'password': '12345'
        }

        response = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.is_authenticated)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/signed-in/')


    def test_sign_in_invalid_user_credentials(self):
        data = {
            'username': 'telet@test1.com',
            'password': '54321'
        }

        response = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertNotEqual(user.username, data['username'])
        self.assertFalse(user.is_authenticated)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
        self.assertContains(response, 'Please enter a correct username and '
                                      'password. Note that both fields may be '
                                      'case-sensitive.')

    def test_sign_in_missing_user_credentials_1(self):
        data = {
            'username': '',
            'password': '54321'
        }

        response = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_sign_in_missing_user_credentials_2(self):
        data = {
            'username': '',
            'password': ''
        }

        response = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')

    def test_sign_in_invalid_user_credentials_2(self):
        data = {
            'username': '345345345345',
            'password': '345345346545'
        }

        response = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signin.html')
