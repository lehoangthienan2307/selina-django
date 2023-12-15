from rest_framework import serializers
from selinaapp.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'fullname', 'password', 'password2', 'phone', 'gender']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password not match")     
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)