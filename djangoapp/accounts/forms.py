from django import forms
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='نام کاربری')
    password = forms.CharField(
        max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور')

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'password': forms.PasswordInput(attrs={'class': 'form-control'}),
    }
