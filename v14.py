#!python
#coding: utf-8
'''正则表达式简化：/student/{name:str}/{id:str}'''
#类型设计，支持str、word、int、float、any类型
'''
    str [^/]+   不包含/的任意类型
    word    \w+ 字母和数字
    int [+-]?\d+    纯数字，正负数
    float   [+-]?\d+.\d+
    any .+  包含/的任意字符   
'''
#/student/{name:str}/xxx/{id:str} ->/student/(?P<name>[^/]+)/xxx/(?P<id>[+-]?\d+)
from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server
from re import compile

#把字典转换成.属性的访问方式.如d['key'] -> d.key
class DictObj:
    def __init__(self,d:dict):
        if not isinstance(d,(dict,)):
            self.__dict__['_dict'] = {}
        else:
            self.__dict__['_dict'] = d
    def __getattr__(self,item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format(item))
    #不允许设置属性
    def __setattr__(self,key,value):
        raise NotImplementedError('Attribute {} Not Implemented'.format(key))
        #raise NotImplementedError

class Router:
    KVPATTERN = compile(r'/({[^{}:]+:?[^{}:]*})')
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
    def transform(self,kv:str):
        name, _, type = kv.strip('/{}').partition(":")
        return '/(?P<{}>{})'.format(name, self.TYPEPATTERNS.get(type,r'\w+')),name, self.TYPECAST.get(type,str)

    def parse(self,src:str):
        start = 0
        res = ''
        translator = {}
        while True:
            matcher = self.KVPATTERN.search(src, start)
            if matcher:
                res += matcher.string[start:matcher.start()]
                tmp = self.transform(matcher.string[matcher.start():matcher.end()])
                res += tmp[0]
                translator[tmp[1]] = tmp[2]
                start = matcher.end()
            else:
                break
        if res:
            return res, translator
        else:
            return src, translator
    def __init__(self,prefix:str=''):
        self.__prefix = prefix.rstrip('/\\')
        self.__routetable = []
    @property
    def prefix(self):
        return self.__prefix
    def route(self,rule,*methods):
        def wrapper(handler):
            pattern, translator = self.parse(rule)
            self.__routetable.append((methods, compile(pattern), translator, handler))
            return handler
        return wrapper
    def get(self,pattern):
        return self.route(pattern,'GET','POST')
    def post(self,pattern):
        return self.route(pattern,'POST')
    def head(self,pattern):
        return self.route(pattern,'HEAD')
    def match(self,request:Request) -> Response:
        #return self.ROUTETABLE.get(request.path,self.notfound)(request)
        if not request.path.startswith(self.prefix):
            return None
        for methods, pattern, translator, handler in self.__routetable:
            #methods为None时表示支持任意http请求方法
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.prefix,'',1))
                if matcher:
                    newdict = {}
                    for k, v in matcher.groupdict().items():
                        newdict[k] = translator[k](v)
                    request.vars = DictObj(newdict) #request.vars.id    request.vars.name
                    return handler(request)


class Application:
    #路由表
    ROUTERS = []

    @classmethod
    def register(cls,router:Router):
        cls.ROUTERS.append(router)

    @dec.wsgify
    def __call__(self,request:Request) -> Response:
        for router in self.ROUTERS:
            response = router.match(request)
            if response:
                return response
        raise exc.HTTPNotFound("您访问的网页被外星人劫持了")

idx = Router()
py = Router('/python')
Application.register(idx)
Application.register(py)

@idx.get(r'^/$') #只匹配根/
def index(request:Request):
    res = Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v14'
    return res
@py.post(r'/{name}/{id}') #匹配/python/xxx/123
def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1> {}".format(request.vars.id).encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v14'
    return res

def main():
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip,port,Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

if __name__ == '__main__':
    main()