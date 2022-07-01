from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterNewUserAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),

]
