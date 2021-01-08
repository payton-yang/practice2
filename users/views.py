from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Users
import json
from django.http import Http404
import jwt


# Create your views here.

class UserList(APIView):

    authentication_classes = ()

    def get(self, request):
        try:
            users = Users.objects.all()
        except Users.DoesNotExist:
            raise Http404
            return Response({
                "code":404,
                "message":"User does not exist"
            })
        user_list = []
        for user in users:
            user_list.append(
                {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                }
            )
        return Response(user_list)

    def post(self, request):
        data = request.data
        param = {
            'name': data.pop('name', None),
            'email': data.pop('email', None),
            'password': data.pop('password', None),
        }

        try:
            users = Users.objects.create(**param)
        except Exception:
            raise Http404

        return Response(users.__str__())


class UserDetail(APIView):
    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        param = {
            'name': data.pop('name', None),
            'email': data.pop('email', None),
            'password': data.pop('password', None),
        }
        user.name = param.get('name', user.name)
        user.email = param.get('email', user.email)
        user.password = param.get('password', user.password)
        user.save()
        data = {
            'email': user.email,
            'name': user.name,
            'password': user.password,
        }
        return Response(data)

    def get(self, request, pk):
        user = self.get_object(pk)
        data = {
            'email': user.email,
            'name': user.name,
            'password': user.password,
        }
        return Response(data)

    def get_object(self, pk):
        try:
            return Users.objects.get(pk=pk)
        except Users.DoesNotExist:
            raise Http404

    def delete(self, request, pk):

        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Login(APIView):
    def post(self, request):
        data = request.data
        try:
            user = Users.objects.get(email=data.get('email', None))
        except Users.DoesNotExist:
            raise Http404
        if data.get('password', None) == user.password:
            payload = {
                'name': user.name,
                'email': user.email
            }
            jwt_token = {'token': jwt.encode(
                payload, "SECRET_KEY", algorithm='HS256')}
            print(jwt_token)
            signature = jwt_token['token'].split('.')[2]
            user.token = signature
            user.save()
            return Response(jwt_token, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
