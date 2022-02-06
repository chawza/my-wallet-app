from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('user/', include('app_user.urls')),
    path('wallet/', include('wallet.urls')),
    path('admin/', admin.site.urls),
]
