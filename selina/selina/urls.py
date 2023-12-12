
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/user/', include('selinaapp.urls')),
    path('admin/', admin.site.urls),
]
