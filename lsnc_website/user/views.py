import json
import hashlib
import random
import base64
import requests
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from .models import UserProfile, Address, WeiBoProfile
from dtoken.views import make_token
from django.core import mail
from django.core.cache import cache
from lsnc_website.celery import app
from utils.login_dec import login_check, login_check_fun
from django.conf import settings
# 将字典转化为查询字符串格式
from urllib.parse import urlencode


# Create your views here.
def users(request):
    '''
    用户注册视图函数
    '''
    json_str = request.body  # 提取请求对象的json串
    json_obj = json.loads(json_str)  # 将json串转化为Python对象
    username = json_obj['username']
    password = json_obj['password']
    phone = json_obj['phone']
    email = json_obj['email']
    old_user = UserProfile.objects.filter(username=username)
    if old_user:
        result = {'code': 10100, 'error': '用户名已存在,请重新注册！'}
        return JsonResponse(result)
    # 密码处理
    m = hashlib.md5()
    m.update(password.encode())
    m_password = m.hexdigest()
    # 用户数据插入
    try:
        UserProfile.objects.create(username=username, password=m_password, phone=phone, email=email)
    except Exception as e:
        print(e)
        result = {'code': 10100, 'error': '用户名已存在,请重新注册！'}
        return JsonResponse(result)
    # 签发token
    token = make_token(username=username)  # 返回的是字节串的token
    print(token)
    result = {'code': 200,
              'username': username,
              'data': {'token': token.decode()},
              'carts_count': 0}
    # 发送激活邮件(二次开发)
    try:
        send_active_email.delay(username, email=email)  # 通过celery执行该函数
    except Exception as e:
        print(e)
    return JsonResponse(result)


def active_view(request):
    '''
    激活视图函数(确认校验完成后,删除redis中的KEY)
    '''
    code = request.GET.get('code')
    if not code:
        return JsonResponse({'code': 10104, 'error': '你的激活链接无效！'})
    # 获取提交的激活链接中的用户名和激活码
    code_str = base64.urlsafe_b64decode(code.encode()).decode()
    print(type(code_str))
    username, post_code = code_str.split('_')
    cache_key = 'email_active_{}'.format(username)
    # 获取cache中的随机激活码
    old_code = cache.get(cache_key)
    print(type(old_code))
    if not old_code:
        return JsonResponse({'code': 10105, 'error': '你的激活链接已过期！'})
    if old_code != post_code:
        return JsonResponse({'code': 10106, 'error': '你的激活链接无效！'})
    try:
        user = UserProfile.objects.get(username=username, is_active=False)
        user.is_active = True
        user.save()
        # 激活完成后删除redis中的KEY
        cache.delete(cache_key)
    except Exception as e:
        print(e)
        return JsonResponse({'code': 10107, 'error': '你的激活链接无效！'})
    return JsonResponse({'code': 200, 'data': 'OK'})


@app.task
def send_active_email(username, email):
    '''
    发送激活邮件
    :param username: 用户名
    '''
    mail_link = generate_mail_link(username)  # 生成邮件链接
    subject = '绿色农产直销网'
    html_message = '''
    亲爱的用户你好,欢迎注册绿色农产直销网,请点击以下链接进行激活<该链接有效期3天>：
    <h3><a href="{}" target="_blank">点击此处</a></h3>
    '''.format(mail_link)
    mail.send_mail(subject=subject,
                   message='',
                   from_email='1129212285@qq.com',
                   recipient_list=[email],
                   html_message=html_message)


def generate_mail_link(username):
    '''

    :param username: 用户名
    :return: 邮件链接
    '''
    random_code = str(random.randint(1000, 9999))
    code_str = '{}_{}'.format(username, random_code)
    b64_code = base64.urlsafe_b64encode(code_str.encode()).decode()
    cache.set('email_active_{}'.format(username), random_code)
    verify_url = 'http://127.0.0.1:7000/templates/active.html?code={}'.format(b64_code)
    return verify_url


