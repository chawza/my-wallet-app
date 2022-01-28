from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)


class UserAccount(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
