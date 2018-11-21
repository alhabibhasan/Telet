# Create your tests here.
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import exceptions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from users.expiring_token_auth import ExpiringTokenAuthentication
from users.models import Teler
from users.views.authentication_views import UserSignInView, UserSignoutView


class TestUserSignOutViews(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        test_user_1 = get_user_model().objects.create_user(email='telet@test1.com', username='telet@test1.com', )
        test_user_1.set_password('12345')
        test_user_1.save()

        test_teler_1 = Teler.objects.create(user=test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11),
                                            email_verified=True)
        test_teler_1.save()

    def _sign_in(self):

        data = {
            'email': 'telet@test1.com',
            'password': '12345'
        }

        sign_in_request = self.factory.post(path=reverse_lazy('users:signin'), data=json.dumps(data),
                                            content_type='application/json')

        sign_in_view = UserSignInView.as_view()

        sign_in_response = sign_in_view(sign_in_request)

        self.assertEquals(sign_in_response.status_code, status.HTTP_200_OK)

        self.token = sign_in_response.data.get('token')

        self.token_verifier = ExpiringTokenAuthentication()

        self.assertEqual(self.token_verifier.authenticate_credentials(self.token)[0].email, 'telet@test1.com')

    def test_sign_out_post(self):

        self._sign_in()

        sign_out_request = self.factory.post(path=reverse_lazy('users:signout'), content_type='application/json')

        # add authentication token to sign put request
        sign_out_request.auth = self.token

        sign_out_view = UserSignoutView.as_view()

        sign_out_response = sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.data.get('detail'), 'Successfully logged out.')

        try:
            self.token_verifier.authenticate_credentials(self.token)
        except (Token.DoesNotExist, exceptions.AuthenticationFailed) as e:
            self.assertEqual(str(e), 'Invalid Token. You may need to log in again.')
        else:
            self.assertTrue(False)

    def test_sign_out_put(self):

        self._sign_in()

        sign_out_request = self.factory.put(path=reverse_lazy('users:signout'), content_type='application/json')

        # add authentication token to sign put request
        sign_out_request.auth = self.token

        sign_out_view = UserSignoutView.as_view()

        sign_out_response = sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.data.get('detail'), 'Successfully logged out.')

        try:
            self.token_verifier.authenticate_credentials(self.token)
        except (Token.DoesNotExist, exceptions.AuthenticationFailed) as e:
            self.assertEqual(str(e), 'Invalid Token. You may need to log in again.')
        else:
            self.assertTrue(False)

    def test_sign_out_get(self):

        self._sign_in()

        sign_out_request = self.factory.get(path=reverse_lazy('users:signout'), content_type='application/json')

        # add authentication token to sign put request
        sign_out_request.auth = self.token

        sign_out_view = UserSignoutView.as_view()

        sign_out_response = sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.data.get('detail'), 'Successfully logged out.')

        try:
            self.token_verifier.authenticate_credentials(self.token)
        except (Token.DoesNotExist, exceptions.AuthenticationFailed) as e:
            self.assertEqual(str(e), 'Invalid Token. You may need to log in again.')
        else:
            self.assertTrue(False)

    def test_sign_out_patch(self):

        self._sign_in()

        sign_out_request = self.factory.patch(path=reverse_lazy('users:signout'), content_type='application/json')

        # add authentication token to sign put request
        sign_out_request.auth = self.token

        sign_out_view = UserSignoutView.as_view()

        sign_out_response = sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.data.get('detail'), 'Successfully logged out.')

        try:
            self.token_verifier.authenticate_credentials(self.token)
        except (Token.DoesNotExist, exceptions.AuthenticationFailed) as e:
            self.assertEqual(str(e), 'Invalid Token. You may need to log in again.')
        else:
            self.assertTrue(False)
