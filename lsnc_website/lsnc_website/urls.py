"""lsnc_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static  # 配置MEDIA资源路由
from django.contrib import admin
from django.urls import path, include, re_path
from user import views as user_views
from dtoken import views as token_views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/users', user_views.users),
    path('v1/users/', include('user.urls')),
    path('v1/tokens', token_views.tokens),
    path('v1/goods/', include('goods.urls')),
    path('v1/carts/', include('carts.urls')),
    path('v1/orders', include('order.urls')),
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}, name='media')
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
