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


# Create your views here.
class CartDetail(APIView):

    def put(self, request, pk):
        data = request.data
        product_list = data.get('list', None)
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user and product_list:
            try:
                cart = Carts.objects.get(pk=pk)
                for item in product_list:
                    product = Products.objects.get(id=item.get('productId', None))
                    try:
                        cart_product = CartProduct.objects.get(cart_id=cart.id, product_id=product.id)
                    except CartProduct.DoesNotExist:
                        cart_product = None
                    if cart_product:
                        if item.get('quantity') == 0:
                            product.quantity += cart_product.quantity
                            cart_product.delete()
                        else:
                            product.quantity -= item.get('quantity')
                            cart_product.quantity += item.get('quantity')
                            cart_product.save()
                        product.save()
                    else:
                        _cart_product = {
                            'cart_id': cart,
                            'product_id': product,
                            'quantity': item.get('quantity', None)
                        }
                        product.quantity -= item.get('quantity')
                        product.save()
                        CartProduct.objects.create(**_cart_product)
            except Exception:
                raise status.HTTP_400_BAD_REQUEST
                return Response(RESPONSE.FAILURE_BAD)
            success = update_dict(dict(cartId=cart.id))
            return Response(success)
        return Response(status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        data = request.data
        token = data.get('token', None)
        jwt_decode = jwt.decode(token, "SECRET_KEY", algorithms='HS256')
        signature = token.split('.')[2]
        user_id = jwt_decode['user_id']
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if signature == user.token and user:
            product_list = []
            cart_product_list = CartProduct.objects.filter(cart_id=pk)
            for cart_product in cart_product_list:
                product = cart_product.product_id
                product_list.append(
                    {
                        'productId': product.id,
                        'name': product.name,
                        'type': product.type,
                        'color': product.color,
                        'quantity': cart_product.quantity
                    }
                )
                success = update_dict(dict(list=product_list))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)
