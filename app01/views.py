from django.shortcuts import render
from django.shortcuts import HttpResponse,redirect
from django.urls import reverse

def login(request):
    url1 = reverse('rbac:xxx:n1')
    url2 = reverse('rbac:xxx:n2')

    print(url1)
    print(url2)
    return HttpResponse('login')

def logout(request):
    return HttpResponse('logout')

def add(request):
    return HttpResponse('add')

def change(request):
    return HttpResponse('change')

import copy

def test(request):
    from django.http.request import QueryDict
    url_params_str = request.GET.urlencode() # _filter = k1=v1&k2=v2&k2=v3

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = url_params_str

    new_params = query_dict.urlencode()

    target_url = "/add_stu/?%s" %new_params
    return redirect(target_url)


def add_stu(request):

    if request.method == "GET":
        return render(request,'add_stu.html')
    # 接收到数据，保存到数据库
    origin_params = request.GET.get('_filter')
    back_url = "/test/?%s" %origin_params
    return redirect(back_url)


def get_fk_queryset(request):
    from app01 import models

    fk_obj = models.Depart._meta.get_field("user")
    user_info_queryset = fk_obj.rel.model.objects.all()
    print(user_info_queryset)

    return HttpResponse('...')

















