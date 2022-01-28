from django.urls import path

from . import views

urlpatterns = [
    path('login', views.user_login, name='login'),
    path('verify-token', views.verify_jwt)
]
