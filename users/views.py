from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

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
            from tasks.tasks import show_name
            show_name.delay("111")
        except Users.DoesNotExist:
            raise Http404
            return Response(RESPONSE.FAILURE_NOT_EXIST)
        user_list = []
        for user in users:
            user_list.append(
                {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                }
            )
            success = update_dict(dict(list=user_list))
        return Response(success)

    def post(self, request):
        result = request.data
        data = result.get('list')
        for item in data:
            param = {
                "addresses": [
                    {
                        "address1": data[index].get('addresses', None).get('address1', None),
                        "city": data[index].get('addresses', None).get('city', None),
                        "country_code": data[index].get('addresses', None).get('country_code', None),
                        "first_name": data[index].get('addresses', None).get('first_name', None),
                        "last_name": data[index].get('addresses', None).get('last_name', None),
                        "postal_code": data[index].get('addresses', None).get('postal_code', None),
                        "state_or_province": data[index].get('addresses', None).get('state_or_province', None)
                    }
                ],
                "authentication": {
                    "force_password_reset": data[index].get('authentication', None).get('force_password_reset', None),
                    "new_password": data[index].get('authentication', None).get('new_password', None)
                },
                "company": data[index].get('company', None),
                "customer_group_id": data[index].get('customer_group_id', None),
                "email": data[index].get('email', None),
                "first_name": data[index].get('first_name', None),
                "last_name": data[index].get('last_name', None),
                "password": data[index].get('authentication', None).get('new_password', None),
                "phone": data[index].get('phone', None)
            }
            try:
                customer = customers.Customers.get_customer(customers.Customers(), data[index].get('email', None))
                user = Users.objects.get(email=data[index].get('email', None))
                if customer.get('data') is None and user is None:
                    user = Users.objects.create(**param)
                    resp = customers.Customers.post_customers([param])
                    if resp.get('data') is None:
                        Response(RESPONSE.FAILURE_BAD)
                    bc_id = resp.get('data').get('data')[0].get('id')
                    user.bc_id = bc_id
                    user.save()
                    for index in range(len(param.get('address'))):
                        BillingAddress.objects.create(**param.get('address')[index])
                    success = update_dict(dict(userId=user.id))
                    return Response(success)
                if customer.get('data') and user:
                    return Response({
                        'code': 405,
                        'message': '用户已存在！'
                    })
                if customer.get('data') is None and user:
                    user_param = {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password,
                        'token': user.token,
                        'company': user.company,
                        'customer_group_id': user.customer_group_id
                    }
                    param.update(user_param)
                    resp = customers.Customers.post_customers([param])
                    if resp.get('data') is None:
                        Response(RESPONSE.FAILURE_BAD)
                    bc_id = resp.get('data').get('data')[0].get('id')
                    user.bc_id = bc_id
                    user.save()
                    return Response({
                        'code': 405,
                        'message': '用户已存在！'
                    })
                if customer.get('data') and user is None:
                    customer_param = {
                        "addresses": [
                            {
                                "address1": customer.get('data').get('data').get('addresses', None).get('address1',
                                                                                                        None),
                                "city": customer.get('data').get('data').get('addresses', None).get('city', None),
                                "country_code": customer.get('data').get('data').get('addresses', None).get(
                                    'country_code', None),
                                "first_name": customer.get('data').get('data').get('addresses', None).get('first_name',
                                                                                                          None),
                                "last_name": customer.get('data').get('data').get('addresses', None).get('last_name',
                                                                                                         None),
                                "postal_code": customer.get('data').get('data').get('addresses', None).get(
                                    'postal_code', None),
                                "state_or_province": customer.get('data').get('data').get('addresses', None).get(
                                    'state_or_province', None)
                            }
                        ],
                        "authentication": {
                            "force_password_reset": customer.get('data').get('data').get('authentication', None).get(
                                'force_password_reset',
                                None),
                            "new_password": customer.get('data').get('data').get('authentication', None).get(
                                'new_password', None)
                        },
                        "company": customer.get('data').get('data').get('company', None),
                        "customer_group_id": customer.get('data').get('data').get('customer_group_id', None),
                        "email": customer.get('data').get('data').get('email', None),
                        "first_name": customer.get('data').get('data').get('first_name', None),
                        "last_name": customer.get('data').get('data').get('last_name', None),
                        "password": customer.get('data').get('data').get('authentication', None).get('new_password',
                                                                                                     None),
                        "phone": customer.get('data').get('data').get('phone', None)
                    }
                    Users.objects.create(**customer_param)
                    for index in range(len(customer_param.get('address'))):
                        BillingAddress.objects.create(**customer_param.get('address')[index])
                    bc_id = customer.get('data').get('data')[0].get('id')
                    user.bc_id = bc_id
                    user.save()
                    return Response({
                        'code': 405,
                        'message': '用户已存在！'
                    })
            except Exception:
                raise Http404
                return Response(RESPONSE.FAILURE_BAD)


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
