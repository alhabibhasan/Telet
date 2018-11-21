from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from users.models import CustomUser, Teler
from users.utils.emails import send_email_activation_email
from users.utils.token_generator import account_activation_token_generator


class UserActivationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            uid = force_text(urlsafe_base64_decode(attrs.get('uidb64')))

            self.user = CustomUser.objects.get(id=uid)

            self.teler = Teler.objects.get(user=self.user)

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, Teler.DoesNotExist) as e:
            raise serializers.ValidationError('Invalid uid.')

        if self.user is not None and self.teler is not None and \
                account_activation_token_generator.check_token(user=self.user, token=attrs.get('token')):
            self.user.is_active = True
            self.user.save()

            self.teler.email_verified = True
            self.teler.save()

            return attrs

        raise serializers.ValidationError('Invalid token.')


class SendUserActivationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        try:
            user = CustomUser.objects.get(username=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            request = self.context['request']
            send_email_activation_email(user, get_current_site(request))
            return email
