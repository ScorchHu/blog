from django.core.exceptions import ValidationError
from django import forms
from django.forms import fields, widgets

from repository import models
from .baseForm import BaseForm


class LoginForm(BaseForm, forms.Form):
    username = fields.CharField()
    password = fields.CharField()
    rmb = fields.IntegerField(required=False)
    check_code = fields.CharField(error_messages={'required':'验证码不能为空'})

    def clean_check_code(self):
    # 对比验证码,不区分大小写,同一大写
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误',code='invalid')


class RegisterForm(BaseForm, forms.Form):
    username = fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.',
                        'min_length': "用户名长度不能小于6个字符",
                        'max_length': "用户名长度不能大于32个字符"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'id': "username"})
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': "email"})
    )
    password = fields.RegexField(
        r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=8,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字、字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': "password"})
    )
    confirm_password = fields.CharField(
        min_length=8,
        max_length=32,
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': "confirm-password"})
    )

    def clean_confirm_password(self):
        if self.request.POST.get('password') != self.request.POST.get('confirm_password'):
            raise ValidationError(message='两次密码输入不一致', code='invalid')
