from rest_framework.views import APIView
from api import models
from api import serilizers as serializers
from rest_framework.response import Response

# Account CRUD

# Create

class AccountCreateApiView(APIView):
    def post(self, request):
        data = serializers.accountSerializerCreate(data=request.data, many=False).data
        return Response(data)

## Retrive
# List

class AccountListApiView(APIView):
    def get(self, request):
        accounts = models.Account.objects.all()
        data = serializers.accountSerializerList(accounts, many=True).data
        return Response(data)

# Detail

class AccountDetailApiView(APIView):
    def get(self, request, id):
        account = models.Account.objects.get(pk=id)
        data = serializers.accountSerializerDetail(account, many=False).data
        return Response(data)

# Update

class AccountUpdateApiView(APIView):
    def put(self, request, id):
        account = models.Account.objects.get(pk=id)
        data = serializers.accountSerializerUpdate(account, data=request.data, many=False).data
        return Response(data)

# Delete

class AccountDeleteApiView(APIView):
    def delete(self, request, id):
        account = models.Account.objects.get(pk=id)
        account.delete()
        data = serializers.accountSerializerDelete(account, many=False).data
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
        data = serializers.bankSerializerList(banks, many=True).data
        return Response(data)
# Detail

class BankDetailAPIView(APIView):
    def get(self, request, id):
        bank = models.bank.objects.get(pk=id)
        data = serializers.bankSerializerDetail(bank, many=False).data
        return Response(data)

# Update

class BankUpdateApiView(APIView):
    def put(self, request, id):
        bank = models.bank.objects.get(pk=id)
        data = serializers.bankSerializerUpdate(bank, data=request.data, many=False).data
        return Response(data)

# Delete

class BankDeleteApiView(APIView):
    def delete(self, request, id):
        bank = models.bank.objects.get(pk=id)
        bank.delete()
        data = serializers.bankSerializerDelete(bank, many=False).data
        return Response(data)
