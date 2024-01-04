from rest_framework import serializers
from selinaapp.utils import Util
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from selinaapp.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes

class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            self.user = User.objects.get(email=email)
            #
            # uid = urlsafe_base64_encode(force_bytes(self.user.id))
            # token = PasswordResetTokenGenerator().make_token(self.user)
            # link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            #
            
            
            return attrs
        except(User.DoesNotExist):
            raise serializers.ValidationError({"email":"Email không tồn tại"})
    
    def update(self, instance, validated_data):
        password = Util.generate_password()
        instance.set_password(password)
        instance.save()

        body = 'Your password has been reset to '+password
        data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':self.user.email
        }
        Util.send_email(data)
        return instance