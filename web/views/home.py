from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.views.decorators.cache import cache_page

from repository import models
# Create your views here.

@cache_page(60 * 15)
def home(request, *args, **kwargs):
    blog = models.Blog.objects.filter(site=kwargs['site']).select_related('user').first()
    if not blog:
        redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article WHERE repository_article.blog_id = %d GROUP BY create_time  ' %blog.nid
    )
    if request.method == "GET":
        article_list = models.Article.objects.filter(blog=blog).all()
    elif request.method == "POST":
        article_list = models.Article.objects.filter(Q(title__contains=request.POST.get("search")), blog=blog).all()
    return render(request, 'home.html',
                  {
                      'blog': blog,
                      'tag_list': tag_list,
                      'category_list': category_list,
                      'date_list': date_list,
                      'article_list': article_list,
                  })


def filter(request, site, condition, index1):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article WHERE repository_article.blog_id = %d GROUP BY create_time  ' %blog.nid
    )
    templates = 'home_category_date.html'
    if condition == 'tag':
        article_list = models.Article.objects.filter(tags=index1, blog=blog).all()
        templates = 'home_tag.html'
    elif condition == 'category':
        article_list = models.Article.objects.filter(category_id=index1, blog=blog).all()
    elif condition == 'date':
        article_list = models.Article.objects.filter(nid=index1, blog=blog).all()
    else:
        article_list = []
    return render(request, templates,
                  {
                      'blog': blog,
                      'tag_list': tag_list,
                      'category_list': category_list,
                      'date_list': date_list,
                      'article_list': article_list,
                  })


@cache_page(60 * 15)
def detail(request, site, article_id):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article WHERE repository_article.blog_id = %d GROUP BY create_time  ' %blog.nid
    )
    comment_list = models.Comment.objects.filter(article_id=article_id).select_related('reply')
    article_detail = models.ArticleDetail.objects.filter(article_id=article_id). \
        values('content',
               'article__title',
               'article__up_count',
               'article__down_count',
               'article__create_time',
               'article__comment_count',
               'article__read_count').first()

    return render(request, 'home_detail.html',
                  {
                      'blog': blog,
                      'tag_list': tag_list,
                      'category_list': category_list,
                      'date_list': date_list,
                      'article_detail': article_detail,
                      'comment_list': comment_list,
                  })
