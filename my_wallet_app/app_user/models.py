from django.db import models
from wallet.models import UserAccount
# from django.apps import apps
# UserAccount = apps.get_model('wallet', 'UserAccount')


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
