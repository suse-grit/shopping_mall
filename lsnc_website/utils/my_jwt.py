import json
import time
import base64
import hmac
import copy


class Jwt:
    def __init__(self):
        pass

    @staticmethod
    def encode(self_payload, key, exp=300):
        '''
        将json对象转化为根据秘钥key换算后的token
        :param self_payload: 私有声明（Python字典）
        :param key: 秘钥key（字符串）
        :param exp: 过期时间（int）
        :return: token
        '''
        # 1.第一部分
        header = {'alg': 'HS256', 'typ': 'JWT'}
        # 转换为json对象的字符串,并去掉字典分隔符两边多余空格,将json的key是有序的,避免由于无序时导致hash运算出现雪崩效应
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        header_bs = Jwt.b64encode(header_json.encode())
        # 2.第二部分(尽量不污染用户的数据,采用深拷贝复制用户传入的私有申明)
        payload = copy.deepcopy(self_payload)
        payload['exp'] = exp + time.time()
        payload_json = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        payload_bs = Jwt.b64encode(payload_json.encode())
        # 3.第三部分
        hm = hmac.new(key.encode(), header_bs + b'.' + payload_bs, digestmod='SHA256')
        hm_bs = Jwt.b64encode(hm.digest())
        result = header_bs + b'.' + payload_bs + b'.' + hm_bs
        return result

    @staticmethod
    def b64encode(j_s):
        '''
        base64转码,基于base64转码,去掉转码后多余的‘=’,减少带宽
        :param j_s: 需要转码的字节串
        '''
        return base64.urlsafe_b64encode(j_s).replace(b'=', b'')

    @staticmethod
    def b64decode(j_s):
        '''
        base64解码
        :param j_s: base64转码后的字节串(已去掉’=‘)
        :return: 原字节串
        '''
        rem = len(j_s) % 4
        if rem > 0:
            j_s += b'=' * (4 - rem)
        return base64.urlsafe_b64decode(j_s)

    @staticmethod
    def decode(token, key):
        '''
        Jwt的token验证
        :param token: 根据秘钥key计算而来的token
        :param key: 秘钥key
        :return: 验证结果
        '''
        header_bs, payload_bs, sign_bs = token.split(b'.')
        hm = hmac.new(key.encode(), header_bs + b'.' + payload_bs, digestmod='SHA256')
        if sign_bs != Jwt.b64encode(hm.digest()):
            # 签名如果不一致,则证明token有问题
            raise
        else:
            # 签名一致的情况下,验证token是否过期
            payload_js = Jwt.b64decode(payload_bs)
            payload = json.loads(payload_js)
            exp = payload['exp']
            if time.time() - exp > 0:
                raise
        return payload


if __name__ == '__main__':
    key = 'mi_ma'
    pay_load = {'user_name': 'gmy',
                'exp': 300}
    result = Jwt.encode(self_payload=pay_load, key=key)
    print(result)