from django.shortcuts import render, redirect, HttpResponse
from repository import models
from django.forms import Form, fields, widgets
import datetime
import json


# Create your views here.
def trouble_list(request):
    # 报障单列表
    try:
        current_user_id = request.session['user_info']['nid']
    except:
        return redirect("/login.html")
    result = models.Trouble.objects.filter(user_id=current_user_id).\
        order_by('status').only('title', 'status', 'processer', 'ctime')
    return render(request, 'backend_trouble_list.html', {'result': result})


class TroubleMaker(Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'detail', 'class': 'kind-content'})  # 生成的标签有id属性
    )


def trouble_create(request):
    # 创建报障单
    if request.method == 'GET':
        form = TroubleMaker()
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            # form.cleaned_data 里面只有 title,content
            dic = {}
            dic['user_id'] = 1
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)
            models.Trouble.objects.create(**dic)
            return redirect('/backend/trouble-list.html')
    return render(request, 'backend_trouble_create.html', {'form': form})


def trouble_edit(request, nid):
    if request.method == 'GET':
        obj = models.Trouble.objects.filter(id=nid, status=1).only('id', 'title', 'detail').first()
        if not obj:
            return HttpResponse('已处理中的报障单无法修改')
        # form里加了initial 显示时如果为空值,不会报错
        form = TroubleMaker(initial={'title': obj.title, 'detail': obj.detail})
        return render(request, 'backend_trouble_edit.html', {'form': form, 'nid': nid})
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            v = models.Trouble.objects.filter(id=nid, status=1).update(**form.cleaned_data)
            # v返回的是更新的数目
            if not v:  # 0
                return HttpResponse('已经被处理')
            else:
                return redirect('/backend/trouble-list.html')


def trouble_kill(request):
    from django.db.models import Q
    current_user_id = 1  # 获取当前处理者id 此处为了方便设为 1
    result = models.Trouble.objects.filter(Q(processer_id=current_user_id) | Q(status=1)).order_by('status')
    return render(request, 'backend_trouble_kill.html', {'result': result})


class Troublehandel(Form):
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'solution', 'class': 'kind-content'})  # 生成的标签有id属性
    )


def trouble_rob(request, nid):
    current_user_id = 1  # 获取当前处理者id 此处为了方便设为 1
    if request.method == 'GET':
        ret = models.Trouble.objects.filter(id=nid, processer=current_user_id).count()  # 表明是我的单子
        if not ret:  # 如果不是我的单子,去抢单
            v = models.Trouble.objects.filter(id=nid, status=1).update(processer_id=current_user_id, status=2)
            if not v:
                return HttpResponse('手速太慢了')
        # 抢到报障单,跳转到处理页面
        obj = models.Trouble.objects.filter(id=nid).first()
        form = Troublehandel(initial={'title': obj.title, 'detail': obj.detail, 'solution': obj.solution})
        return render(request, 'backend_trouble_handel.html', {'obj': obj, 'form': form, 'nid': nid, })
    else:
        ret = models.Trouble.objects.filter(id=nid, processer=current_user_id, status=2).count()
        if not ret:
            return HttpResponse('这不是你的单子')
        print(request.POST)
        form = Troublehandel(request.POST)
        if form.is_valid():
            dic = {}
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            dic['ptime'] = datetime.datetime.now()
            models.Trouble.objects.filter(id=nid, processer=current_user_id, status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
            # return HttpResponse('处理成功')
        obj = models.Trouble.objects.filter(id=nid).first()
        return render(request, 'backend_trouble_handel.html', {'obj': obj, 'form': form, 'nid': nid, })


def trouble_report(request):
    return render(request, 'backend_trouble_report.html')


def trouble_json_report(request):
    user_list = models.UserInfo.objects.filter()
    response = []
    for user in user_list:
        from django.db import connection, connections
        from django.core.serializers import serialize
        cursor = connection.cursor()
        cursor.execute(
            """select date_format(date_format(ctime,'%%Y-%%m-01'),'%%s') * 1000,count(id) from repository_trouble where processer_id = %s group by date_format(ctime,'%%Y-%%m')""",
            [user.nid, ])
        # cursor.execute("""select ctime,COUNT(id) from repository_trouble where processer_id = %s GROUP BY ctime """, [user.nid,])
        # cursor.execute("""select strftime('%%s',strftime("%%Y-%%m-01",ctime)) * 1000,count(id) from repository_trouble where processer_id = %s group by strftime("%%Y-%%m",ctime)""", [user.nid,])

        result = cursor.fetchall()
        print(user.username, result)
        temp = {
            'name': user.username,
            'data': result,
        }
        response.append(temp)
    return HttpResponse(json.dumps(response))
