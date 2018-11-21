from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.expiring_token_auth import ExpiringTokenAuthentication
from users.serializers.model_serializers import TelerSerializer
from users.serializers.auth_serializers import TelerSigninSerializer
from users.models import Teler, CustomUser


class UserSignInView(GenericAPIView):
    serializer_class = TelerSigninSerializer

    def login(self):
        self.user = self.serializer.validated_data['user']

        self.token, created = Token.objects.get_or_create(user=self.user)

    def post(self, request, *args, **kwargs):

        self.serializer = self.get_serializer(data=request.data)

        try:
            self.serializer.is_valid(raise_exception=True)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.login()

        return Response({'token': self.token.key},
                        status=status.HTTP_200_OK)


class UserSignUpView(CreateAPIView):
    '''
    This is used to allow users to sign up.
    '''
    model = Teler
    permission_classes = (AllowAny,)
    serializer_class = TelerSerializer


class UserSignoutView(APIView):
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):

        expiring_token_auth = ExpiringTokenAuthentication()
        expiring_token_auth.delete_token(request.auth)

        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)
