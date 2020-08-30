from django.shortcuts import render,HttpResponse,redirect
from repository import models
from untils.pager import Pagination
from django.urls import reverse

# Create your views here.

def index(request,*args,**kwargs):

    if kwargs:
        article_type_id=int(kwargs['article_type_id'])
        base_url= reverse('index',kwargs=kwargs)
    else:
        article_type_id=None
        base_url='/'

    data_count =models.Article.objects.filter(**kwargs).count()
    current_page=request.GET.get('p')
    page_obj=Pagination(data_count,current_page,4,7)
    page_str = page_obj.page_str(base_url)          #后端生成页码

    article__list=models.Article.objects.filter(**kwargs).all()[page_obj.start():page_obj.end()]
    article_type_list=models.Article.type_choices

    return render(request,'index.html',
                  {
                      'article_type_list':article_type_list,
                      'article__list':article__list,
                      'article_type_id':article_type_id,
                      'page_str':page_str,
                  })

def home(request,*args,**kwargs):
    print(args)
    print(kwargs)
    blog=models.Blog.objects.filter(site=kwargs['site']).select_related('user').first()
    if not blog:
        redirect('/')
    tag_list=models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article GROUP BY create_time '
    )
    print(date_list)
    article_list = models.Article.objects.filter(blog=blog).all()

    return render(request, 'home.html',
                  {
                      'blog':blog,
                       'tag_list':tag_list,
                       'category_list':category_list,
                       'date_list':date_list,
                       'article_list':article_list,
                  })

def filter(request,site,condition,index1):
    # tag2=models.Article.objects.filter(tags=).values('title')
    # print(tag2)
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article GROUP BY create_time '
    )
    templates='home_category_date.html'
    if condition=='tag':
        article_list = models.Article.objects.filter(tags=index1,blog=blog).all()
        templates='home_tag.html'
    elif condition=='category':
        article_list = models.Article.objects.filter(category_id=index1, blog=blog).all()
    elif condition=='date':
        article_list = models.Article.objects.filter(nid=index1, blog=blog).all()
    else:
        article_list=[]
    return render(request,templates,
                  {
                      'blog':blog,
                       'tag_list':tag_list,
                       'category_list':category_list,
                       'date_list':date_list,
                       'article_list':article_list,
                   })

def detail(request,site,article_id):
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        redirect('/')

    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select create_time,COUNT(nid) as num ,nid from repository_article GROUP BY create_time '
    )
    comment_list = models.Comment.objects.filter(article_id=article_id).select_related('reply')
    article_detail=models.ArticleDetail.objects.filter(article_id=article_id).\
        values('content',
               'article__title',
               'article__up_count',
               'article__down_count',
               'article__create_time',
               'article__comment_count',
               'article__read_count').first()

    return render(request,'home_detail.html',
                  {
                      'blog': blog,
                      'tag_list': tag_list,
                      'category_list': category_list,
                      'date_list': date_list,
                      'article_detail':article_detail,
                      'comment_list':comment_list,
                  })


