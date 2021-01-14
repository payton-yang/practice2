import random

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from service import products
from .models import Products
from util.status import update_dict
import util.status as RESPONSE


# Create your views here.
class ProductList(APIView):
    def get(self, request):
        products = Products.objects.all()
        product_list = []
        for product in products:
            product_list.append(product.__str__())
        success = update_dict(dict(list=product_list))
        return Response(success)

    def post(self, request):
        resp = products.Products.get_products(products.Products(), param=dict(limit=50))
        data = resp['data']
        count = int(data['meta']['pagination']['count'])
        for index in range(count):
            param = {
                'name': data['data'][index]['name'],
                'bc_product_id': data['data'][index]['id'],
                'type': data['data'][index]['type'],
                'price': data['data'][index]['price'],
                'option_set_id': data['data'][index]['option_set_id'],
                'date_modified': data['data'][index]['date_modified'],
                'date_created': data['data'][index]['date_created'],
                'sku': data['data'][index]['sku'],
                'description': data['data'][index]['description'],
                'quantity': random.randint(30, 1000),
            }
            try:
                product = Products.objects.create(**param)
            except BaseException:
                raise status.HTTP_400_BAD_REQUEST
                return Response(FAILURE_BAD)
            success = update_dict(dict(productId=product.id))
        return Response(success)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Response(RESPONSE.FAILURE_NOT_EXIST)

    def get(self, request, pk):
        product = self.get_object(pk)
        success = update_dict(dict(product.__str__()))
        return Response(success)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        success = dict(productId=pk)
        return Response(success)

    def put(self, request, pk):
        data = request.data
        product = self.get_object(pk)
        product.name = data.get('name', product.name)
        product.type = data.get('type', product.type)
        product.image = data.get('image', product.image)
        product.quantity = data.get('quantity', product.quantity)
        product.color = data.get('color', product.color)
        product.save()
        success = dict(data=product.__str__())
        return Response(success)
