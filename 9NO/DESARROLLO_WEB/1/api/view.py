from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from django.contrib.auth.models import User

from api import models
from api import serilizers as serializers

# User CRUD

# Create

class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer
    

## Retrive
# List

class UserListApiView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = serializers.ListUserSerializer(users, many=True).data
        return Response(data)

# Detail

class UserDetailApiView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        data = serializers.DetailUserSerializer(user, many=False).data
        return Response(data)

# Update

class UserUpdateApiView(APIView):
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        data = serializers.UpdateUserSerializer(user, data=request.data, many=False).data
        return Response(data)

# Delete

class UserDeleteApiView(APIView):
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        data = serializers.DeleteUserSerializer(user, many=False).data
        return Response(data)


# Bank CRUD

# Create

class BankCreateApiView(APIView):
    pass

## Retrive
# List

class BankListApiView(APIView):
    def get(self, request):
        banks = models.bank.objects.all()
        data = serializers.ListBankSerializer(banks, many=True).data
        return Response(data)
# Detail

class BankDetailAPIView(APIView):
    def get(self, request, id):
        bank = models.bank.objects.get(pk=id)
        data = serializers.DetailBankSerializer(bank, many=False).data
        return Response(data)

# Update

class BankUpdateApiView(APIView):
    def put(self, request, id):
        bank = models.bank.objects.get(pk=id)
        data = serializers.UpdateBankSerializer(bank, data=request.data, many=False).data
        return Response(data)

# Delete

class BankDeleteApiView(APIView):
    def delete(self, request, id):
        bank = models.bank.objects.get(pk=id)
        bank.delete()
        data = serializers.DeleteBankSerializer(bank, many=False).data
        return Response(data)
