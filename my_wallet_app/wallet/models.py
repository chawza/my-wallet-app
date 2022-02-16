from django.db import models


class UserAccount(models.Model):
    user = models.ForeignKey('app_user.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)


class Transactions(models.Model):
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    currency = models.CharField(max_length=256, default='IDR')
    amount = models.IntegerField()
    type = models.CharField(max_length=256)
    note = models.TextField(default='')
    date = models.DateTimeField()
    is_transfer = models.BooleanField(default=False)
