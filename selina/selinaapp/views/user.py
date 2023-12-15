from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from selinaapp.serializers.user.change_password_serializer import ChangePasswordSerializer
from selinaapp.serializers.user.login_serializer import LoginSerializer
from selinaapp.serializers.user.password_reset_email_serializer import PasswordResetEmailSerializer
from selinaapp.serializers.user.register_serializer import RegisterSerializer
from selinaapp.serializers.user.user_serializer import UserSerializer
from selinaapp.serializers.user.password_reset_serializer import PasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        try:
            serializer = UserSerializer(request.user, fields=('id', 'email', 'fullname'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error':{'non_fields_errors':['Email or password not valid']}}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='change-password')
    def change_password(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(request.user, serializer.validated_data)
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='send-reset-password-email')
    def send__reset_password_email(self, request):
        try:
            serializer = PasswordResetEmailSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='reset-password/(?P<uid64>\w+)/(?P<token>[\w-]+)')
    def reset_password(self, request, **kwargs):
        try:
            uid64 = kwargs.get('uid64')
            token = kwargs.get('token')
            serializer = PasswordResetSerializer(data=request.data, context={'uid64':uid64, 'token':token})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.update(serializer.user, serializer.validated_data)
            return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)