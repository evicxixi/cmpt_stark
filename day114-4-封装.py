""""""
list_filter = [
    '董方方',
    '黄晓雪',
    '李贝贝',

]

# ############################ 老封装思想 ############################

list_filter = [
    {'text':'董方方','gender':'男','color':'xx'}, # 字典对象做封装
    {'text':'黄晓雪','gender':'男','color':'xx'},
    {'text':'李贝贝','gender':'男','color':'xx'},
]


for item in list_filter:
    print(item['text'] + item['gender'])


# ############################ 老封装思想 ############################
class Option(object):
    def __init__(self,text,gender,color):
        self.text = text
        self.gender = gender
        self.color = color

    def get_t_g(self):
        return self.text +self.gender

list_filter = [
    Option(text='董方方',gender='男',color = 'xx'), # 字典对象做封装
    Option(text='黄晓雪',gender='男',color = 'xx'), # 字典对象做封装
    Option(text='李贝贝',gender='男',color = 'xx'), # 字典对象做封装
]

for item in list_filter:
    print(item.get_t_g())






# 内部需要辨别：谁是单选和多选？






