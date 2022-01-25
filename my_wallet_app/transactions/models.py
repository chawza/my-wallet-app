from pyexpat import model
from django.db import models

class Transactions(models.Model):
    account_id = models.ForeignKey('app_user.UserAccount', on_delete=models.CASCADE)
    category = models.CharField(max_length=256)
    currency = models.CharField(max_length=256)
    amount = models.IntegerField()
    type = models.CharField(max_length=256)
    note = models.TextField()
    date = models.DateTimeField()
    is_transfer = models.BooleanField(default=False)