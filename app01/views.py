from django.shortcuts import render
from django.shortcuts import HttpResponse
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


def test(request):
    from app01 import models

    list_display = ['id','title']


    header_list = []
    for name in list_display:
        header_list.append(models.UserInfo._meta.get_field(name).verbose_name)
    print(header_list)

    user_queryset = models.UserInfo.objects.all()
    for item in user_queryset:
        row = []
        for field in list_display:
            row.append(getattr(item,field))
        print(row)

    return HttpResponse('...')





















