import datetime
import json
from alipay import AliPay
from django.db import transaction
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from goods.models import SKU
from order.models import OrderInfo, OrderGoods
from user.models import Address
from carts.views import CartsView
from goods.views import get_sku_name_and_values

# 公共调用类
from utils.login_dec import login_check


class OrderBaseView(View):
    # 获取存储在购物车中的商品数据
    def get_carts_dict(self, user_id):
        carts_dict = CartsView().get_carts_datas(user_id)
        print("购物车", len(carts_dict))
        # 将选中的商品 转化成 {id:count}
        return {k: v[0] for k, v in carts_dict.items() if v[1] == 1}

    def get_direct_dict(self, sku_id, count):
        # 将直接购买传来的商品 转化成 {id:count}
        return {int(sku_id): int(count)}

    # 获取立即购买的商品列表
    def get_direct_order_list(self, skus, count=None):
        sku_list = []
        for sku in skus:
            # 获取商品属性值，商品属性名
            sku_sale_attr_val, sku_sale_attr_name = get_sku_name_and_values(sku.id)
            sku_list.append({
                'id': sku.id,
                'default_image_url': str(sku.default_image_url),
                'name': sku.name,
                'price': sku.price,
                'count': count,
                'total_amount': sku.price * int(count),
                "sku_sale_attr_name": sku_sale_attr_name,
                "sku_sale_attr_val": sku_sale_attr_val,
            })
        return sku_list

    # 从redis中删除所有已经加入了订单的商品
    def delete_redis_order(self, sku_ids, user_id):
        carts = CartsView()
        for sku_id in sku_ids:
            carts.del_carts_data(user_id, sku_id)

    # 获取用户地址
    def get_address(self, user_id):
        """
        :param request:
        :return: address_list(地址列表)
        """
        print("user:", user_id)
        addresses = Address.objects.filter(is_active=True, user_profile_id=user_id)
        print(addresses)
        addresses_default = []
        addresses_no_default = []
        for address in addresses:
            detail_address = address.province + address.city + address.county + address.detail
            address_dic = {
                "id": address.id,
                "name": address.receiver,
                "mobile": address.receiver_phone,
                "title": address.tag,
                "address": detail_address
            }
            if address.is_default:
                addresses_default.append(address_dic)
            else:
                addresses_no_default.append(address_dic)

        return addresses_default + addresses_no_default

    # 获取在购物车购买的商品列表
    def get_carts_order_list(self, user_id):
        """
        :param skus:
        :param cart_dict:
        :return: sku_list(sku列表)
        """
        sku_list = CartsView().get_carts_list(user_id)
        print(sku_list)
        return [s for s in sku_list if s['selected'] == 1]

    def get_order_string(self, order_id, total_amount, sku_goods):
        """
        :param order_id:
        :param total_amount:
        :return: order_string
        """
        trade_name = []
        for sku_good in sku_goods:
            trade_name.append(sku_good.sku.name + "(" + sku_good.sku.caption + ")")
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url-　阿里与商户后台交互
            # 使用的文件读取方式,载入支付秘钥
            app_private_key_string=open(settings.ALIPAY_KEYS_DIR + 'app_private_key.pem').read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # 使用文件读取的方式,载入支付报公钥
            alipay_public_key_string=open(settings.ALIPAY_KEYS_DIR + 'alipay_public_key.pem').read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
        # 测试方式此为支付宝沙箱环境

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=int(total_amount),
            subject=order_id,
            # 回转url,　支付宝与买家业务处理完毕(支付成功)将玩家重定向到此路由,带着交易的参数返回
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_RETURN_URL  # 可选, 不填则使用默认notify url
        )
        return order_string

    def get_make_pay_order(self, order, carts_count):
        # 4.生成支付宝支付链接
        sku_goods = OrderGoods.objects.filter(order_info=order)
        order_string = self.get_order_string(order.order_id, order.total_amount + 10, sku_goods)
        # 构建让用户跳转的支付链接
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string
        # TODO:传给前端的数据
        print(pay_url)
        # 5.传入前端数据
        data = {
            'saller': '达达商城',
            'total_amount': order.total_amount + order.freight,
            'order_freight': order.freight,
            'order_id': order.order_id,
            'pay_url': pay_url,
            'carts_count': carts_count
        }
        return data


