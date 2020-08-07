from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        '''
        该模型类不会在数据库中创建实际数据表,且其它模型类可以继承该模型类
        '''
        abstract = True  # 指定该模型类为抽象模型类
