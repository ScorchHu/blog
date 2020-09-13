"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from web.views import home, account, index

urlpatterns = [
    # Index
    path('', index.index),
    re_path(r'all/(?P<article_type_id>\d+).html$', index.index, name='index'),
    re_path(r'article/(\d+)/$', index.article_detail),
    re_path(r'login.html$', account.login),
    re_path(r'logout.html$', account.logout),
    re_path(r'register.html$', account.register),
    re_path(r'check_code.html$', account.check_code),

    # Home
    re_path(r'(?P<site>\w+)/(?P<condition>((tag)|(category)|(date)))/(?P<index1>\w+-*\w*).html$', home.filter),
    re_path(r'(?P<site>\w+)/(?P<article_id>\w+-*\w*).html$', home.detail),
    re_path(r'(?P<site>\w+).html$', home.home),
]
