from typing import Any, Dict
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

from rest_framework import serializers
from .models import User

custom_user = get_user_model()


# serializer for user list & user profile
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'is_superuser', 'is_active', 
            'first_name', 'last_name', 'username', 
            'email', 'phone_number', 'user_type'
        ]


# serializer to create new user
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'first_name', 'last_name', 'username', 
            'email', 'password', 'phone_number', 
            'date_of_birth', 'user_type',
        ]
    

class CreateAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username', 'email', 'password', 'date_of_birth', 'phone_number']

# Serializer to add user-data to the /jwt/create route
# class CustomTokenSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         obj = self.user

#         data.update({
#             'id': obj.id, 
#             'username': obj.username,
#             'email': obj.email,
#             'user_type' : obj.user_type
#         })

#         return data
    
    