# CBV 基于类的视图(用户地址管理)
class AddressView(View):
    # 登录验证
    @login_check
    def get(self, request, username):
        # http://127.0.0.1:8000/v1/users/gmy1/address
        '''
        地址获取视图
        '''
        user = request.login_user
        if user.username != username:
            return JsonResponse({'code': 403, 'error': 'please login'})
        all_address = Address.objects.filter(user_profile=user, is_active=True)
        address_list = []
        for address in all_address:
            address_dict = {}
            address_dict['id'] = address.id
            address_dict['address'] = '{}{}{}{}'.format(address.province, address.city, address.county, address.detail)
            address_dict['receiver'] = address.receiver
            address_dict['receiver_mobile'] = address.receiver_phone
            address_dict['tag'] = address.tag
            address_dict['postcode'] = address.postcode
            address_dict['is_default'] = address.is_default
            address_list.append(address_dict)
        return JsonResponse({'code': 200, 'addresslist': address_list})

    @login_check
    def post(self, request, username):
        '''
        地址新增视图
        '''
        json_str = request.body
        json_obj = json.loads(json_str)
        # 取出元素
        receiver = json_obj['receiver']
        province = json_obj['province']
        city = json_obj['city']
        county = json_obj['county']
        detail = json_obj['detail']
        receiver_phone = json_obj['receiver_phone']
        postcode = json_obj['postcode']
        tag = json_obj['tag']
        login_user = request.login_user
        # 判断用户是否已有地址数据
        old_address = Address.objects.filter(user_profile=login_user, is_active=True)
        is_default = False
        if not old_address:
            is_default = True
        login_user.address_set.create(receiver=receiver, receiver_phone=receiver_phone,
                                      province=province, city=city,
                                      county=county, detail=detail,
                                      postcode=postcode, tag=tag,
                                      is_default=is_default)
        return JsonResponse({'code': 200, 'data': '新增地址成功'})

    @login_check
    def put(self, request, username, address_id):
        '''
        更新地址视图
        {"address":"北京市北京市市辖区东城区阿萨德",
        "receiver":"爱仕达所",
        "tag":"宿舍1",
        "receiver_mobile":"15182623583",
        "id":10}
        '''
        login_user = request.login_user
        if login_user.username != username:
            return JsonResponse({'code': 403, 'error': 'please login'})
        json_str = request.body
        json_obj = json.loads(json_str)
        addr_id = json_obj['id']
        if addr_id != address_id:
            return JsonResponse({'code': 20102, 'error': 'your modify is error!'})
        address_detail = json_obj['address']
        receiver = json_obj['receiver']
        tag = json_obj['tag']
        receiver_phone = json_obj['receiver_mobile']
        try:
            addr = Address.objects.get(id=addr_id, user_profile=login_user, is_active=True)
            addr.detail = address_detail
            addr.receiver = receiver
            addr.tag = tag
            addr.receiver_phone = receiver_phone
            addr.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 20103, 'error': 'your modify is error!'})
        return JsonResponse({'code': 200, 'data': '地址修改成功!'})

    @login_check
    def delete(self, request, username, address_id):
        '''
        删除地址视图
        '''
        # /v1/users/gmy1/address/1
        login_user = request.login_user
        if login_user.username != username:
            return JsonResponse({'code': 403, 'error': 'please login'})
        json_str = request.body
        json_obj = json.loads(json_str)
        addr_id = json_obj['id']
        if address_id != addr_id:
            return JsonResponse({'code': 20210, 'error': 'delete error!'})
        try:
            addr = Address.objects.get(id=addr_id, user_profile=login_user)
            addr.is_active = False
            if addr.is_default:
                addr.is_default = False
                addr.save()
                adds = Address.objects.filter(user_profile=login_user, is_active=True)
                if adds:
                    new_default = adds[0]
                    new_default.is_default = True
                    new_default.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code': 20211, 'error': 'delete error!'})
        return JsonResponse({'code': 200, 'data': '删除地址成功!'})


