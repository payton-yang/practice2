from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
        data = request.data
        param = {
            'name': data.pop('name', None),
            'email': data.pop('email', None),
            'password': data.pop('password', None),
        }

        try:
            user = Users.objects.create(**param)
        except Exception:
            raise Http404
            return Response(RESPONSE.FAILURE_BAD)
        success = update_dict(dict(userId=user.id))
        return Response(success)


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
            print(jwt_token)
            signature = jwt_token['token'].split('.')[2]
            user.token = signature
            user.save()
            success = update_dict(dict(jwt_token))
            return Response(success)
        return Response(RESPONSE.FAILURE_BAD)
