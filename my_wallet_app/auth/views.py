import json
# from django.shortcuts import render
import jwt
from django.http.request import HttpRequest
from django.http import response
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

User = apps.get_model('app_user', 'User')


def _get_rsa_private_key():
    filepath = 'rsa_private.pem'
    with open(filepath, 'rb') as file:
        private_key = file.read()
    return private_key.decode()


def _get_rsa_public_key():
    filepath = 'rsa_public.pem'
    with open(filepath, 'rb') as file:
        public_key = file.read()
    return public_key.decode()


def _create_jwt_token(username: str, user_id: int):
    signed_key = _get_rsa_private_key()
    message = {
        "username": username,
        "id": user_id
    }
    token = jwt.encode(message, signed_key, "RS256")
    return token


def _verify_jwt_token(token: str):
    public_key = _get_rsa_public_key()
    payload = jwt.decode(token, public_key, ["RS256"])
    return payload


# Create your views here.
def user_login(req: HttpRequest):
    if req.method == "POST":
        body = json.loads(req.body)
        try:
            existed_user = User.objects.get(username=body['username'])
        except ObjectDoesNotExist:
            return response.HttpResponseNotFound(json.dumps({"message": 'User not found!'}))

        if existed_user.password == body['password']:
            jwt_token = _create_jwt_token(existed_user.username, existed_user.password)
            res_body = {"token": jwt_token}
            return response.HttpResponse(json.dumps(res_body))

        return response.HttpResponseBadRequest(json.dumps({"message": "username or password is invalid"}))

    return response.HttpResponseBadRequest(json.dumps({"message": "request method Error"}))


def verify_jwt(req: HttpRequest):
    if req.method == "POST":
        body = json.loads(req.body)
        token = body['token']
        message = _verify_jwt_token(token)
        return response.HttpResponse(json.dumps(message))

    return response.HttpResponseBadRequest('Unknown request method')

