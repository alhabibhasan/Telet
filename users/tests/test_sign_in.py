# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.utils import json
from users.models import Teler
from users.views import UserLoginView


class TestPatientSignIn(APITestCase):
    # Init the factory object
    factory = APIRequestFactory()
    # Get the user sign up url
    url = reverse_lazy('user-signin')

    def setUp(self):
        test_user_1 = get_user_model().objects.create_user(username='test_user1',
                                                           email='telet@test1.com')
        test_user_1.set_password('12345')
        test_user_1.save()

        test_teler_1 = Teler.objects.create(user=test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11)
                                            )
        test_teler_1.save()

        test_user_2 = get_user_model().objects.create_user(username='test_user2',
                                                           email='telet@test2.com')
        test_user_2.set_password('abcde')
        test_user_2.save()

        test_teler_2 = Teler.objects.create(user=test_user_2,
                                            gender='M',
                                            mobile_number='0000000000',
                                            date_of_birth=date(year=1998, month=4, day=11)
                                            )
        test_teler_2.save()

    def test_sign_in_normal(self):
        data = {
            'email': 'telet@test1.com',
            'password': '12345'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserLoginView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_sign_in_invalid_credentials(self):
        data = {
            'email': 'telet@fake.com',
            'password': 'fake'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserLoginView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_credentials_mixed_up_1(self):
        data = {
            'email': 'telet@user1.com',
            'password': 'abcde'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserLoginView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_credentials_mixed_up_2(self):
        data = {
            'email': 'telet@user2.com',
            'password': '12345'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserLoginView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
