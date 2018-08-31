from django.template import Library
from django.conf import settings
from types import FunctionType
from stark.service import pagination
from stark.utlis import generater

register = Library()


@register.inclusion_tag('stark/list.html')
def list(self, request):
    """
    所有URL的查看列表页面
    :param request:
    :return:
    """

    # ##### 添加按钮 ######
    add_btn = self.get_add_btn()

    # ##### 处理表格 #####
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

    queryset = self.model_class.objects.all().order_by(*self.get_order_by())
    generater_obj = generater.generater(queryset)   # 赋值为生成器
    body_list = []
    for ret in range(len(queryset)):
        row = generater_obj.__next__()  # 循环调用生成器
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
    # ret = header_list
    # print('header_list', type(ret), ret)
    ret = body_list
    print('body_list', len(ret), type(ret))

    try:
        page_num = int(request.GET.get('page', 1))
    except Exception:
        page_num = 1
    page_obj = pagination.Pagination(page_num, len(body_list))
    # page_obj = pagination.Pagination(page_num, 7)

    data = body_list[page_obj.start:page_obj.end]

    return locals()
