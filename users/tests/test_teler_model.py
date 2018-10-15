# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import UserLoginForm
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

        test_user_2 = get_user_model().objects.create_user(email='telet@test2.com', username='telet@test2.com')
        test_user_2.set_password('abcde')
        test_user_2.save()

        test_teler_2 = Teler.objects.create(user=test_user_2,
                                            gender='M',
                                            mobile_number='0000000000',
                                            date_of_birth=date(year=1998, month=4, day=11)
                                            )
        test_teler_2.save()

        test_user_3 = get_user_model().objects.create_user(email='telet@test3.com', username='telet@test3.com')
        test_user_3.set_password('wxyz')
        test_user_3.save()

    def test_sign_in_form_valid_details(self):
        data = {
            'username': 'telet@test1.com',
            'password': '12345'
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertTrue(sign_in_form.is_valid())

    def test_sign_in_form_invalid_email_1(self):
        data = {
            'username': 'telet',
            'password': '12345'
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertFalse(sign_in_form.is_valid())

    def test_sign_in_form_invalid_email_2(self):
        data = {
            'username': 'telet@live',
            'password': '12345'
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertFalse(sign_in_form.is_valid())

    def test_sign_in_form_invalid_missing_email(self):
        data = {
            'username': '',
            'password': '12345'
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertFalse(sign_in_form.is_valid())

    def test_sign_in_form_invalid_missing_password(self):
        data = {
            'username': 'telet@user.com',
            'password': ''
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertFalse(sign_in_form.is_valid())

    def test_sign_in_not_teler(self):
        data = {
            'username': 'telet@user3.com',
            'password': 'wxyz'
        }

        sign_in_form = UserLoginForm(data=data)

        self.assertFalse(sign_in_form.is_valid())
