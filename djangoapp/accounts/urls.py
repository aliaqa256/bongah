from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterNewUserAPIView.as_view(), name='register'),
    path('set_phone_number/', views.SetUserPhoneNumberAPIView.as_view(), name='set_phone_number'),
    path('login/', views.LoginAPIView.as_view(), name='login'),


# templates
    path('final_register/', views.FinalRegisterTemplateView.as_view(),
         name='final_register'),

    path('login_template/', views.LoginTemplateView.as_view(), name='login'),
]
