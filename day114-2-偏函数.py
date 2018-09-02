""""""
import functools

def func(a1,a2):
    print(a1+a2)

new_func = functools.partial(func,8)

new_func(7)
new_func(2)
new_func(8)