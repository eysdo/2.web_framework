#!python
#coding: utf-8
from re import compile
pattern = compile(r'/({[^{}:]+:?[^{}:]*})')
s = '/student/{name:str}/xxx/{id:int}'
s1 = '/student/xxx/{id:int}/yyy'
s2 = '/student/xxx/5134678'
s3 = '/student/{name:}/xxx/{id}'
s4 = '/student/{name:}/xxx/{id:aaa}'
TYPEPATTERNS = {
    'str':r'[^/]+',
    'word':r'\w+',
    'int':r'[+-]?\d+',
    'float':r'[+-]?\d+\.\d+',
    'any':r'.+'
}

TYPECAST = {
    'str':str,
    'word':str,
    'int':int,
    'float':float,
    'any':str
}
def transform(kv:str):
    name, _, type = kv.strip('/{}').partition(":")
    return '/(?P<{}>{})'.format(name, TYPEPATTERNS.get(type,r'\w+')),name, TYPECAST.get(type,str)

def parse(src:str):
    start = 0
    res = ''
    translator = {}
    while True:
        matcher = pattern.search(src, start)
        if matcher:
            res += matcher.string[start:matcher.start()]
            tmp = transform(matcher.string[matcher.start():matcher.end()])
            res += tmp[0]
            translator[tmp[1]] = tmp[2]
            start = matcher.end()
        else:
            break
    if res:
        return res, translator
    else:
        return src, translator