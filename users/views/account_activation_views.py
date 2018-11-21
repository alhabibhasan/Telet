from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers.activation_serializers import UserActivationSerializer, SendUserActivationEmailSerializer


class TelerUserActivation(GenericAPIView):
    serializer_class = UserActivationSerializer

    '''
    At the moment, because the front end is yet to be implemented, the activation email will contain 
    a link with the uidb64 and token, this link will take you to a page that you need to enter those details into.
    The front end would be made to take those credentials and post the form automatically.
    '''

    def post(self, request, *args, **kwargs):
        assert 'uidb64' and 'token' in request.data
        self.serializer = self.get_serializer(data=request.data)

        try:
            self.serializer.is_valid(raise_exception=True)
        except (serializers.ValidationError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({'activated': 'Account activated successfully.'},
                        status=status.HTTP_200_OK)


class TelerSendEmailActivationEmailView(GenericAPIView):
    serializer_class = SendUserActivationEmailSerializer

    def post(self, request, *args, **kwargs):
        self.serializser = self.get_serializer(data=request.data)
        self.serializser.is_valid(raise_exception=True)

        return Response(
            {
                'sent': 'If a match was found, then an activation email was sent again, please check you emails.'
            },
            status=status.HTTP_200_OK)
