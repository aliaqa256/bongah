
from trace import Trace
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Sum
from ast import keyword
import re
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import Payments, SearchWords, User
from .serializers import RegisterNewUserSerializer, UserLoginSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from idpay.api import IDPayAPI
from .models import MainPayed
import requests
import json
import uuid


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
            user = User.objects.get(username=request.data['username'])
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
        user=request.user
        keyword = request.POST['keyword']
        list_of_keywords = keyword.split(',')

        SearchWords.objects.bulk_create(
            SearchWords(word=keyword, user=user) for keyword in list_of_keywords
        )




        return redirect('/auth/select_plan')
        # return render(request, 'accounts/final_register.html',{'title':'ثبت نام نهایی'})
        



class LoginTemplateView(View):
    def get(self, request, *args, **kwargs):
        # if user is login
        if request.user.is_authenticated:
            return redirect('accounts:card')
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



class CardTemplateView(View):
    def get(self, request, *args, **kwargs):
        user=request.user
        keywords = user.search_words.all()
        # sum of user payments amount
        sum_of_payments = Payments.objects.filter(user=user, is_done=False).aggregate(Sum('amount'))['amount__sum'] or 0
        context={
            'title':'خرید کارت',
            'keywords': keywords,
            'sum_of_payments':sum_of_payments
        }
        return render(request, 'accounts/card.html',context)


class DeleteKeywordAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print('---------------------------------')
        self.check_object_permissions(request, request.user)
        word = SearchWords.objects.get(id=request.data['keyword_id'])

        word.delete()
        return Response(status=status.HTTP_200_OK)



class SelectPlanTemplateView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'انتخاب پلن',
        }
        return render(request, 'accounts/select_plan.html', context)
    def post(self, request, *args, **kwargs):
        user = request.user
        price = request.POST['plan_type']
        days= request.POST['plan_days']
        Payments.objects.create(user=user, amount=price,days=int(days))
        return redirect('accounts:card')


# ///////////////////////////////////////
def payment_init():
    base_url = "https://moshaveryar-bot.ir/"
    api_key = 'b93732b3-9473-40ad-a275-933d90fe0532'
    sandbox = "true"

    return IDPayAPI(api_key, base_url, True)


def payment_start(request):
    if request.method == 'POST':

        order_id = uuid.uuid1()
        amount = request.POST.get('amount')
        user=User.objects.get(username=request.POST.get('name'))

        payer = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'mail': request.POST.get('mail'),
            'desc': request.POST.get('desc'),
        }

        record = MainPayed(order_id=order_id, amount=int(amount),user=user)
        record.save()

        idpay_payment = payment_init()
        result = idpay_payment.payment(
            str(order_id), amount, 'auth/payment/return', payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"
        print('----------------------------------')

    return render(request, 'accounts/error.html', {'txt': txt})


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')
        payer = request.POST.get('payer')

        if MainPayed.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()

            payment = MainPayed.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = str(date)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()
            user=payment.user

            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)
                print(result)

                if 'status' in result:

                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()
                    # if status is 100 then payment is success
                    rooz=0
                    pp=Payments.objects.filter(is_done=False,user=user)
                    for pay in pp:
                        rooz+= pay.days
                        pay.is_done=True
                        pay.save()
                    user.days_left=user.days_left + rooz
                    user.save()

                    return render(request, 'accounts/error.html', {'txt': result['message']})

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + \
                    str(status) + "   |   " + "Description : " + \
                    idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return render(request, 'accounts/error.html', {'txt': txt})


def payment_check(request, pk):

    payment = MainPayed.objects.get(pk=pk)

    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:

        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()

    return render(request, 'accounts/error.html', {'txt': result['message']})
