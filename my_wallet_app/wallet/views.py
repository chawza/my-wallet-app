from datetime import datetime, timedelta, timezone
from dateutil import parser
from django.utils.timezone import make_aware

from django.http.request import HttpRequest
from django.http import response

from .models import Transactions
from app_user.models import UserAccount
from .forms import TransactionForm


def _parse_to_datetime(timestamp: str) -> datetime:
    return make_aware(parser.parse(timestamp, ignoretz=True), timezone.utc)


def _calculate_time_range(params):
    today = datetime.now(timezone.utc)
    if 'start_date' in params:
        start_date = _parse_to_datetime(params.get('start_date').replace('"', ''))
    else:
        start_date = today - timedelta(days=30)

    if 'end_date' in params:
        end_date = _parse_to_datetime(params.get('end_date').replace('"', ''))
    else:
        end_date = today

    if end_date < start_date:
        raise Exception(f'{start_date.__str__()} is BEFORE {end_date.__str__()}!')
    return start_date, end_date


def transactions(request: HttpRequest):
    if request.method == 'GET':
        try:
            start_date, end_date = _calculate_time_range(request.GET)
            print(start_date, end_date)
            query = Transactions.objects \
                .filter(account__user_id=request.user.id) \
                .filter(date__gte=start_date, date__lte=end_date) \
                .order_by('date')

            data = list(query.values())

            for idx, row in enumerate(data):
                row['account'] = UserAccount.objects.get(id=row['account_id']).name
                del row['account_id']

            payload = {'transactions': data}
            return response.JsonResponse(payload)

        except parser.ParserError:
            return response.HttpResponseBadRequest('Cannot parse datetime parameter(s)')

    if request.method == 'POST':
        tran = TransactionForm(request.GET)
        if tran.is_valid():
            tran.save()
            return response.HttpResponse('Record Added')
        return response.HttpResponseBadRequest(tran.errors.as_json())

    return response.HttpResponseBadRequest('Invalid Method')


def get_user_account_endpoint(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = request.user
            accounts = UserAccount.objects.filter(user_id=user.id)

            payload = {'accounts': list(accounts.values('id', 'name'))}
            return response.JsonResponse(payload)

        except Exception as error:
            return response.HttpResponseBadRequest(error)

    return response.HttpResponseBadRequest('Invalid Method')


def user_profile(request: HttpRequest):
    if request.method == 'GET':
        try:
            user = request.user
            return response.JsonResponse({
                "profile": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            })

        except Exception as error:
            return response.HttpResponseBadRequest(error)

    return response.HttpResponseBadRequest('Invalid Method')
