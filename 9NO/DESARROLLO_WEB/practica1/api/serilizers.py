from rest_framework import serializers
from django.contrib.auth.models import User

# Models
from api.models import bank as Bank


# Bank
# Create

class CreateBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            'name',
            'address',
            'status',
        ]

## Retrive
# List

class ListBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            'id',
            'name',
            'status'
        ]

# Detail

class DetailBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

# Update

class UpdateBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = [
            'name',
            'address',
            'status',
        ]

# Delete

class DeleteBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


# User
# Create

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={
            "input_type": "password"
            }
        )
    password_confirmation = serializers.CharField(
        write_only=True,
        style={
            "input_type": "password"
            }
        )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirmation',
        ]
        read_only_fields = ['id',]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Este usuario ya existe.")
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este email ya tiene una cuenta vinculada.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'Las contraseñas no coinciden.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password = validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

## Retrive
# List

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_active',
        ]

# Detail

class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'date_joined',
        ]

# Update

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
        ]

# Delete

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]
