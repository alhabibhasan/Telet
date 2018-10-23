from django.test import TestCase
from django.urls import reverse_lazy

from users.forms import UserSignUpForm
from users.models import CustomUser


class TestUserSignUpViews(TestCase):
    def test_sign_up_normal(self):

        data= {
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        user = CustomUser.objects.filter(email='test@telet.com')[0]

        self.assertTrue(user.email == 'test@telet.com')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response,expected_url='/users/signin/')


    def test_sign_up_password_mismatch(self):

        data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_456'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        self.assertEqual(response.status_code, 200)


    def test_sign_up_invalid_email(self):

        data={
            'email': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        self.assertEqual(response.status_code, 200)


    def test_sign_up_invalid_DOB(self):
        data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/1',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        self.assertEqual(response.status_code, 200)


    def test_sign_up_invalid_gender(self):
        data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'XXX',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        self.assertEqual(response.status_code, 200)


    def test_sign_up_email_exists(self):
        from users.models import CustomUser
        user = CustomUser(email='test@telet.com', username='test@telet.com')
        user.set_password('random_password_123')
        user.save()

        data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'F',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        }

        response = self.client.post(reverse_lazy('users:signup'), data=data)

        self.assertEqual(response.status_code, 200)
