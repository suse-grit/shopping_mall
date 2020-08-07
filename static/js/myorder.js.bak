/**
 * Created by tarena on 19-9-5.
 */
function orders() {
            $.ajax({
                    type: 'get',
                    url: baseUrl+'/order/info/',
                    datatype: 'json',
                    async: false,
                    success: function (response) {
                        var result = JSON.stringify(response)
                        var results = JSON.parse(result)
                        console.log(results)
                        console.log(results.context.sku_list)
                        var data_goods = results.context.sku_list
                        console.log(data_goods)
                        var data_address = results.context.addresses
                        console.log(data_address)
                        console.log(data_address[0].id)
                        var orderConfirm = {
                        }
                        orderConfirm.data = {
                            html_goods: function () {
                                var HTML = '';
                                var sumPrice = 0;
                                for (var i = 0; i < data_goods.length; i++) {
                                    HTML += ' <ul class="item_detail">'
                                    HTML += '<li class="p_info">'
                                    HTML += '<div class="product_name">'
                                    HTML += '<p>'
                                    HTML += data_goods[i].name
                                    HTML += '</p>'
                                    var saleattr_name = data_goods[i].sku_sale_attr_names
                                    var saleattr_val = data_goods[i].sku_sale_attr_vals
                                    for (var j = 0; j < saleattr_name.length; j++){
                                        HTML += '<span>'
                                        HTML += saleattr_name[j]
                                        HTML += ':'
                                        HTML += saleattr_val[j]
                                        HTML += '</span>&nbsp&nbsp'
                                    }
                                    HTML += '</div>'
                                    HTML += '<b><img src="' + data_goods[i].sku_default_imgage_url + '" /></b>'
                                    HTML += '</li>'
                                    HTML += '<li class="p_price">'
                                    HTML += '<i>皮粉专属价</i>'
                                    HTML += '<br />'
                                    HTML += '<span class="pro_price">￥<span class="ppp_price">' + data_goods[i].price +
                                        '</span></span>'
                                    HTML += '</li>'
                                    HTML += '<li class="p_count"><span>' + data_goods[i].count + '</span></li>'
                                    HTML += '<li class="p_tPrice">￥<span>' + data_goods[i].count * data_goods[i].price + '</span></li>'
                                    HTML += '</ul>'
                                    sumPrice += data_goods[i].count * data_goods[i].price;
                                }
                                $("#count").html(data_goods.length);
                                $(".zj").html(sumPrice);
                                return HTML;
                            },
                            html_address : function() {
                                var HTML = '';
                                HTML += '<p>收货人信息<span class="rt" id="choose">新增收货地址</span></p>'
                                HTML += '<div class="allAdd_content">'
                                for (var i = 0; i < data_address.length; i++) {
                                    if (i==0){
                                        HTML += '<div id="addresId1" class="base_select">';
                                    }else{
                                        HTML += '<div id="addresId2" class="base">';
                                    }
                                    HTML += '<i class="address_name">';
                                    HTML += data_address[i].name;
                                    HTML += '</i><i class="user_address">';
                                    HTML += data_address[i].address;
                                    HTML += '&nbsp&nbsp';
                                    HTML += data_address[i].mobile;
                                    HTML += '</i><i class="user_site rt">';
                                    HTML += data_address[i].title;
                                    HTML += '</i></div>';
                                }
                                HTML += '</div>';
                                HTML += '<a id="more" href="javascript:;">更多地址 &gt;&gt;</a>';
                                return HTML;
                                },
                            addads: function () {
                                var receiverName = $("#receiverName").val(); // 收件人
                                var receiverState = $("#receiverState").val(); // 省
                                var receiverCity = $("#receiverCity").val(); // 市
                                var receiverDistrict = $("#receiverDistrict").val(); // 区/县
                                var receiverAddress = $("#receiverAddress").val(); //
                                var receiverMobile = $("#receiverMobile").val();
                                var receiverZip = $("#receiverZip").val() ? $("#receiverZip").val() : null;
                                var addressName = $("#addressName").val();
                                if (receiverName && receiverState && receiverCity && receiverDistrict && receiverAddress &&
                                    receiverMobile) {
                                    $.ajax({
                                        type: 'post',
                                        url: baseUrl + '/user/addads',
                                        contentType:'application/json',
                                        datatype: JSON,
                                        data: {
                                            "consignee": receiverName,
                                            "ads": receiverState + receiverCity + receiverDistrict + receiverAddress,
                                            "mobile": receiverMobile,
                                            'zipcode': receiverZip,
                                            'alias': addressName
                                        },
                                        success: function (response) {

                                        },
                                        error: function (err) {
                                            alert('保存失败' + err)
                                        }
                                    })
                                } else {
                                    alert("请将必填信息填写完整");
                                }
                            },
                            initPage: function () {
                                //顶部支付订单背景画布
                                var canvas = document.getElementById("canvas_gray");
                                var cxt = canvas.getContext("2d");
                                var gray = cxt.createLinearGradient(10, 0, 10, 38);
                                gray.addColorStop(0, '#f5f4f5');
                                gray.addColorStop(1, '#e6e6e5');
                                cxt.beginPath();
                                cxt.fillStyle = gray;
                                cxt.moveTo(20, 19);
                                cxt.lineTo(0, 38);
                                cxt.lineTo(0, 0);
                                cxt.fill();
                                cxt.closePath();
                                //顶部确认订单信息背景画布
                                var canvas = document.getElementById("canvas_blue");
                                var cxt = canvas.getContext("2d");
                                var blue = cxt.createLinearGradient(10, 0, 10, 38);
                                blue.addColorStop(0, '#997679');
                                blue.addColorStop(1, '#997679');
                                cxt.beginPath();
                                cxt.fillStyle = blue;
                                cxt.moveTo(20, 19);
                                cxt.lineTo(0, 38);
                                cxt.lineTo(0, 0);
                                cxt.fill();
                                cxt.closePath();
                            }
                        }
                        $(function () {
                            //初始化
                            orderConfirm.data.initPage();
                            $(".item_title").after(orderConfirm.data.html_goods());
                            $(".adress_choice").after(orderConfirm.data.html_address());
                            //点击显示更多地址事件
                            $("#more").click(function () {
                                if ($(this).hasClass("upup")) {
                                    $(".base_select").siblings().hide();
                                    // $(".allAdd_content>div:not(:first-child)").css("display","none");
                                    $("#more").html("更多地址>>");
                                    $(this).removeClass("upup");
                                } else {
                                    $(".base_select").siblings().show();
                                    // $(".allAdd_content>div:not(:first-child)").css("display","block");
                                    $("#more").html("收起地址>>");
                                    $("#more").addClass("upup");
                                }
                            })
                            //控制新增收货地址框的显示隐藏
                            $("#choose").click(function () {
                                $(".modal").show();
                            })
                            $(".cha").click(function () {
                                $(".modal").hide();
                            })
                            $(".user_site").click(function () {
                                $(this).parent().attr("class", "base_select").siblings().attr("class", "base");
                                $(this).hide();
                            })
                            //地址页面添加名称至输入框
                            $(".sp").click(function () {
                                var value = $(this).html();
                                $("#addressName").val(value);
                            })
                            $('.save_recipient').click(function () {
                                orderConfirm.data.addads()
                            })
                        })
                         $("#go_pay").click(function () {
                             window.location='http://172.162.18.60:5000/order_p?address_id='+data_address[0].id
                         })
                    },
                    error:function(){
                        console.log("错误")
                    }
                }
            )
            return false
        }

window.onload = function () {
    orders()
}

















