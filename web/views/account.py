import json
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse
from django import forms
from django.forms import fields, widgets

from repository import models
from untils.check_code import create_validate_code
from ..forms.accountForm import LoginForm
# Create your views here.


def login(request):
    # 账号登陆
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        print(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. filter(
                username=username,
                password=password). values(
                'nid',
                'nickname',
                'username',
                'email',
                'avatar',
                'blog__nid',
                'blog__site').first()

            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True  # 验证通过
                request.session['user_info'] = user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 免登录1个月

        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))


def check_code(request):
    # 验证码
    f = BytesIO()                       # 放在内存中
    img, code = create_validate_code()
    request.session['CheckCode'] = code  # 把验证码放在session,方便后面和输入的作比较
    img.save(f, 'PNG')                  # 生成后放在内存

    return HttpResponse(f.getvalue())   # 获取内存中的f图片


def register(request):
    # 账号注册
    return render(request, 'register.html')


def logout(request):
    # 账号退出
    request.session.clear()
    return redirect("/")


# -------------------验证码测试----------------
def test(request):
    if request.method == "GET":
        return render(request, 'test.html')
    else:
        input_coded = request.POST.get('code')
        check_code1 = request.session['check_code']
        print(input_coded, check_code1)
        return HttpResponse('....')


def yanzheng(request):
    # img获取图片的第二种方法
    # f=open('static/cankao/1.jpg','rb')
    # data = f.read()
    # f.close()

    # 调用自动生成验证码文件
    # #实质:把随机生成的字符串写到一张空白图片上,放在内存再返回给前端
    f = BytesIO()  # 放在内存中
    img, code = create_validate_code()
    request.session['check_code'] = code  # 把验证码放在session,方便后面和输入的作比较
    img.save(f, 'PNG')  # 生成后放在内存

    return HttpResponse(f.getvalue())  # 获取内存中的f图片


def upload(request):
    print(request.FILES)
    dic = {
        'error': 0,
        'url': '/static/img/6.jpg',
        'message': '错误了...'
    }

    return JsonResponse(dic)
