from django.db import models
from django.apps import apps
from transactions.models import Transactions


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)

    def find_account_by_id(self, account_id):
        for account in self.get_all_accounts():
            if account.id == account_id:
                return account
        raise UserAccount.DoesNotExist(account_id)

    def get_all_accounts(self):
        return UserAccount.objects.filter(user_id=self.id)


class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
