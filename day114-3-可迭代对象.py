""""""

"""
li = [11,22,33] # list类的一个对象

for item in li:
    print(item)
"""

"""
class Foo(object):

    def __iter__(self):

        # return iter([11,22,33,44]) # 返回迭代器

        yield 11        # 返回生成器（迭代器的一种）
        yield 22
        yield 33

obj = Foo()  # list类的一个对象
for item in obj:
    print(item)
"""


class Row(object):
    def __init__(self,data):
        self.data = data

    def __iter__(self):
        yield "<div>"
        yield '全部'
        for item in self.data:
            yield "<a href='/index/?p1=1.0'>%s</a>" %item
        yield "</div>"

data_list= [
    Row(['1.0以下','1.1-1.6']),
    Row(['汽油','柴油','混合动力','电动']),
]

for row in data_list:
    for field in row:
        print(field)