@login_check_fun
def default_address_view(request, username):
    '''
    设置默认地址视图
    '''
    login_user = request.login_user
    if login_user.username != username:
        return JsonResponse({'code': 403, 'error': 'please login'})
    addr_id = json.loads(request.body)['id']
    try:
        addr = Address.objects.get(user_profile=login_user, id=addr_id, is_active=True)
        if addr.is_default:
            return JsonResponse({'code': 20104, 'error': '亲,这个地址已经是默认地址了!'})
        old_default = Address.objects.get(user_profile=login_user, is_active=True, is_default=True)
        addr.is_default = True
        old_default.is_default = False
        addr.save()
        old_default.save()
    except Exception as e:
        print(e)
        return JsonResponse({'code': 20105, 'error': 'your default set is invalid!'})
    return JsonResponse({'code': 200, 'data': '亲,设置默认地址完成!'})


# 微博第三方登录
def weibo_url_view(request):
    '''
    给前端返回微博授权页的uri
    '''
    wei_bo_url = 'https://api.weibo.com/oauth2/authorize'
    params = {'client_id': settings.WEIBO_APP_KEY,
              'response_type': 'code',
              'redirect_uri': settings.WEIBO_REDIRECT_URI}
    url = wei_bo_url + '?' + urlencode(params)
    return JsonResponse({'code': 200, 'oauth_url': url})


class WeiBoUserView(View):
    def get(self, request):
        '''
        根据前端返回的授权码换取token
        '''
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code': 10107, 'error': '你的授权信息有误!'})
        token_url = 'https://api.weibo.com/oauth2/access_token'
        # 向微博服务器发出post请求,用code换取token,https://api.weibo.com/oauth2/access_token
        request_data = {
            'client_id': settings.WEIBO_APP_KEY,
            'client_secret': settings.WEIBO_APP_SECRET,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.WEIBO_REDIRECT_URI,
            'code': code
        }
        response = requests.post(token_url, data=request_data)
        if response.status_code == 200:
            json_data = json.loads(response.text)
        else:
            return JsonResponse({'code': 10108, 'error': '新浪服务器比较繁忙,请稍后重试!'})
        weibo_uid = json_data['uid']
        access_token = json_data['access_token']
        try:
            weibo_user = WeiBoProfile.objects.get(wb_uid=weibo_uid)
        except Exception as e:
            # 该微博账号第一次登录
            WeiBoProfile.objects.create(access_token=access_token, wb_uid=weibo_uid)
            # 返回微博uid信息给前端
            return JsonResponse({'code': 201, 'uid': weibo_uid})
        else:
            # 检查是否绑定注册过
            # 1.如果绑定过,正常返回
            user = weibo_user.user_profile
            if user:
                username = user.username
                token = make_token(username=username)
                return JsonResponse({'code': 200, 'username': username, 'token': token.decode()})
            else:
                # 2.如果没有绑定注册过
                return JsonResponse({'code': 201, 'uid': weibo_uid})

    def post(self, request):
        # 微博用户绑定注册关联模块
        json_obj = json.loads(request.body)
        uid = json_obj['uid']
        username = json_obj['username']
        password = json_obj['password']
        phone = json_obj['phone']
        email = json_obj['email']
        # 密码处理
        m = hashlib.md5()
        m.update(password.encode())
        # 生成原始对象,绑定微博账号的外键(采用数据库的事物控制)
        try:
            # 触发数据库事物控制
            with transaction.atomic():
                user = UserProfile.objects.create(username=username,
                                                  password=m.hexdigest(),
                                                  email=email,
                                                  phone=phone)
                weibo_user = WeiBoProfile.objects.get(wb_uid=uid)
                weibo_user.user_profile = user
                weibo_user.save()
        except Exception as e:
            return JsonResponse({'code': 10109, 'error': '服务器繁忙,请稍后重试!'})
        token = make_token(username=username)
        return JsonResponse({'code': 200, 'username': username, 'token': token.decode()})
