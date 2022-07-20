from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterNewUserAPIView.as_view(), name='register'),
    path('set_phone_number/', views.SetUserPhoneNumberAPIView.as_view(), name='set_phone_number'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('delete_word/', views.DeleteKeywordAPIView.as_view(), name='delete_word'),

# templates
    path('final_register/', views.FinalRegisterTemplateView.as_view(),
         name='final_register'),

    path('login_template/', views.LoginTemplateView.as_view(), name='login'),
    path('card/', views.CardTemplateView.as_view(), name='card'),
    path('select_plan/', views.SelectPlanTemplateView.as_view(), name="select_plan"),

    # //
    path('payment', views.payment_start, name='payment_start'),
    path('payment/return', views.payment_return, name='payment_return'),
    path('payment/check/<pk>', views.payment_check, name='payment_check'),
]
