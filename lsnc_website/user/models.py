from django.db import models


# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=11, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(verbose_name='手机号码', max_length=11)
    is_active = models.BooleanField(verbose_name='是否激活', default=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'user_user_profile'


class Address(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # 建立外键(一对多)
    receiver = models.CharField(verbose_name='收件人', max_length=11)
    province = models.CharField(verbose_name='省', max_length=11)
    city = models.CharField(verbose_name='市', max_length=11)
    county = models.CharField(verbose_name='县', max_length=11)
    detail = models.CharField(verbose_name='详细地址', max_length=80)
    postcode = models.CharField(verbose_name='邮政编码', max_length=6)
    receiver_phone = models.CharField(verbose_name='手机号', max_length=11)
    tag = models.CharField(verbose_name='标签', max_length=10)
    is_active = models.BooleanField(verbose_name='是否活跃', default=True)
    is_default = models.BooleanField(verbose_name='是否为默认地址', default=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'user_address'


class WeiBoProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True)
    wb_uid = models.CharField(verbose_name='微博用户id', max_length=10, unique=True)
    access_token = models.CharField(verbose_name='权限令牌', max_length=32)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        db_table = 'user_wei_bo_profile'
