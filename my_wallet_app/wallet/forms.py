from django.forms import ModelForm
from .models import Transactions


class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields = ['account', 'category', 'amount', 'type', 'note', 'date']
