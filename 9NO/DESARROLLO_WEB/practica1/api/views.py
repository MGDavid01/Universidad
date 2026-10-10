# views.py
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from api import serializers
from api import models
from rest_framework import generics


class UpdateWithDetailSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.request.method == "GET":
            return self.detail_serializer_class
        return super().get_serializer_class()


# ============================
# CRUD DE USUARIOS
# ============================

# OBTENER LA LISTA DE USUARIOS

class UserListAPIView(APIView):
    def get(self, request):
        user = User.objects.all()
        data = serializers.UserSerializerList(user, many=True).data
        return Response(data)

# OBTENER LOS DETALLES DE UN USUARIO

class UserDetailAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        data = serializers.UserSerializerDetail(user, many=False).data
        return Response(data)

# CREAR UN USUARIO

class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer

# ============================
# CRUD DEL BANCO
# ============================

# CREAR UN BANCO
class BankCreateAPIView(generics.CreateAPIView):
    queryset = models.Bank.objects.all()
    serializer_class = serializers.BankSerializerCreate

# LISTA DE LOS BANCOS
    
class BankListAPIView(APIView):
    def get(self, request):
        banks = models.Bank.objects.all()
        data = serializers.BankSerializerList(banks, many=True).data
        return Response(data)

# DETALLE DE CADA BANCO
class BankDetailAPIView(APIView):
    def get(self, request, pk):
        bank = models.Bank.objects.get(pk=pk)
        data = serializers.BankSerializerDetail(bank, many=False).data
        return Response(data)
    
# UPDATE DE UN BANCO
class BankUpdateAPIView(UpdateWithDetailSerializerMixin, generics.RetrieveUpdateAPIView):
    queryset = models.Bank.objects.all()
    serializer_class = serializers.BankSerializerUpdate
    detail_serializer_class = serializers.BankSerializerDetail

# DELETE DE UN BANCO
class BankDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Bank.objects.all()
    serializer_class = serializers.BankSerializerDelete

# ===================================
#  CRUD ACCOUNT
# ===================================

# LISTA DE CUENTAS

class AccountListAPIView(APIView):
    def get(self, request):
        accounts = models.Account.objects.all()
        data = serializers.AccountSerializerList(accounts, many=True).data
        return Response(data)

# DETALLE DE LA CUENTA

class AccountDetailAPIView(APIView):
    def get(self, request, pk):
        account = get_object_or_404(models.Account, pk=pk)
        data = serializers.AccountSerializerDetail(account).data
        return Response(data)

# CREATE

class AccountCreateAPIView(generics.CreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializerCreate

# UPDATE
class AccountUpdateAPIView(UpdateWithDetailSerializerMixin, generics.RetrieveUpdateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializerUpdate
    detail_serializer_class = serializers.AccountSerializerDetail

# DELETE
class AccountDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializerDelete

# ============================
# PROVIDERS VIEW
# ============================
# CREATE
class ProviderCreateAPIView(generics.CreateAPIView):
    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializerCreate

# LIST
class ProviderListAPIView(APIView):
    def get(self, request):
        providers = models.Provider.objects.all()
        data = serializers.ProviderSerializerList(providers, many=True).data
        return Response(data)
    
# DETAIL
class ProviderDetailAPIView(APIView):
    def get(self, request, pk):
        provider = get_object_or_404(models.Provider, pk=pk)
        data = serializers.ProviderSerializerDetail(provider).data
        return Response(data)
    
# UPDATE
class ProviderUpdateAPIView(UpdateWithDetailSerializerMixin, generics.RetrieveUpdateAPIView):
    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializerUpdate
    detail_serializer_class = serializers.ProviderSerializerDetail

# DELETE
class ProviderDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Provider.objects.all()
    serializer_class = serializers.ProviderSerializerDelete

# ============================
# PAYMENTS VIEW
# ============================
# CREATE
class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializerCreate

# LIST
class PaymentListAPIView(APIView):
    def get(self, request):
        payments = models.Payment.objects.all()
        data = serializers.PaymentSerializerList(payments, many=True).data
        return Response(data)
    
# DETAIL
class PaymentDetailAPIView(APIView):
    def get(self, request, pk):
        payment = get_object_or_404(models.Payment, pk=pk)
        data = serializers.PaymentSerializerDetail(payment).data
        return Response(data)
    
# UPDATE
class PaymentUpdateAPIView(UpdateWithDetailSerializerMixin, generics.RetrieveUpdateAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializerUpdate
    detail_serializer_class = serializers.PaymentSerializerDetail

# DELETE
class PaymentDeleteAPIView(generics.DestroyAPIView):
    queryset = models.Payment.objects.all()
    serializer_class = serializers.PaymentSerializerDelete
    