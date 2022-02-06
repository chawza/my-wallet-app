from django.urls import path

from . import views

urlpatterns = [
    path('transactions', views.get_all_user_transactions, name='fetch all user\'s transactions'),
    path('user-account', views.get_user_account_endpoint, name='fetch user account endpoint')
]
