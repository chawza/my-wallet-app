from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('auth.urls')),
    path('user/', include('app_user.urls')),
    path('transactions/', include('transactions.urls')),
    path('admin/', admin.site.urls),
]
