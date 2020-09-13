import json
import hashlib
from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse

from repository import models
from untils.check_code import create_validate_code
from ..forms.accountForm import LoginForm, RegisterForm
# Create your views here.


def get_sign_sha1(res):
    """
    使用sha1加密,返回str加密后的字符串
    """
    obj = hashlib.sha1()
    obj.update(bytes(res,encoding='utf-8'))
    return obj.hexdigest().upper()


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
            password = get_sign_sha1(form.cleaned_data.get('password'))
            user_info = models.UserInfo.objects.filter(
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
    if request.method == "GET":
        form = RegisterForm(request=request)
    elif request.method == "POST":
        form = RegisterForm(request=request, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.cleaned_data.pop("confirm_password")
            form.cleaned_data['password'] = get_sign_sha1(form.cleaned_data['password'])
            try:
                user_obj = models.UserInfo.objects.create(**form.cleaned_data)
            except:
                error ={"msg": "用户名或邮箱已被使用"}
                return render(request, 'register.html', {"form": form, "error": error})
            blog_data = {
                'title': form.cleaned_data['username'],
                'site': form.cleaned_data['username'],
                'theme': 'warm',
                'user_id': user_obj.nid
            }
            models.Blog.objects.create(**blog_data)
            return render(request,'register_success.html')
    return render(request, 'register.html', {"form": form})


def logout(request):
    # 账号退出
    request.session.clear()
    return redirect("/")


