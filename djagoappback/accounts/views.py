
from ast import keyword
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import SearchWords, User
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


class SetUserPhoneNumberAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, *args, **kwargs):
        if request.user:
            user = request.user
        if 'phone_number' in request.data and 'username' in request.data:
            user = User.objects.get(phone=request.data['username'])
        user.phone_number = request.data['phone_number']
        user.save()
        return Response(status=status.HTTP_200_OK)



class FinalRegisterTemplateView(View):
    def get(self, request,*args, **kwargs):
        context={
            'title':'ثبت نام نهایی',
        }
        return render(request, 'accounts/final_register.html',context)

    def post(self, request, *args, **kwargs):
        print(request.POST['days'])
        user=request.user
        keyword = request.POST['keyword']
        list_of_keywords = keyword.split(',')

        SearchWords.objects.bulk_create(
            SearchWords(word=keyword, user=user) for keyword in list_of_keywords
        )



        return render(request, 'accounts/final_register.html',{'title':'ثبت نام نهایی'})
        



class LoginTemplateView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context={
            'title':'ورود',
            'form':form
        }
        return render(request, 'accounts/login.html',context)
    

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'حساب فعالی با این مشخصات یافت نشد ')
                return redirect('accounts:login')

            if user.check_password(password):
                login(request, user)
                return redirect('accounts:final_register')
            else:
                messages.error(request, 'حساب فعالی با این مشخصات یافت نشد')
                return redirect('accounts:login')

        else:
            context = {
                'form': form,
            }
            messages.error(request, 'something went wrong.')
            return render(request, 'accounts/login.html', context)
