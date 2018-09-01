# cmpt_stark 组件：

## 功能：
自动对多张表增删改查。
    自动发现url（由单例模式、路由系统的namespace、启动文件）等知识点构建。
自定义复杂操作。

## 预留的钩子（7个）：
### 1. 排序规则
~~~
第一种方法：
class UserInfoConfig(StarkConfig):
    order_by = ['-id']
    list_display = ['id','title',StarkConfig.display_edit,StarkConfig.display_del]

site.register(models.UserInfo,UserInfoConfig)
第二种方法：
class UserInfoConfig(StarkConfig):
    list_display = ['id','title',StarkConfig.display_edit,StarkConfig.display_del]

    def get_order_by(self):
        return ['-id']
site.register(models.UserInfo,UserInfoConfig)
~~~

### 2. 显示列
备注：可以在此钩子函数内过滤权限。
~~~
第一种方法：
class UserInfoConfig(StarkConfig):
    list_display = ['id','title',StarkConfig.display_edit,StarkConfig.display_del]
site.register(models.UserInfo,UserInfoConfig)
第二种方法：
class UserInfoConfig(StarkConfig):
    order_by = ['-id']

    def get_list_display(self):
        return  ['id','title',StarkConfig.display_edit,StarkConfig.display_del]
~~~

### 3. 添加按钮
~~~
class UserInfoConfig(StarkConfig):
    list_display = ['id','title',StarkConfig.display_edit,StarkConfig.display_del]
    def get_add_btn(self):
        # 显示 
        # return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % self.reverse_add_url())
        
        # 不显示
        return None 
        
site.register(models.UserInfo,UserInfoConfig)
~~~

### 4. 定制ModelForm
~~~
第一种方法：统一使用基类返回ModelForm。
class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Depart
        fields = "__all__"

    def clean_name(self):
        return self.cleaned_data['name']

class DepartConfig(StarkConfig):
    list_display = [StarkConfig.display_checkbox,'id', 'name', 'tel', 'user',StarkConfig.display_edit_del]
    model_form_class = DepartModelForm
第二种方法：自己定义ModelForm。
class DepartModelForm(forms.ModelForm):
    class Meta:
        model = models.Depart
        fields = "__all__"

    def clean_name(self):
        return self.cleaned_data['name']

class DepartConfig(StarkConfig):
    list_display = [StarkConfig.display_checkbox,'id', 'name', 'tel', 'user',StarkConfig.display_edit_del]
    
    def get_model_form_class(self):

            return DepartModelForm
~~~

### 5. 自定义列表页面
在基类重写列表views函数changelist_view
~~~
class DepartConfig(StarkConfig):
    list_display = [StarkConfig.display_checkbox,'id', 'name', 'tel', 'user',StarkConfig.display_edit_del]
    model_form_class = DepartModelForm

    def changelist_view(self, request):
        return HttpResponse('自定义列表页面')

site.register(models.Depart, DepartConfig)
~~~

### 6. 增加URL
在基类重写预留的钩子函数extra_url
~~~
class RoleConfig(StarkConfig):

    order_by = ['-id', ]
    list_display = [StarkConfig.display_checkbox,'id','title',StarkConfig.display_edit,StarkConfig.display_del]

    def extra_url(self):
        data = [
            url(r'^xxxxxxx/$', self.xxxxxx),
        ]

        return data

    def xxxxxx(self,request):
        print('....')

        return HttpResponse('xxxxx')

site.register(models.Role,RoleConfig)
~~~

### 7. 自定制URL：自定义选择生成4个url中的某几个
在基类重写get_urls
~~~
class RoleConfig(StarkConfig):

    order_by = ['-id', ]
    list_display = [StarkConfig.display_checkbox,'id','title']

    def get_add_btn(self):
        return False
    
    def extra_url(self):
        data = [
            url(r'^xxxxxxx/$', self.xxxxxx),
        ]

        return data

    def xxxxxx(self,request):
        print('....')
        return HttpResponse('xxxxx')


    def get_urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            url(r'^list/$', self.wrapper(self.changelist_view), name='%s_%s_changelist' % info),
        ]

        extra = self.extra_url()
        if extra:
            urlpatterns.extend(extra)

        return urlpatterns

site.register(models.Role,RoleConfig)
~~~