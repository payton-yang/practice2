from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from service.addresses import Addresses
from address.models import Address
from billing_address.models import BillingAddress
from service import customers
from .models import Users
import json
from django.http import Http404
import jwt
from util.status import update_dict
import util.status as RESPONSE


# Create your views here.

class UserList(APIView):
    authentication_classes = ()

    def get(self, request):
        try:
            users = Users.objects.all()
        except Users.DoesNotExist:
            raise Http404
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        user_list = []
        for user in users:
            user_list.append(user.__str__())
            success = update_dict(dict(list=user_list))
        return Response(success)

    def post(self, request):
        result = request.data
        data = result.get('list')
        for item in data:
            param = {
                "addresses": [
                    {
                        "address1": address.get('address1', None),
                        "city": address.get('city', None),
                        "country_code": address.get('country_code', None),
                        "first_name": address.get('first_name', None),
                        "last_name": address.get('last_name', None),
                        "postal_code": address.get('postal_code', None),
                        "state_or_province": address.get('state_or_province', None)
                    } for address in item.get('addresses')
                ],
                "authentication": {
                    "force_password_reset": item.get('authentication', None).get('force_password_reset', None),
                    "new_password": item.get('authentication', None).get('new_password', None)
                },
                "company": item.get('company', None),
                "customer_group_id": item.get('customer_group_id', None),
                "email": item.get('email', None),
                "first_name": item.get('first_name', None),
                "last_name": item.get('last_name', None),
                "password": item.get('authentication', None).get('new_password', None),
                "phone": item.get('phone', None)
            }
            customer = customers.Customers.get_customer(customers.Customers(), email=item.get('email', None))
            try:
                user = Users.objects.get(email=item.get('email', None))
            except Users.DoesNotExist:
                user = None
            if not customer.get('data') and user is None:
                resp = customers.Customers.post_customers(customers.Customers(), data=[param])
                addresses = param.pop('addresses')
                param.pop('authentication')
                user = Users.objects.create(**param)
                for address in addresses:
                    address.update(dict(user_id=user))
                    Address.objects.create(**address)
                if not resp.get('data'):
                    Response(RESPONSE.FAILURE_BAD)
                bc_id = resp.get('data')[0].get('id')
                user.bc_id = bc_id
                user.save()
                success = update_dict(dict(userId=user.id))
                return Response(success)
            if customer.get('data') and user:
                return Response({
                    'code': 405,
                    'message': '用户已存在！'
                })
            if not customer.get('data') and user:
                addresses = Address.objects.filter(user_id=user)
                address_list = []
                for address in addresses:
                    tmp = address.__str__()
                    tmp.pop('id')
                    tmp.pop('user_id')
                    address_list.append(tmp)
                customer_param = {
                    "addresses": address_list,
                    "authentication": {
                        "force_password_reset": True,
                        "new_password": user.password
                    },
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'company': user.company,
                    'customer_group_id': user.customer_group_id,
                    "phone": item.get('phone', None)
                }
                resp = customers.Customers.post_customers(customers.Customers(), data=[customer_param])
                if not resp.get('data'):
                    Response(RESPONSE.FAILURE_BAD)
                bc_id = resp.get('data')[0].get('id')
                user.bc_id = bc_id
                user.save()
                return Response({
                    'code': 405,
                    'bc_id': bc_id,
                    'message': '用户已存在！'
                })
            if customer.get('data') and user is None:
                user_param = {
                    "company": customer.get('data')[0].get('company', None),
                    "customer_group_id": customer.get('data')[0].get('customer_group_id', None),
                    "email": customer.get('data')[0].get('email', None),
                    "first_name": customer.get('data')[0].get('first_name', None),
                    "last_name": customer.get('data')[0].get('last_name', None),
                    "phone": customer.get('data')[0].get('phone', None),
                    "bc_id": customer.get('data')[0].get('id', None)
                }
                user = Users.objects.create(**user_param)
                addresses = Addresses.get_customer_addresses(Addresses(),
                                                             customer_id=customer.get('data')[0].get('id', None))
                for item in addresses.get('data'):
                    item.pop('address_type')
                    item.pop('country')
                    item.pop('id')
                    item.pop('customer_id')
                    item.pop('phone')
                    item.update({'user_id': user})
                    Address.objects.create(**item)
                bc_id = customer.get('data')[0].get('id')
                user.bc_id = bc_id
                user.save()
                return Response({
                    'code': 405,
                    'id': user.id,
                    'message': '用户已存在！'
                })


class UserDetail(APIView):
    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        token = data.get('token', None)
        signature = token.split('.')[2] if token else None
        password = data.get('password', None)
        if signature == user.token and password:
            user.password = password
            user.save()
            pwd = [
                {
                    "id": 7870,
                    "authentication": {
                        "force_password_reset": True,
                        "new_password": password
                    }
                }
            ]
            customers.Customers.update_pwd(customers.Customers(), pwd)
            success = update_dict(dict())
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)

    def get(self, request, pk):
        user = self.get_object(pk)
        data = {
            'email': user.email,
            'name': user.name,
            'password': user.password,
        }
        success = update_dict(data)
        return Response(success)

    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404
            return Response(RESPONSE.FAILURE_NOT_EXIST)

    def delete(self, request, pk):

        user = self.get_object(pk)
        success = update_dict(dict(userId=user.id))
        user.delete()
        return Response(success)


class Login(APIView):
    def post(self, request):
        data = request.data
        try:
            user = Users.objects.get(email=data.get('email', None))
        except Users.DoesNotExist:
            raise Http404
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        if data.get('password', None) == user.password:
            payload = {
                'user_id': user.id,
                'email': user.email
            }
            jwt_token = {'token': jwt.encode(
                payload, "SECRET_KEY", algorithm='HS256')}
            signature = jwt_token['token'].split('.')[2]
            user.token = signature
            user.save()
            success = update_dict(dict(jwt_token))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)


class ValidatePwd(APIView):
    def post(self, request):
        data = request.data
        resp = customers.Customers.validate_pwd(customers.Customers(), customer_id=data.get('customer_id'),
                                                data={'password': data.get('password')})

        return Response({
            'code': 200,
            'message': resp.get('success')
        })
