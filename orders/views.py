from datetime import datetime
import uuid

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import jwt
from service import orders
# Create your views here.
from billing_address.models import BillingAddress
from order_product.models import OrderProduct
from orders.models import Orders
from products.models import Products
from users.models import Users
from util.status import update_dict
import util.status as RESPONSE


class Order(APIView):
    def get(self, request):
        data = request.data
        token = data.get('token', None)
        signature = token.split('.')[2] if token else None
        jwt_decode = jwt.decode(token, 'SECRET_KEY', 'HS256')
        user_id = jwt_decode.get('user_id', None)
        user = Users.objects.get(id=user_id)
        if signature == user.token and user:
            orders = Orders.objects.filter(user_id=user_id)
            order_list = []
            for order in orders:
                product_list = []
                products = OrderProduct.objects.filter(order_id=order.id)
                for product in products:
                    product_list.append(
                        product.__str__().get('product_id').__str__()
                    )
                tmp = order.__str__()
                user_id = tmp.get('user_id').id
                tmp.update({'user_id': user_id})
                tmp.update({'products': product_list})
                order_list.append(tmp)
            success = update_dict(dict(list=order_list))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)

    def post(self, request):
        data = request.data
        token = data.get('token', None)
        billing_address = data.get('billing_address', None)
        product_list = data.get('list', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        user = Users.objects.get(id=user_id)

        if signature == user.token and user and product_list and billing_address:
            _billing_address = BillingAddress.objects.create(**billing_address)
            param = {
                'user_id': user,
                'status': '1'
            }
            order = Orders.objects.create(**param)
            products = []
            for item in product_list:
                product = Products.objects.get(bc_product_id=item.get('product_id'))
                order_product = {
                    'order_id': order,
                    'product_id': product,
                    'billing_address_id': _billing_address,
                    'quantity': item.get('quantity', None)
                }
                OrderProduct.objects.create(**order_product)
                products.append({'name': product.name,
                                 'quantity': item.get('quantity', None),
                                 'price_ex_tax': product.price,
                                 'price_inc_tax': product.price})
            bc_order = {
                'billing_address': billing_address,
                'products': products
            }
            resp = orders.Orders.post_order(orders.Orders(), bc_order)
            if resp:
                order.bc_order_id = resp.get('id')
                order.save()
                success = update_dict(dict(orderId=order.id))
                return Response(success)
        return Response(RESPONSE.FAILURE_BAD)
