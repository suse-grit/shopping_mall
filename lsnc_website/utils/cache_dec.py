from django.core.cache import caches

goods_detail = None


# @cache_check(key_prefix='gd', key_param='sku_id', cache='goods_detail',expire=60)
# 能接受参数的装饰器(详情页与首页必须要分开缓存)
def cache_check(**cache_kwargs):
    def _cache_check(func):
        def wrapper(self, request, *args, **kwargs):
            CACHE = caches['default']
            if 'cache' in cache_kwargs:
                CACHE = caches[cache_kwargs['cache']]  # 如果views指定缓存位置
            key_prefix = cache_kwargs['key_prefix']
            key_param = cache_kwargs['key_param']
            expire = cache_kwargs.get('expire', 120)
            if key_param not in kwargs:
                raise ValueError('your key_param is not in kwargs')
            cache_key = key_prefix + str(kwargs[key_param])  # 拼出缓存中详情页的具体的cache_key
            result = CACHE.get(cache_key)
            if result:
                return result
            # 如果没有缓存<走视图函数>
            res = func(self, request, *args, **kwargs)
            CACHE.set(cache_key, res, expire)
            return res

        return wrapper

    return _cache_check
