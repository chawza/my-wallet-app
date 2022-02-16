from django.urls import path

from . import views

urlpatterns = [
    path('user/profile', views.user_profile, name='User profile endpoint'),
    path('transactions', views.transactions, name='Transaction CRUD endpoint'),
    path('user-account', views.get_user_account_endpoint, name='fetch user account endpoint')
]
