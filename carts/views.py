from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import jwt

from cart_product.models import CartProduct
from products.models import Products
from .models import Carts
from util.status import update_dict
import util.status as RESPONSE
from .models import Users
import uuid
from datetime import datetime
from service import carts


class Cart(APIView):
    def post(self, request):
        data = request.data
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, 'SECRET_KEY', algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        product_list = data.get('list', None)
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user and product_list:
            bc_param = {
                "line_items": product_list
            }
            resp = carts.Carts.post_cart(carts.Carts(), bc_param)
            param = {
                'user_id': user,
                'status': '1',
            }
            cart = Carts.objects.create(**param)
            for item in product_list:
                product = Products.objects.get(bc_product_id=item.get('product_id', None))
                item_list = resp.get('data').get('line_items').get('physical_items')
                for physical_item in item_list:
                    _cart_product = {
                        'cart_id': cart,
                        'product_id': product,
                        'bc_item_id': physical_item.get('id'),
                        'quantity': item.get('quantity', None),
                    }
                    product.quantity -= item.get('quantity')
                    product.save()
                    CartProduct.objects.create(**_cart_product)
                cart.bc_cart_id = resp.get('data').get('id')
                cart.save()
            success = update_dict(dict(cart_id=cart.id, bc_cart_id=resp.get('data').get('id')))
            return Response(success)
        return Response(status.HTTP_400_BAD_REQUEST)


# Create your views here.
class CartDetail(APIView):

    def put(self, request, cart_id, item_id):
        data = request.data
        line_item = data.get('line_item', None)
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        try:
            if signature == user.token and user and line_item:
                cart = Carts.objects.get(pk=cart_id)
                product = Products.objects.get(bc_product_id=line_item.get('product_id', None))
                try:
                    cart_product = CartProduct.objects.get(cart_id=cart_id, bc_item_id=item_id)
                except CartProduct.DoesNotExist:
                    cart_product = None
                if cart_product:
                    product.quantity += cart_product.quantity
                    cart_product.quantity = line_item.get('quantity')
                    product.quantity -= line_item.get('quantity')
                    cart_product.save()
                    product.save()
                else:
                    return Response(RESPONSE.FAILURE_BAD)
                bc_param = {
                    "line_item": {
                        "quantity": line_item.get('quantity'),
                        "product_id": line_item.get('product_id'),
                    }
                }
                carts.Carts.put_cart_items(carts.Carts(), bc_cart_id=cart.bc_cart_id,
                                           item_id=item_id,
                                           data=bc_param)
                success = update_dict(dict(cart_id=cart.id))
                return Response(success)
        except Exception:
            return Response(RESPONSE.FAILURE_BAD)

    def post(self, request, cart_id):
        data = request.data
        line_items = data.get('line_items', None)
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user and line_items:
            cart = Carts.objects.get(id=cart_id)
            for item in line_items:
                bc_cart = {
                    'line_items': [item],
                    'gift_certificates': data.get('gift_certificates')
                }
                resp = carts.Carts.add_cart_items(carts.Carts(), cart.bc_cart_id, bc_cart)
                product = Products.objects.get(bc_product_id=item.get('product_id'))
                param = {
                    'cart_id': cart,
                    'product_id': product,
                    'bc_item_id': resp.get('data').get('line_items').get('physical_items')[0].get('id'),
                    'quantity': item.get('quantity')
                }
                cart_product = CartProduct.objects.create(**param)
            if resp and cart_product:
                return Response({
                    'code': 200,
                    'message': 'success',
                    'bc_cart_id': cart.bc_cart_id
                })

    def delete(self, request, cart_id, item_id):
        data = request.data
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user:
            cart_product = CartProduct.objects.get(cart_id=cart_id, bc_item_id=item_id)
            product = Products.objects.get(id=cart_product.product_id.__str__().get('id'))
            product.quantity += cart_product.quantity
            product.save()
            cart_product.delete()
            cart = Carts.objects.get(id=cart_id)
            resp = carts.Carts.delete_cart_items(carts.Carts(), cart.bc_cart_id, item_id)
            if resp is not False and cart_product:
                return Response({
                    'code': 200,
                    'message': 'success',
                    'data': {}
                })
        return Response(RESPONSE.FAILURE_BAD)

    def get(self, request, pk):
        data = request.data
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user:
            product_list = []
            cart_product_list = CartProduct.objects.filter(cart_id=pk)
            for cart_product in cart_product_list:
                tmp = cart_product.__str__()
                tmp.update(dict(cart_id=tmp.get('cart_id').__str__().get('id')))
                tmp.update(dict(product_id=tmp.get('product_id').__str__().get('id')))
                tmp.pop('id')
                product = cart_product.product_id
                product_list.append(
                    tmp
                )
            success = update_dict(dict(list=product_list))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)
