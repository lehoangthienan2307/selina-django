from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from selinaapp.old.authentication_serializer import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserSerializer(request.user, fields=('id', 'email', 'fullname'))
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':{'non_fields_errors':['Email or password not valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        

class PasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = PasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class PasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = PasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        serializer.update(serializer.user, serializer.validated_data)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)