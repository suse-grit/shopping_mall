from django.urls import path
from . import views

urlpatterns = [
    path('activation', views.active_view),
    # 调用as_view方法转化为了视图函数处理请求
    path('<str:username>/address', views.AddressView.as_view()),
    path('<str:username>/address/<int:address_id>', views.AddressView.as_view()),
    # /v1/users/gmy1/address/default  设置默认地址的URI
    path('<str:username>/address/default', views.default_address_view),
    # /v1/users/weibo/authorization
    path('weibo/authorization', views.weibo_url_view),
    # /v1/users/weibo/users","query":{"code":"b62b8759272a85efd7d4044bfbaa1b70"}
    path('weibo/users', views.WeiBoUserView.as_view())
]
