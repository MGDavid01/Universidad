# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from api import models

# =============================
# USERS SERIALIZERS
# =============================

# CREATE USER

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type":"password"
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={
            "input_type":"password"
            }
    )

    class Meta: 
        model = User
        fields=[
            "id",
            "username",
            "first_name",
            "email",
            "password",
            "password_confirm"
        ]

        read_only_fields =("id",)

    def validate_username(self,value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Este usuario ya existe, Registra uno diferente"
            )
        return value

    def validate_email(self,value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Email ya existe, Registra uno diferente"
                )
        return value

    def validate(self, attrs):
        if attrs["password"]!=attrs["password_confirm"]:
            raise serializers.ValidationError ({
                "password_confirm": "Los password no coinciden"
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get["last_name",""]
        )
        

# LISTA DE USUARIOS
class UserSerializerList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]

# DETALLE DEL USUARIO
class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

# ============================
# BANKS SERIALIZERS
# ============================

# CREAR BANCOS
class BankSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["name", "address"]

# LISTA DE BANCOS
class BankSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = [
            "id",
            "name",
            "status",
        ]

# DETALLE DE LOS BANCOS
class BankSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = [
            "id",
            "name",
            "address",
            "status",
            "timestamp",
            "update",
        ]

# UPDATE DE UN BANCO
class BankSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["name", "address", "status"]

# DELETE DE UN BANCO
class BankSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Bank
        fields = ["id", "name", "status"]

# ================================
# ACCOUNT SERIALIZER
# ================================

# LISTA DE CUENTAS
class AccountSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "id",
            "name",
            "bank",
            "currency",
        ]

# DETALLE DE LA CUENTA
class AccountSerializerDetail(serializers.ModelSerializer):
    bank_name = serializers.CharField(source="bank.name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = models.Account
        fields = [
            "id",
            "name",
            "bank_name",
            "username",
            "currency",
            "timestamp",
            "update",
            "status",
        ]

# CREATE
class AccountSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "name",
            "bank",
            "user",
            "currency",
        ]

# UPDATE
class AccountSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "name",
            "bank",
            "user",
            "currency",
            "status",
        ]

# DELETE
class AccountSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            "id",
            "name",
            "status",
        ]

# ============================
# PROVIDERS SERIALIZER
# ============================
# CREATE
class ProviderSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "name",
            "address",
        ]

# RETRIEVE
# LIST

class ProviderSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "id",
            "name",
            "status",
        ]

# DETAIL

class ProviderSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = "__all__"

# UPDATE

class ProviderSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "name",
            "address",
            "status",
        ]

# DELETE

class ProviderSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = [
            "id",
            "name",
            "status",
        ]

# ============================
# PAYMENT SERIALIZER
# ============================
# CREATE
class PaymentSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "name",
            "account",
            "user",
            "provider",
        ]

# LIST
class PaymentSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "id",
            "name",
            "account",
        ]

# DETAIL

class PaymentSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = "__all__"

# UPDATE
class PaymentSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "name",
            "account",
            "user",
            "provider",
            "status",
        ]
# DELETE
class PaymentSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "id",
            "name",
            "status",
        ]