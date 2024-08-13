from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer
from captcha.fields import CaptchaField

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Xác thực mật khẩu', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Tên đăng nhập',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(label=_("Tên đăng nhập"), widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_("Mật khẩu"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'current-password', 'class': 'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password =  forms.CharField(label=_("Mật khẩu cũ"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("Mật khẩu mới"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password', 'class': 'form-control'}), 
    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Xác nhận mật khẩu"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password', 'class': 'form-control'}))
   
class MyPasswordResetForm(PasswordResetForm):
    email= forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs=
    {'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Nhập email tài khoản'}))

class MySetPasswordForm(SetPasswordForm):
     new_password1 = forms.CharField(label=_("Nhập mật khẩu mới"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password', 'class': 'form-control'}), 
    help_text=password_validation.password_validators_help_text_html())
     new_password2 = forms.CharField(label=_("Xác nhận mật khẩu"), strip=False, widget=forms.PasswordInput(attrs=
    {'autocomplete': 'new-password', 'class': 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        labels = {
            'name': 'Tên khách hàng',
            'locality': 'Nơi cư trú',
            'city': 'Thành phố',
            'state': 'Tỉnh',
            'zipcode': 'Mã bưu chính'
        }
        widgets = {'name':forms.TextInput(attrs=
        {'class': 'form-control'}), 'locality':forms.TextInput(attrs=
        {'class': 'form-control'}), 'city': forms.TextInput(attrs=
        {'class': 'form-control'}),
        'state': forms.Select(attrs={'class': 'form-control'}),
        'zipcode': forms.NumberInput(attrs={'class': 'form-control'})
        }
