from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse

from repository import models
from ..forms.article import ArticleForm

# Create your views here.


def index(request):
    try:
        nickname = request.session['user_info']['nickname']  # 没登录 拿不到session就会报错
        return render(request, 'backend_index.html', {'nickname': nickname})
    except Exception as e:
        return redirect("/login.html")


def backend_article(request, *args, **kwargs):
    try:
        blog_site = request.session['user_info']['blog__site']
    except:
        return redirect("/login.html")
    blog = models.Blog.objects.filter(site=blog_site).select_related('user').first()
    category_list = models.Category.objects.filter(blog=blog).values('title', 'nid')
    tag_list = models.Tag.objects.filter(blog=blog).values('title', 'nid')

    blog_id = request.session['user_info']['blog__nid']
    conditions = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            conditions[k] = v
    conditions['blog_id'] = blog_id
    article_count = models.Article.objects.filter(**conditions).count()
    article_list = models.Article.objects.filter(**conditions).all()
    return render(request, 'backend_article.html',
                  {
                      'blog': blog,
                      'category_list': category_list,
                      'tag_list': tag_list,
                      'article_count': article_count,
                      'article_list': article_list,
                      'kwargs': kwargs,
                  })


def article_create(request):
    if request.method == 'GET':
        try:
            blog_id = request.session['user_info']['blog__nid']
        except:
            return redirect("/login.html")
        form = ArticleForm(request=request)
        return render(request, 'backend_article_create.html', {'form': form})

    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作,方便出错回滚
                tags = form.cleaned_data.pop('tags')  # 只能选数据库本身有的tag,不能直接存进去
                # 把提交过来的content去除掉,因为models字段里面没有
                content = form.cleaned_data.pop('content')
                # 理论上content应该加一个防止XSS攻击
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']
                # print(form.cleaned_data)
                obj = models.Article.objects.create(**form.cleaned_data)
                models.ArticleDetail.objects.create(content=content, article=obj)
                tag_list = []
                for tag_id in tags:  # 文章分类是多选
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)  # 批量插入数据

            return redirect('/backend/backend_article-0-0.html')
        else:
            return render(request, 'backend_article_create.html', {'form': form})
    else:
        return redirect('/')


def article_del(request):
    article_nid = request.GET.get('article_nid')
    msg = '成功'
    try:
        models.Article.objects.filter(nid=article_nid).first().delete()
    except Exception as e:
        mag = str(e)
    return HttpResponse(msg)


def article_edit(request, nid):
    try:
        blog_id = request.session['user_info']['blog__nid']
    except:
        return redirect("/login.html")
    if request.method == 'GET':
        article_obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
        content_dict = models.ArticleDetail.objects.filter(article=article_obj).values('content').first()
        tag_id = article_obj.tags.values_list('nid')
        print(tag_id)
        if tag_id:
            tag_id = list(zip(*tag_id))[0]
        print(tag_id)
        condition = {
            'nid': article_obj.nid,
            'title': article_obj.title,
            'summary': article_obj.summary,
            'content': content_dict['content'],
            'article_type_id': article_obj.article_type_id,
            'category_id': article_obj.category_id,
            'tags': tag_id
        }
        form = ArticleForm(request=request, data=condition)
        return render(request, 'backend_article_edit.html', {'form': form, 'nid': nid})

    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(
                nid=nid, blog_id=blog_id).first()
            with transaction.atomic():  # 事务操作,方便出错回滚
                tags = form.cleaned_data.pop('tags')  # 只能选数据库本身有的tag,不能直接存进去
                # 把提交过来的content去除掉,因为models字段里面没有
                content = form.cleaned_data.pop('content')
                # 理论上content应该加一个防止XSS攻击
                models.Article.objects.filter(
                    nid=obj.nid).update(
                    **form.cleaned_data)
                models.ArticleDetail.objects.filter(
                    article=obj).update(content=content)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:  # 文章分类是多选
                    tag_id = int(tag_id)
                    tag_list.append(
                        models.Article2Tag(
                            article_id=obj.nid,
                            tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)  # 批量插入数据
            return redirect('/backend/backend_article-0-0.html')
        else:
            return render(
                request, 'backend_article_edit.html', {
                    'form': form, 'nid': nid})
    else:
        return redirect('/')
