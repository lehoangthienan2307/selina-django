
from django.urls import path, include
#from selinaapp.views.authentication_view import *
from selinaapp.views import user, book, cart, order
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', user.UserViewSet, basename='user')
router.register('book', book.BookViewSet, basename='book')
router.register('cart', cart.CartViewSet, basename='cart')
router.register('order', order.OrderViewSet, basename='order')
urlpatterns = [
   path('api/', include(router.urls))
]

# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='register'),    
#     path('login/', UserLoginView.as_view(), name='login'),
#     path('profile/', UserProfileView.as_view(), name='profile'),
#     path('change/', UserChangePasswordView.as_view(), name='changepassword'),
#     path('send-reset-password-email/', PasswordResetEmailView.as_view(), name='send-reset-password-email'),
#     path('reset-password/<uid>/<token>/', PasswordResetView.as_view(), name='reset-password'),
# ]
