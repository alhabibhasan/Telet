from django.test import TestCase

from users.forms import UserSignUpForm


class TestUserSignUpForms(TestCase):
    def test_sign_up_normal(self):

        form = UserSignUpForm(data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        })

        self.assertTrue(form.is_valid())


    def test_sign_up_password_mismatch(self):

        form = UserSignUpForm(data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_456'
        })

        self.assertFalse(form.is_valid())

    def test_sign_up_invalid_email(self):

        form = UserSignUpForm(data={
            'email': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        })

        self.assertFalse(form.is_valid())

    def test_sign_up_invalid_DOB(self):
        form = UserSignUpForm(data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'M',
            'date_of_birth': '01/01/1',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        })

        self.assertFalse(form.is_valid())

    def test_sign_up_invalid_gender(self):
        form = UserSignUpForm(data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'XXX',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        })

        self.assertFalse(form.is_valid())

    def test_sign_up_email_exists(self):
        from users.models import CustomUser
        user = CustomUser(email='test@telet.com', username='test@telet.com')
        user.set_password('random_password_123')
        user.save()

        form = UserSignUpForm(data={
            'email': 'test@telet.com',
            'first_name': 'Test',
            'last_name': 'User',
            'gender': 'F',
            'date_of_birth': '01/01/2000',
            'mobile_number': '07940236488',
            'password1': 'random_password_123',
            'password2': 'random_password_123'
        })

        self.assertFalse(form.is_valid())