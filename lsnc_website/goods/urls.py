from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # /v1/goods/catalogs/1
    path('catalogs/<int:catalog_id>', cache_page(600, cache='goods')(views.GoodsListView.as_view())),
    # cache_page(timeout='缓存时间', cache='settings.py中缓存配置中的key')
    path('index', cache_page(600, cache='goods')(views.GoodsIndexView.as_view())),
    path('detail/<int:sku_id>', views.GoodsDetailView.as_view())
]
