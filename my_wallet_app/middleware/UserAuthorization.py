import json
from django.http.response import HttpResponseNotAllowed
from django.http.request import HttpRequest
from app_user.models import User
import jwt


def _get_rsa_public_key():
    filepath = 'rsa_public.pem'
    with open(filepath, 'rb') as file:
        public_key = file.read()
    return public_key.decode()


def _verify_jwt_token(token: str):
    jwt_token = token.split(' ')[1]
    public_key = _get_rsa_public_key()
    payload = jwt.decode(jwt_token, public_key, ["RS256"])
    return payload


class UserAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.response_reject_message = 'Not Authorized'
        self.rejectResponse = HttpResponseNotAllowed(json.dumps({"message": self.response_reject_message}))

    def __call__(self, request: HttpRequest):
        # ignore auth app
        if request.path.startswith('/auth'):
            return self.get_response(request)

        if 'Authorization' not in request.headers:
            return self.rejectResponse
        try:
            payload = _verify_jwt_token(request.headers['Authorization'])
            user = User.objects.get(username=payload['username'])
            request.user = user
        except User.DoesNotExist:
            return self.rejectResponse

        response = self.get_response(request)
        return response
