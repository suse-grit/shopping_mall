from django.conf.urls import url
from . import views

urlpatterns = [
    # 各种状态订单信息的查询，订单的生成，订单状态的修改
    url(r'^(?P<username>[\w]{1,11})$', views.OrderInfoView.as_view()),
    # 预订单即确认订单信息
    url(r'^(?P<username>[\w]{1,11})/advance$', views.AdvanceOrderView.as_view()),
]
