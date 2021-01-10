from datetime import datetime
import uuid

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import jwt

# Create your views here.
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
                        {
                            'id': product.__str__().id,
                            'name': product.__str__().name,
                            'type': product.__str__().type,
                            'quantity': product.quantity,
                            'color': product.__str__().color
                        }
                    )
                order_list.append(
                    {
                        'orderId': order.id,
                        'uuid': order.uuid,
                        'create_time': order.create_time,
                        'status': order.status,
                        'product': product_list
                    }
                )
            success = update_dict(dict(list=order_list))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)

    def post(self, request):
        data = request.data
        token = data.get('token', None)
        product_list = data.get('list', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        user = Users.objects.get(id=user_id)

        if signature == user.token and user and product_list:
            param = {
                'user_id': user,
                'status': '1',
                'uuid': uuid.uuid1(),
                'create_time': datetime.now()
            }

            order = Orders.objects.create(**param)
            for item in product_list:
                product_id = item.get('productId', None)
                product = Products.objects.get(id=product_id)
                order_product = {
                    'order_id': order,
                    'product_id': product,
                    'quantity': item.get('quantity', None)
                }
                product.quantity -= item.get('quantity', 0)
                product.save()
                OrderProduct.objects.create(**order_product)
            success = update_dict(dict(orderId=order.id))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)
