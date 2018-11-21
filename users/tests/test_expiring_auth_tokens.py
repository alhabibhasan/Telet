from datetime import timedelta, datetime, date

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from users.expiring_token_auth import ExpiringTokenAuthentication
from users.models import Teler


class TestToken:
    def __init__(self, datetime):
        self.created = datetime

class TestExpiringAuthenticationTokens(APITestCase):

    def setUp(self):

        self.token_auth = ExpiringTokenAuthentication()

        self.test_user_1 = get_user_model().objects.create_user(email='telet@test1.com', username='telet@test1.com', )
        self.test_user_1.set_password('12345')
        self.test_user_1.save()

        self.test_teler_1 = Teler.objects.create(user=self.test_user_1,
                                            gender='M',
                                            mobile_number='07940236488',
                                            date_of_birth=date(year=1998, month=4, day=11),
                                            email_verified=True)
        self.test_teler_1.save()

    def test_if_old_token_is_expired(self):
        token = TestToken(datetime(year=2018, month=1, day=1, tzinfo=pytz.UTC))

        self.assertTrue(self.token_auth.token_expired(token))


    def test_if_just_expired_token_is_expired(self):
        expiration_limit = settings.AUTH_TOKEN_EXPIRE_AFTER_DAYS

        created = datetime.now(timezone.utc) - timedelta(days=expiration_limit)

        token = TestToken(created)

        self.assertTrue(self.token_auth.token_expired(token))

    def test_if_in_date_token_is_expired(self):
        created = datetime.now(timezone.utc) - timedelta(days=1)

        token = TestToken(created)

        self.assertFalse(self.token_auth.token_expired(token))