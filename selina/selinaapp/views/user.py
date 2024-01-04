from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from selinaapp.serializers.user.change_password_serializer import ChangePasswordSerializer
from selinaapp.serializers.user.login_serializer import LoginSerializer
from selinaapp.serializers.user.password_reset_email_serializer import PasswordResetEmailSerializer
from selinaapp.serializers.user.register_serializer import RegisterSerializer
from selinaapp.serializers.user.user_serializer import UserSerializer
from selinaapp.serializers.user.edit_profile_serializer import EditProfileSerializer
from selinaapp.serializers.user.password_reset_serializer import PasswordResetSerializer
from selinaapp.serializers.user.register_verification_serializer import RegisterVerificationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from selinaapp.models.user import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }

class UserViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'message': 'Email đã tồn tại', 'status_code': 4}, status=status.HTTP_200_OK)
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Đăng kí thành công', 'status_code': 1}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'msg':str(e)}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        try:
            serializer = UserSerializer(request.user, fields=('email', 'fullname', 'phone', 'address', 'gender', 'avatar_url'))
            return Response({'data':serializer.data, 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_200_OK)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                
                if user.status == 'pending':
                    return Response({'data':'unverified_account','message':'Tài khoản chưa được kích hoạt','status_code': 4}, status=status.HTTP_200_OK)
                
                if user.status == 'banned':
                    return Response({'data':'account_banned','message':'Tài khoản bị khóa','status_code': 4}, status=status.HTTP_200_OK)
                
                user_data = UserSerializer(user, fields=('id', 'fullname', 'phone', 'email', 'device_token', 'avatar_url', 'user_type', 'status', 'gender', 'address'))
                token['user_data'] = user_data.data
                
                return Response({'data':token,'message':'Đăng nhập thành công','status_code': 1}, status=status.HTTP_200_OK)
            else:
                return Response({'data':'email_no_exists','message':'Tài khoản hoặc mật khẩu không hợp lệ','status_code': 4}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='change-password')
    def change_password(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_200_OK)
            serializer.update(request.user, serializer.validated_data)
            return Response({'data':serializer.data, 'message':'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='send-reset-password-email')
    def send_reset_password_email(self, request):
        try:
            serializer = PasswordResetEmailSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({'data':'email_does_not_match','message':serializer.errors["email"][0],'status_code': 4}, status=status.HTTP_200_OK)
            serializer.update(serializer.user, serializer.validated_data)
            return Response({'data':'password_sent','message':'Đã gửi mật khẩu','status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':'system_error','message':str(e),'status_code': 5}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='reset-password/(?P<uid64>\w+)/(?P<token>[\w-]+)')
    def reset_password(self, request, **kwargs):
        try:
            uid64 = kwargs.get('uid64')
            token = kwargs.get('token')
            serializer = PasswordResetSerializer(data=request.data, context={'uid64':uid64, 'token':token})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_200_OK)
            serializer.update(serializer.user, serializer.validated_data)
            return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':e}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='approve-account')
    def approve_account(self, request):
        try:
            serializer = RegisterVerificationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_200_OK)
            serializer.update(serializer.user, serializer.validated_data)
            return Response({'message': 'Email verification Successful', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='logout')
    def logout(self, request):
        try:
            #request.user.auth_token.delete()
            access_token = request.META.get('HTTP_AUTHORIZATION')
            print("check1 " + str(access_token))
            #print("check " + request.user.auth_token)
            return Response({'message': 'Đăng xuất thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'message':str(e)}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], url_path='modify-personal-info')
    def modify_personal_info(self, request):
        try:
            serializer = EditProfileSerializer(instance = request.user, data=request.data, partial=True)
            
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'data':serializer.errors, 'message':'That bai', 'status_code': 4}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'data':serializer.data, 'message':'Thành công', 'status_code': 1}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({'data':str(e), 'message':'Lỗi', 'status_code': 4}, status=status.HTTP_200_OK)
        
    