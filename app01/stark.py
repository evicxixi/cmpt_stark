from stark.service.stark import site, StarkConfig
from app01 import models
from django import forms
from django.shortcuts import HttpResponse


class UserInfoConfig(StarkConfig):
    order_by = ['-id']
    list_display = ['id', 'title',
                    StarkConfig.display_edit, StarkConfig.display_del]

    def get_list_display(self):
        return ['id', 'title', StarkConfig.display_edit, StarkConfig.display_del]


site.register(models.UserInfo, UserInfoConfig)


class DepartModelForm(forms.ModelForm):

    class Meta:
        model = models.Depart
        fields = "__all__"

    def clean_name(self):
        return self.cleaned_data['name']


class DepartConfig(StarkConfig):
    list_display = [StarkConfig.display_checkbox, 'id',
                    'name', 'tel', 'user', StarkConfig.display_edit_del]
    model_form_class = DepartModelForm

    # StarkConfig的派生类内可重写视图函数 如下
    # def changelist_view(self, request):
    #     return HttpResponse('自定义列表页面')


site.register(models.Depart, DepartConfig)
