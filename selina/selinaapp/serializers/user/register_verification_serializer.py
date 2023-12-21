from rest_framework import serializers
from selinaapp.utils import Util
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from selinaapp.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes

class RegisterVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        try:
            self.user = User.objects.get(email=email)
            if self.user.otp != otp:
                raise serializers.ValidationError('Invalid OTP')
            return attrs
        except(User.DoesNotExist):
            raise serializers.ValidationError('Email not exist')
        
    def update(self, instance, validated_data):
        instance.status = 'normal'
        instance.save()
        return instance
    