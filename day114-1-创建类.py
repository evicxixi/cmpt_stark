""""""

# ###################### 程序中的代码 ######################
"""
def gen_cls():

    class Foo(object):
        pass

    return Foo


cls = gen_cls()

print(cls)
"""
# ###################### 类和对象 ######################
# class Foo(object):
#     pass
#
# obj = Foo()

# ###################### 创建类:默认都是由type创建 ######################
name = "Foo"
country = "中国"
detail = lambda self, x: x + 1
# 根据以上三个参数创建一个类，类中有两个成员
"""
class Foo(object):
    country = '中国'
    def detail(self,x):
        return x + 1     
"""
cls = type(name, (object,), {'country': '中国', 'detail': lambda self, x: x + 1})

obj = cls()
print(obj.country)
print(obj.detail(100))
