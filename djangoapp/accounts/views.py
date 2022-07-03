
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterNewUserSerializer, UserLoginSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterNewUserAPIView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterNewUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

class AddUserNewKeyWord(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if request.user:
            user = request.user
        if 'phone' in request.data:
            user=User.objects.get(phone=request.data['phone'])

        user.key_words.add(request.data['key_word'])
        user.save()
        return Response(status=status.HTTP_200_OK)