from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from untils.pager import Pagination
from django.urls import reverse

from repository import models
# Create your views here.


def index(request, *args, **kwargs):
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)
    else:
        article_type_id = None
        base_url = '/'

    data_count = models.Article.objects.filter(**kwargs).count()
    current_page = request.GET.get('p')
    page_obj = Pagination(data_count, current_page, 4, 7)  #每页显示的数据数, 最多显示的页数
    page_str = page_obj.page_str(base_url)  # 后端生成页码

    article__list = models.Article.objects.filter(**kwargs).all()[page_obj.start():page_obj.end()]
    article_type_list = models.Article.type_choices

    rec_list = models.Article.objects.filter().all()[0:8]
    comm_list = models.Article.objects.filter().all().order_by('-comment_count')[0:8]
    return render(request, 'index.html',
                  {
                      'article_type_list': article_type_list,
                      'article__list': article__list,
                      'rec_list':rec_list,
                      'comm_list':comm_list,
                      'article_type_id': article_type_id,
                      'page_str': page_str,
                  })


def article_detail(request, article_id):
    article_type_list = models.Article.type_choices
    rec_list = models.Article.objects.filter().all()[0:8]
    comm_list = models.Article.objects.filter().all().order_by('-comment_count')[0:8]
    comment_list = models.Comment.objects.filter(article_id=article_id).select_related('reply')
    article_detail = models.ArticleDetail.objects.filter(article_id=article_id). \
        values('content',
               'article__title',
               'article__up_count',
               'article__down_count',
               'article__create_time',
               'article__comment_count',
               'article__read_count').first()
    return render(request,'index_article_detail.html',
                  {
                      'article_type_list': article_type_list,
                      'article_detail': article_detail,
                      'rec_list': rec_list,
                      'comm_list': comm_list,
                      'comment_list': comment_list,
                  })