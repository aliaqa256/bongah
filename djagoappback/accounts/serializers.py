import re
from rest_framework import status
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterNewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    # validate phone number
    def validate_phone_number(self, value):
        if value is '':
            return value

        regex = r'^\+?1?\d{9,15}$'
        if not re.match(regex, value):
            raise serializers.ValidationError("Phone number is invalid")

        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user


class UserLoginSerializer(TokenObtainPairSerializer):

    pass