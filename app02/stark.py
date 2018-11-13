from stark.service.stark import site,StarkConfig
from django.conf.urls import url
from django.shortcuts import HttpResponse
from app02 import models


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