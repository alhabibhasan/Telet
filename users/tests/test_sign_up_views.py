# Create your tests here.
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.utils import json
from users.views.authentication_views import UserSignUpView


class TestPatientSignUp(APITestCase):
    # Init the factory object
    factory = APIRequestFactory()
    # Get the user sign up url
    url = reverse_lazy('users:signup')

    def test_sign_up_valid_passwords(self):
        """
        Ensure that we can create an account
        """
        # Define the data to be used
        data = {
            "user": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test_user@telet.com",
                "password1": "some_random_password123",
                "password2": "some_random_password123"
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }

        # define the request
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        # init the view
        view = UserSignUpView.as_view()

        # send the request to the view and store the response
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up_invalid_passwords(self):
        """
        Ensure that we can create an account
        """
        # Define the data to be used
        data = {
            "user": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test_user@telet.com",
                "password1": "password",
                "password2": "password"
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }

        # define the request
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')

        # init the view
        view = UserSignUpView.as_view()

        # send the request to the view and store the response
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_duplicate_email(self):
        """
        Ensure that we can't create an account with an email that is already being used
        """
        data = {
            "user": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test_user@telet.com",
                "password1": "some_random_password123",
                "password2": "some_random_password123"
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }
        view = UserSignUpView.as_view()

        first_request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        view(first_request)  # send the first request

        second_request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        second_response = view(second_request)  # send the second request with the same data value

        self.assertEquals(second_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_mismatch_passwords(self):
        """
        Ensure that we can't create an account with mismatching passwords
        """
        data = {
            "user": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test_user@telet.com",
                "password1": "some_random_password123",
                "password2": "some_random_password"
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        view = UserSignUpView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_sign_up_missing_required_name_fields(self):

        data = {
            "user": {
                "first_name": "",
                "last_name": "",
                "email": "test_user@telet.com",
                "password1": "some_random_password123",
                "password2": "some_random_password123"
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        view = UserSignUpView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_missing_required_password_fields(self):

        data = {
            "user": {
                "first_name": "",
                "last_name": "",
                "email": "test_user@telet.com",
                "password1": "",
                "password2": ""
            },
            "mobile_number": "07940236488",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        view = UserSignUpView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_sign_up_missing_non_required_fields(self):

        data = {
            "user": {
                "first_name": "Test",
                "last_name": "User",
                "email": "test_user@telet.com",
                "password1": "some_random_password123",
                "password2": "some_random_password123"
            },
            "mobile_number": "",
            "date_of_birth": "2000-01-01",
            "gender": "M"
        }
        request = self.factory.post(path=self.url, data=json.dumps(data), content_type='application/json')
        view = UserSignUpView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)