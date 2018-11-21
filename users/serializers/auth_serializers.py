from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class TelerSigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input-type': 'password'})

    def validate(self, attrs):
        if attrs['email'] is None or attrs['password'] is None:
            raise serializers.ValidationError('Email address and password are required')

        email = attrs['email']

        user = get_user_model().objects.get(email=email)

        if not user.teler.email_verified:
            raise serializers.ValidationError('Your email hasn\'t been activated yet, please check your emails.')

        attrs['user'] = user

        return attrs
