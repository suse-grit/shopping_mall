from .my_jwt import Jwt
from django.http import JsonResponse
from django.conf import settings
from user.models import UserProfile


# 登录验证
def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        # 获取用户本地存储的token数据,请求头中获取数据
        token = request.META.get('HTTP_AUTHORIZATION')
        # 如果没有token
        if not token:
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        try:
            pay_load = Jwt.decode(token.encode(), settings.JWT_TOKEN_KEY)
        except Exception as e:
            print(e)
            result = {'code': 403, 'error': 'your token is invalid!'}
            return JsonResponse(result)
        try:
            username = pay_load['username']  # 取出payload中username部分
            user = UserProfile.objects.get(username=username)
            request.login_user = user
        except Exception as e:
            print(e)
            result = {'code': 403, 'error': 'your token is invalid!'}
            return JsonResponse(result)
        return func(self, request, *args, **kwargs)

    return wrapper


def login_check_fun(func):
    def wrapper(request, *args, **kwargs):
        # 获取用户本地存储的token数据,请求头中获取数据
        token = request.META.get('HTTP_AUTHORIZATION')
        # 如果没有token
        if not token:
            result = {'code': 403, 'error': 'please login'}
            return JsonResponse(result)
        try:
            pay_load = Jwt.decode(token.encode(), settings.JWT_TOKEN_KEY)
        except Exception as e:
            print(e)
            result = {'code': 403, 'error': 'your token is invalid!'}
            return JsonResponse(result)
        try:
            username = pay_load['username']  # 取出payload中username部分
            user = UserProfile.objects.get(username=username)
            request.login_user = user
        except Exception as e:
            print(e)
            result = {'code': 403, 'error': 'your token is invalid!'}
            return JsonResponse(result)
        return func(request, *args, **kwargs)

    return wrapper
