from django.db import models

# Create your models here.
from django.db import models
from utils.basemodels import BaseModel
from user.models import UserProfile, Address
from goods.models import SKU

status_choices = (
    (1, "待付款"),
    (2, "待发货"),
    (3, "待收货"),
    (4, "订单完成"),
)


class OrderInfo(BaseModel):
    """订单信息"""
    order_id = models.CharField(max_length=64, primary_key=True, verbose_name="订单号")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name="收货地址")
    total_count = models.IntegerField(default=1, verbose_name="商品总数")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品总金额")
    freight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="运费")
    pay_method = models.SmallIntegerField(default=1, verbose_name="支付方式")

    # 订单地址
    receiver = models.CharField(verbose_name=u'收件人', max_length=10, default='')
    address = models.CharField(max_length=100, verbose_name='用户地址', default='')
    receiver_mobile = models.CharField(verbose_name=u'电话', max_length=11, default='')
    tag = models.CharField(verbose_name=u'标签', max_length=10, default='', )

    status = models.SmallIntegerField(verbose_name="订单状态", choices=status_choices)

    class Meta:
        db_table = "order_order_info"
        verbose_name = '订单基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


class OrderGoods(BaseModel):
    """订单商品"""
    order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    sku = models.ForeignKey(SKU, models.CASCADE)
    count = models.IntegerField(default=1, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")

    # 以下字段为商品评价功能所用,留做2.0迭代使用
    # comment = models.TextField(default="", verbose_name="评价信息")
    # score = models.SmallIntegerField(default=5, verbose_name='满意度评分')
    # is_anonymous = models.BooleanField(default=False, verbose_name='是否匿名评价')
    # is_commented = models.BooleanField(default=False, verbose_name='是否评价了')

    class Meta:
        db_table = "order_order_goods"
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sku.name
