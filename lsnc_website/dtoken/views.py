import json
import time
import hashlib
from django.http import JsonResponse
from django.conf import settings
from utils.my_jwt import Jwt
from user.models import UserProfile


# Create your views here.
def tokens(request):
    # 获取json_obj
    json_str = request.body
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    # 用户名和密码校验
    if not username:
        return JsonResponse({'code': 10200, 'error': '输入用户名为空,请重新输入！'})
    password = json_obj.get('password')
    if not password:
        return JsonResponse({'code': 10201, 'error': '输入用户名为空,请重新输入！'})
    # 查询用户是否存在
    try:
        user = UserProfile.objects.get(username=username)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 10202, 'error': '用户名或密码输入错误,请重新输入'})
    # 密码校验
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        return JsonResponse({'code': 10203, 'error': '用户名或密码输入错误,请重新输入！'})
    # 签发token
    token = make_token(username=username)
    result = {
        'code': 200,
        'username': username,
        'data': {'token': token.decode()},
        'carts_count': 0
    }
    return JsonResponse(result)


def make_token(username, expire=3600 * 24):
    '''
    token制作
    '''
    now = time.time()
    payload = {
        'username': username,
        'exp': int(now + expire)
    }
    key = settings.JWT_TOKEN_KEY
    return Jwt.encode(self_payload=payload, key=key, exp=expire)
