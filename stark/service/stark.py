import functools
from types import FunctionType
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django import forms


class StarkConfig(object):

    def display_checkbox(self, row=None, header=False):
        if header:
            return "选择"
        return mark_safe("<input type='checkbox' name='pk' value='%s' />" % row.pk)

    def display_edit(self, row=None, header=False):
        if header:
            return "编辑"

        return mark_safe('<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a>' % self.reverse_edit_url(row))

    def display_del(self, row=None, header=False):
        if header:
            return "删除"

        return mark_safe('<a href="%s"><i class="fa fa-trash-o" aria-hidden="true"></i></a>' % self.reverse_del_url(row))

    def display_edit_del(self, row=None, header=False):
        if header:
            return "操作"
        tpl = """<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a> |
        <a href="%s"><i class="fa fa-trash-o" aria-hidden="true"></i></a>
        """ % (self.reverse_edit_url(row), self.reverse_del_url(row),)
        return mark_safe(tpl)

    order_by = []
    list_display = []
    model_form_class = None

    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site

    def get_order_by(self):
        return self.order_by

    def get_list_display(self):
        return self.list_display

    def get_add_btn(self):
        return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % self.reverse_add_url())

    def get_model_form_class(self):
        """
        获取ModelForm类
        :return:
        """
        if self.model_form_class:
            return self.model_form_class

        class AddModelForm(forms.ModelForm):

            class Meta:
                model = self.model_class
                fields = "__all__"

        return AddModelForm

    def changelist_view(self, request):
        """
        所有URL的查看列表页面
        :param request:
        :return:
        """
        queryset = self.model_class.objects.all().order_by(*self.get_order_by())

        # ##### 添加按钮 ######
        add_btn = self.get_add_btn()

        # ##### 作业一：处理表格 #####
        # inclusion_tag
        # 生成器
        list_display = self.list_display

        header_list = []
        if list_display:
            for name_or_func in list_display:
                if isinstance(name_or_func, FunctionType):
                    verbose_name = name_or_func(self, header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(
                        name_or_func).verbose_name
                header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)

        body_list = []
        for row in queryset:
            # ret = row
            # print('row', type(ret), ret)
            row_list = []
            if not list_display:
                row_list.append(row)
                body_list.append(row_list)
                continue
            for name_or_func in list_display:
                if isinstance(name_or_func, FunctionType):
                    val = name_or_func(self, row=row)
                else:
                    val = getattr(row, name_or_func)
                    # ret = val
                    # print('getattr(row, name_or_func)', type(ret), ret)
                row_list.append(val)
            body_list.append(row_list)
        ret = header_list
        print('header_list', type(ret), ret)
        ret = body_list
        print('body_list', type(ret), ret)

        return render(request, 'stark/changelist.html', {'header_list': header_list, 'body_list': body_list, 'add_btn': add_btn})

    def add_view(self, request):
        """
        所有添加页面，都在此函数处理
        使用ModelForm实现
        :param request:
        :return:
        """
        AddModelForm = self.get_model_form_class()
        if request.method == "GET":
            form = AddModelForm()
            return render(request, 'stark/change.html', {'form': form})

        form = AddModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def change_view(self, request, pk):
        """
        所有编辑页面
        :param request:
        :param pk:
        :return:
        """
        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('数据不存在')

        ModelFormClass = self.get_model_form_class()
        if request.method == 'GET':
            form = ModelFormClass(instance=obj)
            return render(request, 'stark/change.html', {'form': form})
        form = ModelFormClass(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def delete_view(self, request, pk):
        """
        所有删除页面
        :param request:
        :param pk:
        :return:
        """
        if request.method == "GET":
            return render(request, 'stark/delete.html', {'cancel_url': self.reverse_list_url()})

        self.model_class.objects.filter(pk=pk).delete()
        return redirect(self.reverse_list_url())

    def wrapper(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    def get_urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            url(r'^list/$', self.wrapper(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^add/$', self.wrapper(self.add_view), name='%s_%s_add' % info),
            url(r'^(?P<pk>\d+)/change/', self.wrapper(self.change_view),
                name='%s_%s_change' % info),
            url(r'^(?P<pk>\d+)/del/', self.wrapper(self.delete_view),
                name='%s_%s_del' % info),
        ]

        extra = self.extra_url()
        if extra:
            urlpatterns.extend(extra)

        return urlpatterns

    def extra_url(self):
        pass

    def reverse_list_url(self):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_changelist' % (namespace, app_label, model_name)
        list_url = reverse(name)
        return list_url

    def reverse_add_url(self):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_add' % (namespace, app_label, model_name)
        add_url = reverse(name)
        return add_url

    def reverse_edit_url(self, row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_change' % (namespace, app_label, model_name)
        edit_url = reverse(name, kwargs={'pk': row.pk})
        return edit_url

    def reverse_del_url(self, row):
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = self.site.namespace
        name = '%s:%s_%s_del' % (namespace, app_label, model_name)
        del_url = reverse(name, kwargs={'pk': row.pk})
        return del_url

    @property
    def urls(self):
        return self.get_urls()


class AdminSite(object):

    def __init__(self):
        self._registry = {}
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, stark_config=None):
        if not stark_config:
            stark_config = StarkConfig
        self._registry[model_class] = stark_config(model_class, self)
        """
        {
            models.UserInfo: StarkConfig(models.UserInfo), # 封装：model_class=UserInfo，site=site对象
            models.Role: RoleConfig(models.Role)           # 封装：model_class=Role，site=site对象
        }
        """

    def get_urls(self):

        urlpatterns = []
        # urlpatterns.append(url(r'^x1/', self.x1))
        # urlpatterns.append(url(r'^x2/', self.x2))
        # urlpatterns.append(url(r'^x3/', ([
        #                                      url(r'^add/', self.x1),
        #                                      url(r'^change/', self.x1),
        #                                      url(r'^del/', self.x1),
        #                                      url(r'^edit/', self.x1),
        #                                  ],None,None)))

        for k, v in self._registry.items():
            # k=modes.UserInfo,v=StarkConfig(models.UserInfo), # 封装：model_class=UserInfo，site=site对象
            # k=modes.Role,v=RoleConfig(models.Role)           #
            # 封装：model_class=Role，site=site对象
            app_label = k._meta.app_label
            model_name = k._meta.model_name
            urlpatterns.append(
                url(r'^%s/%s/' % (app_label, model_name,), (v.urls, None, None)))
        return urlpatterns

    @property
    def urls(self):
        # 返回一个元组 包含三个值 替代路由继承中的include()
        return self.get_urls(), self.app_name, self.namespace


site = AdminSite()
