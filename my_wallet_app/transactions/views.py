import json
from datetime import datetime, timedelta
from dateutil import parser

from django.http.request import HttpRequest
from django.http import response

from .models import Transactions
from app_user.models import UserAccount


def _parse_to_datetime(timestamp: str) -> datetime:
    return parser.parse(timestamp)


def _calculate_time_range(params):
    today = datetime.today()
    if 'start_date' in params:
        start_date = _parse_to_datetime(params.get('start_date'))
    else:
        start_date = today - timedelta(days=30)

    if 'end_date' in params:
        end_date = _parse_to_datetime(params.get('end_date'))
    else:
        end_date = today
    if end_date < start_date:
        raise Exception(f'{start_date.__str__()} is BEFORE {end_date.__str__()}!')
    return start_date, end_date


def get_all_user_transactions(request: HttpRequest):
    if request.method == 'GET':
        try:
            start_date, end_date = _calculate_time_range(request.GET)

            query = Transactions.objects \
                .filter(account__user_id=request.user.id) \
                .filter(date__gte=start_date, date__lte=end_date) \
                .order_by('date')

            data = list(query.values())

            for idx, row in enumerate(data):
                row['account'] = UserAccount.objects.get(id=row['account_id']).name
                del row['account_id']

        except parser.ParserError:
            return response.HttpResponseBadRequest('Cannot parse datetime parameter(s)')

        except Exception as error:
            return response.HttpResponseBadRequest(error)

        payload = {'transactions': data}
        return response.JsonResponse(payload)

    return response.HttpResponseBadRequest('Invalid Method')
