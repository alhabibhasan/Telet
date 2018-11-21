from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import Teler, CustomUser
from users.utils.emails import send_email_activation_email

'''
UserSerializer is used as a nested field within the TelerSerializer.

At present, it is not used as a standalone serializer.
'''


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        # first create the user
        user = get_user_model().objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError('Passwords must match.')

        user = CustomUser(attrs)

        password = attrs['password1']

        try:
            validate_password(password=password, user=user)
        except ValidationError:
            raise serializers.ValidationError('Password cannot be too similar to your name or email.')

        return attrs

    class Meta:
        model = get_user_model()
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2',
                  )


class TelerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    def create(self, validated_data):
        # get the user information
        user_data = validated_data['user']
        # create the user object with validated data
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        # create the Teler object
        teler = Teler.objects.create(user=user,
                                     mobile_number=validated_data['mobile_number'],
                                     date_of_birth=validated_data['date_of_birth'],
                                     gender=validated_data['gender'],
                                     email_verified=False
                                     )
        request = self.context['request']

        if request is not None:
            send_email_activation_email(user, get_current_site(request))

        return teler

    class Meta:
        model = Teler
        fields = ('user',
                  'mobile_number',
                  'date_of_birth',
                  'gender',
                  )



