import json

from http import HTTPStatus
from pathlib import Path
from base64 import b64encode, b64decode
from uuid import uuid4
from subprocess import call
from traceback import print_exc
from django.http import request
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

@csrf_exempt
def user_login(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        params = load_json(request.body)
        account = params['account']
        password = params['password']
        if User.objects.filter(email=account).exists():
            user = User.objects.get(email=account)            
            user = auth.authenticate(username=user.username, password=password)
            if user is not None and user.is_active:
                try:
                    token = Token.objects.get(user=user)
                    token.delete()
                    token = Token.objects.create(user=user)
                except:
                    token = Token.objects.create(user=user)       
                auth.login(request, user)
                print(token)
                return JsonResponse({
                    'code': 'LOGIN_SUCCESS',
                    'message': 'LOGIN Success.',
                    'token': token.key
                }, status=HTTPStatus.OK)
            else:
                return JsonResponse({
                    'code': 'LOGIN_FAILED',
                    'message': 'LOGIN Failed.',
                }, status=HTTPStatus.OK)
        else:
            return JsonResponse({
                'code': 'ACCOUNT_NOT_EXIST',
                'message': 'LOGIN Failed.',
            }, status=HTTPStatus.OK)

@csrf_exempt
def user_logout(request):
    auth.logout(request)
    return JsonResponse({
        'code': 'LOGOUT_SUCCESS',
        'message': 'LOGOUT Success.',
    }, status=HTTPStatus.OK)

@csrf_exempt
def user_regist(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        params = load_json(request.body)
        name = params['name']
        password = params['password']
        email = params['email']
        print(name, password, email)
        User.objects.create_user(username=name, password=password, email=email)       
        return JsonResponse({
            'code': 'USER_REGIST_SUCCESS',
            'message': 'Regist User Success.',
        }, status=HTTPStatus.OK)

def load_json(data):
    return json.loads(data.decode("UTF-8"))