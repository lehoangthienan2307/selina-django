from rest_framework import serializers
from selinaapp.models.user import User
from selinaapp.utils import Util

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    # USER_TYPE = (
    #     ('NORMAL_USER', 'normal_user'),
    #     ('SELLER', 'seller'),
    #     ('ADMIN', 'admin'),
    # )
    # type = serializers.ChoiceField(choices=USER_TYPE)
    class Meta:
        model = User
        fields = ['email', 'fullname', 'password', 'password2', 'phone', 'gender', 'user_type']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({"password":"Password not match"})     
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        otp = Util.generate_otp()
        body = 'Your OTP is '+otp
        data = {
            'subject':'Confirm Email',
            'body':body,
            'to_email':validated_data.get("email")
        }
        Util.send_email(data)
        #TO DO: set redis
        user.otp = otp
        user.save()
        return user