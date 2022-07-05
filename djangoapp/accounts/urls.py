from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterNewUserAPIView.as_view(), name='register'),
    path('set_phone_number/', views.SetUserPhoneNumberAPIView.as_view(), name='set_phone_number'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

]