class OrderInfoView(OrderBaseView):
    @login_check
    def get(self, request, username):
        """
        查询用户订单：
            0,"所有订单"
            1,"待付款"
            2,"待发货"
            3,"待收货"
            4,"订单完成"
            5,"去付款"
        """
        user = request.login_user
        status = request.GET.get("type")
        if int(status) == 0:
            order_list = OrderInfo.objects.filter(user_profile=user)

        # 去付款
        elif int(status) == 5:
            order_id = request.GET.get("order_id")
            try:
                order = OrderInfo.objects.get(order_id=order_id)
            except Exception as e:
                return JsonResponse({'code': 50102, 'errmsg': '商品问题'})

            # 查看redis存储长度
            carts_dict = self.get_carts_dict(user.id)
            carts_count = len(carts_dict)
            data = self.get_make_pay_order(order, carts_count)
            return JsonResponse({"code": 200, "data": data})

        else:
            order_list = OrderInfo.objects.filter(user_profile=user, status=status)
        orders_lists = []
        for order in order_list:
            good_skus = OrderGoods.objects.filter(order_info=order)
            sku_list = []
            # 1.获取订单中商品的信息，即sku数据
            print("good_skus", good_skus)
            for good_sku in good_skus:
                sku = good_sku.sku
                sku_sale_attr_vals, sku_sale_attr_names = get_sku_name_and_values(sku.id)
                sku_list.append({
                    'id': sku.id,
                    'default_image_url': str(sku.default_image_url),
                    'name': sku.name,
                    'price': sku.price,
                    'count': good_sku.count,
                    'total_amount': sku.price * good_sku.count,
                    "sku_sale_attr_names": sku_sale_attr_names,
                    "sku_sale_attr_vals": sku_sale_attr_vals,
                })
                print("sku_list", sku_list)
            # 2.获取订单信息
            orders_lists.append({
                "order_id": order.order_id,
                "order_total_count": order.total_count,
                "order_total_amount": order.total_amount,
                "order_freight": order.freight,
                # TODO 地址查询
                "address": {
                    "title": order.tag,
                    "address": order.address,
                    "mobile": order.receiver_mobile,
                    "receiver": order.receiver
                },
                "status": order.status,
                "order_sku": sku_list,
                "order_time": str(order.created_time)[0:19]
            })
        data = {
            'orders_list': orders_lists,
        }
        print(data)
        return JsonResponse({"code": 200, "data": data, 'base_url': settings.PIC_URL})

    @login_check
    def post(self, request, username):
        # 生成用户订单
        user = request.login_user
        obj_js = json.loads(request.body)
        address_id = obj_js.get("address_id")
        buy_count = obj_js.get("buy_count")
        sku_id = obj_js.get("sku_id")

        # 通过从购物车请求过来 请求不带sku_id
        if not sku_id:
            is_carts = True
            goods_dict = self.get_carts_dict(user.id)
            if not goods_dict:
                return JsonResponse({'code': 50201, 'errmsg': 'cart no goods'})
        else:
            is_carts = False
            goods_dict = self.get_direct_dict(sku_id, buy_count)

        # 检查购物车时，购物车中是否还有数据

        try:
            address = Address.objects.get(id=address_id, is_active=True)
        except:
            return JsonResponse({'code': 50102, 'errmsg': '收货地址无效'})
        now = datetime.datetime.now()

        # 开启事务
        with transaction.atomic():
            # 禁止自动提交
            sid = transaction.savepoint()
            # 创建订单基本对象
            order_id = '%s%02d' % (now.strftime('%Y%m%d%H%M%S'), user.id)
            total_count = 0
            total_amount = 0
            # 地址需要修改
            detail_address = address.province + address.city + address.county + address.detail
            order = OrderInfo.objects.create(
                order_id=order_id,
                user_profile=user,
                address=detail_address,
                receiver=address.receiver,
                receiver_mobile=address.receiver_phone,
                tag=address.tag,
                total_count=0,
                total_amount=0,
                freight=1,
                pay_method=1,
                status=1
            )

            # 购物车生产订单
            skus = SKU.objects.filter(id__in=goods_dict.keys())

            for sku in skus:
                goods_count = int(goods_dict[sku.id])
                # 创建订单
                # 判断库存，不足则提示,如果足够则继续执行
                if sku.stock < goods_count:
                    # 回滚事务
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code': 50103, 'errmsg': '商品[%d]库存不足' % sku.id})

                # 使用乐观锁修改商品数量
                version_old = sku.version
                result = SKU.objects.filter(pk=sku.id, version=version_old).update(stock=sku.stock - goods_count,
                                                                                   sales=sku.sales + goods_count,
                                                                                   version=version_old + 1)
                # result表示sql语句修改数据的个数
                if result == 0:
                    # 库存发生变化，未成功购买
                    transaction.savepoint_rollback(sid)
                    return JsonResponse({'code': 50104, 'errmsg': '操作太快了,请稍后重试'})

                # 创建订单商品对象
                OrderGoods.objects.create(
                    order_info=order,
                    sku_id=sku.id,
                    count=goods_count,
                    price=sku.price
                )
                # 　计算总数量,总金额
                total_count += goods_count
                total_amount += sku.price * goods_count

            # 5.修改订单对象的总金额、总数量
            order.total_count = total_count
            order.total_amount = total_amount
            # 运费默认为10
            order.freight = 10
            order.save()

            # 提交
            transaction.savepoint_commit(sid)

        if is_carts:
            # 3.从购物车中删除所有已经加入了订单的商品
            self.delete_redis_order(goods_dict.keys(), user.id)

        # 查看redis存储长度
        carts_dict = self.get_carts_dict(user.id)
        carts_count = len(carts_dict)

        data = self.get_make_pay_order(order, carts_count)

        return JsonResponse({"code": 200, "data": data})

    @login_check
    def put(self, request, username):
        # 修改用户订单状态(确认收货)
        result = json.loads(request.body)
        if not result:
            return JsonResponse({"code": 50105, "error": "订单不存在！"})
        order_id = result.get("order_id")
        order = OrderInfo.objects.filter(order_id=order_id)[0]
        order.status = 4
        order.save()
        return JsonResponse({"code": 200, 'base_url': settings.PIC_URL})


class AdvanceOrderView(OrderBaseView):
    @login_check
    def get(self, request, username):
        # 预订单（订单确认）
        # 1.获取收货地址列表
        user = request.login_user
        addresses_list = self.get_address(user.id)
        # 2.组织商品数据
        settlement = int(request.GET.get('settlement_type'))
        # 购物车结算
        data = {}
        if settlement == 0:
            # 3.获取购买购物车商品列表
            sku_list = self.get_carts_order_list(user.id)
            print("购物车：", sku_list)
        # 直接购买结算
        else:
            sku_id = request.GET.get('sku_id')
            count = request.GET.get('buy_num')
            skus = SKU.objects.filter(id=sku_id)
            # 获取商品列表
            sku_list = self.get_direct_order_list(skus, count)
            print("立即购买：", sku_list)
            data['buy_count'] = count
            data['sku_id'] = sku_id
        # 3.组织数据
        data['addresses'] = addresses_list
        data['sku_list'] = sku_list
        return JsonResponse({'code': 200, 'data': data, 'base_url': settings.PIC_URL})
