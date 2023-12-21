from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    