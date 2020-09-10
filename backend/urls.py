from django.contrib import admin
from django.urls import path, re_path
from backend.views import user
from backend.views import trouble

urlpatterns = [
    re_path('index/', user.index),
    re_path('backend_article-(?P<category_id>\d+)-(?P<tags>\d+).html$', user.backend_article),
    re_path('backend_article-create.html$', user.article_create),
    re_path('backend_article-edit-(\d+).html$', user.article_edit),
    re_path('backend_article-del.html$', user.article_del),
    # 一般用户:提交报障单,查看修改(未处理)
    path('trouble-list.html', trouble.trouble_list),
    path('trouble-create.html', trouble.trouble_create),
    re_path('trouble-edit-(\d+).html$', trouble.trouble_edit),
    re_path('trouble-kill-list.html$', trouble.trouble_kill),
    re_path('trouble-rob-(\d+).html$', trouble.trouble_rob),
    re_path('trouble-report.html$', trouble.trouble_report),
    re_path('trouble-json-report.html$', trouble.trouble_json_report),
]
