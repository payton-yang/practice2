from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        data = request.data
        if data['id']:
            data.pop('id')
        try:
            product = Products.objects.create(**data)
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
