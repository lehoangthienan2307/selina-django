from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from selinaapp.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid64 = self.context.get('uid64')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid64))
            self.user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(self.user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            # user.set_password(password)
            # user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(self.user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
    
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance