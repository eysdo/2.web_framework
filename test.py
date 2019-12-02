#!python
#coding: utf-8

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            res = func(*args, **kw)
            return res
        return wrapper
    return decorator
@log('abc') #now = log('abc')(now)
def now():
    return '20191119'



print(now())