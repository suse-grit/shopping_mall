from django.contrib import admin
from .models import *
from django.core.cache import caches

GOODS_CACHE = caches['goods']

# Register your models here.


GOODS_CACHES = caches['goods']
GD_CACHES = caches['goods_detail']


class BaseModel(admin.ModelAdmin):
    """
    继承admin.ModelAdmin
    重写save_model / delete_model 方法
    """

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 删除首页缓存
        GOODS_CACHES.clear()
        print("保存数据时，首页缓存删除")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 删除首页缓存
        GOODS_CACHES.clear()
        print("删除数据时，首页缓存删除")

    def delete_goods_detail_cache(self, sku_id):
        cache_key = 'good_detail_{}'.format(sku_id)
        GD_CACHES.delete(cache_key)


@admin.register(Brand)
class BrandAdmin(BaseModel):
    list_display = ['id', 'name']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)


@admin.register(Catalog)
class CatalogAdmin(BaseModel):
    list_display = ['id', 'name']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)


@admin.register(SPU)
class SPUAdmin(BaseModel):
    list_display = ['id', 'name', 'catalog']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('catalog',)

    search_fields = ('name',)  # 搜索字段


@admin.register(SPUSaleAttr)
class SPUSaleAttrAdmin(BaseModel):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 删除首页缓存
        GOODS_CACHES.clear()
        # 删除spu对应的sku缓存
        all_sku_ids = obj.spu.sku_set.values('id')
        for sid in all_sku_ids:
            _id = sid['id']
            self.delete_goods_detail_cache(_id)
        print("保存数据时，首页缓存删除，详情页缓存删除")

    def delete_model(self, request, obj):
        all_sku_ids = obj.spu.sku_set.values('id')
        super().delete_model(request, obj)
        # 删除首页缓存
        GOODS_CACHES.clear()
        # 删除spu对应的sku缓存
        for sid in all_sku_ids:
            _id = sid['id']
            self.delete_goods_detail_cache(_id)
        print("保存数据时，首页缓存删除，详情页缓存删除")

    list_display = ['id', 'spu', 'name']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('spu',)

    search_fields = ('name',)  # 搜索字段


@admin.register(SKU)
class SKUAdmin(BaseModel):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        GOODS_CACHES.clear()
        self.delete_goods_detail_cache(obj.id)
        print("保存数据时，首页缓存删除，详情页缓存删除")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 删除首页缓存
        GOODS_CACHES.clear()
        self.delete_goods_detail_cache(obj.id)
        print("保存数据时，首页缓存删除，详情页缓存删除")

    list_display = ['id', 'name', 'spu', 'is_launched', ]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('spu',)

    search_fields = ('name',)  # 搜索字段


@admin.register(SaleAttrValue)
class SaleAttrValueAdmin(BaseModel):
    list_display = ['id', 'name', 'spu_sale_attr', ]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('spu_sale_attr',)

    search_fields = ('name',)  # 搜索字段


@admin.register(SKUImage)
class SKUImageAdmin(BaseModel):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 删除详情页缓存
        self.delete_goods_detail_cache(obj.sku.id)
        print("sku.id", obj.sku.id)
        print("保存数据时，详情页缓存清除")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 删除详情页缓存
        self.delete_goods_detail_cache(obj.sku.id)
        print("sku.id", obj.sku.id)
        print("保存数据时，详情页缓存清除")

    list_display = ['id', 'sku', 'image', ]
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('sku',)


@admin.register(SPUSpec)
class SPUSpecAdmin(BaseModel):
    list_display = ['id', 'spu', 'name']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('spu',)

    search_fields = ('name',)  # 搜索字段


@admin.register(SKUSpecValue)
class SKUSpecValueAdmin(BaseModel):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 删除详情页缓存
        self.delete_goods_detail_cache(obj.sku.id)
        print("sku.id", obj.sku.id)
        print("保存数据时，详情页缓存清除")

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        # 删除详情页缓存
        self.delete_goods_detail_cache(obj.sku.id)
        print("保存数据时，详情页缓存清除")

    list_display = ['id', 'sku', 'spu_spec', 'name']

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20

    # ordering设置默认排序字段，创建时间降序排序
    ordering = ('created_time',)

    # fk_fields 设置显示外键字段
    fk_fields = ('sku', 'spu_spec')

    search_fields = ('spec_name',)  # 搜索字段
