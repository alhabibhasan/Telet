from datetime import timedelta, datetime

from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from django.conf import settings

from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):

    def token_expired(self, token):
        created_at = token.created
        current_time = datetime.now(timezone.utc)
        expire_after = timedelta(days=settings.AUTH_TOKEN_EXPIRE_AFTER_DAYS)
        expired = (current_time >= created_at + expire_after)

        return expired

    def authenticate_credentials(self, key):
        token = self.__get_token(key)

        if self.token_expired(token):
            token.delete()
            raise exceptions.AuthenticationFailed('Token has expired, you need to log back in.')

        return super().authenticate_credentials(key)

    def delete_token(self, key):
        token = self.__get_token(key)
        token.delete()

    def __get_token(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token. You may need to log in again.')

        return token