# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.utils import json

from users.models import Teler
from users.views.authentication_views import UserSignInView


class TestUserSignInViews(APITestCase):
    # Init the factory object
    factory = APIRequestFactory()
    # Get the user sign up url
    url = reverse_lazy('users:signin')

    def setUp(self):
        test_user_1 = get_user_model().objects.create_user(email='telet@test1.com',
                                                           username='telet@test1.com',
                                                           is_active=True)
        test_user_1.set_password('random_password_123')
        test_user_1.save()

        test_teler_1 = Teler.objects.create(user=test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11),
                                            email_verified=True)
        test_teler_1.save()

        test_user_2 = get_user_model().objects.create_user(email='telet@test2.com',
                                                           username='telet@test2.com',
                                                           )
        test_user_2.set_password('12345')
        test_user_2.save()

        test_teler_2 = Teler.objects.create(user=test_user_2,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11),
                                            email_verified=False)
        test_teler_2.save()

    def test_sign_in_normal(self):
        data = {
            'email': 'telet@test1.com',
            'password': 'random_password_123'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_sign_in_invalid_credentials(self):
        data = {
            'email': 'telet@fake.com',
            'password': 'fake'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_credentials_mixed_up_1(self):
        data = {
            'email': 'telet@user1.com',
            'password': 'abcde'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_credentials_mixed_up_2(self):
        data = {
            'email': 'telet@user2.com',
            'password': '12345'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_sign_in_invalid_credentials_mixed_up_3(self):
        data = {
            'email': '745675675486546',
            'password': '54654645654456'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_email_not_verified(self):
        data = {
            'email': 'telet@test2.com',
            'password': '12345'
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_no_fields(self):
        data = {
        }

        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        view = UserSignInView.as_view()

        response = view(request)

        print(response)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)