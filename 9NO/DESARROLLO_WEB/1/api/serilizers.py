from rest_framework import serializers

# Models
from api import models


# Bank
# Create

class bankSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.bank
        fields = [
            'name',
            'address',
            'status',
        ]

## Retrive
# List

class bankSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.bank
        fields = [
            'id',
            'name',
            'status'
        ]

# Detail

class bankSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.bank
        fields = '__all__'

# Update

class bankSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.bank
        fields = [
            'name',
            'address',
            'status',
        ]

# Delete

class bankSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.bank
        fields = '__all__'


# Account
# Create

class accountSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            'name',
            'bank',
            'user',
            'currency',
            'balance',
            'status',
        ]

## Retrive
# List

class accountSerializerList(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            'id',
            'name',
            'status',
        ]

# Detail

class accountSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'

# Update

class accountSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            'name',
            'bank',
            'user',
            'currency',
            'balance',
            'status',
        ]

# Delete

class accountSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'
