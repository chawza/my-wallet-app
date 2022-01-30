from django.urls import path

from . import views

urlpatterns = [
    path('user', views.get_all_user_transactions, name='fetch all user\'s transactions')
]
