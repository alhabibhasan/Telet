from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Teler
from users.serializers import TelerSerializer


class CreateUserView(CreateAPIView):
    '''
    This is used to allow users to sign up.
    '''
    model = Teler
    permission_classes = (AllowAny,)
    serializer_class = TelerSerializer

    # You can override the POST method if you need to do any custom action before the default action is completed


class UserLoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=status.HTTP_400_BAD_REQUEST)

        username = self._get_username(email)

        # set the default value to None
        user = None
        if username is not None:
            # if the user doesn't exist, then it will stay as None
            user = authenticate(username=username, password=password)

        # if the user name didn't exist (so email was fake)
        # OR the email and password were wrong, then run this if statement
        if username is None or user is None:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=status.HTTP_200_OK)

    def _get_username(self, email):
        user = get_user_model().objects.filter(email=email)
        if user is not None and len(user) == 1:
            return user.first().username
        return None
