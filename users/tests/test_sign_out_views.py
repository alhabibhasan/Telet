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

        response_sign_in = self.client.post(reverse_lazy('users:signin'), data=data)

        user = auth.get_user(self.client)

        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.is_authenticated)

        self.assertEqual(response_sign_in.status_code, 302)
        self.assertRedirects(response_sign_in, '/users/signed-in/')

        response_sign_out = self.client.get(reverse_lazy('users:signout'))

        user = auth.get_user(self.client)

        self.assertEqual(response_sign_out.status_code, 302)
        self.assertFalse(user.is_authenticated)
