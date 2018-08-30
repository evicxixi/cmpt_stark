import functools

def wrapper(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@wrapper
def f1():
    print('f1')

@wrapper
def f2():
    print('f1')


print(f1.__name__)
print(f2.__name__)