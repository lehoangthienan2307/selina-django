
from django.urls import path, include
from selinaapp.views.authentication_view import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),    
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', PasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', PasswordResetView.as_view(), name='reset-password'),
]
