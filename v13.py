#!python
#coding: utf-8
'''支持路由分组：按照前缀分别映射，每个路径前缀对应一个路由实例'''
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

class Router:
    def __init__(self,prefix:str=''):
        self.__prefix = prefix.rstrip('/\\')
        self.__routetable = []
    @property
    def prefix(self):
        return self.__prefix
    def route(self,pattern,*methods):
        def wrapper(handler):
            self.__routetable.append((methods,compile(pattern), handler))
            return handler
        return wrapper
    def get(self,pattern):
        return self.route(pattern,'GET','POST')
    def post(self,pattern):
        return self.route(pattern,'POST')
    def head(self,pattern):
        return self.route(pattern,'HEAD')
    def match(self,request:Request) -> Response:
        print(request.path)
        #return self.ROUTETABLE.get(request.path,self.notfound)(request)
        for methods, pattern, handler in self.__routetable:
            if not request.path.startswith(self.prefix):
                return None
            #methods为None时表示支持任意http请求方法
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.prefix,'',1))
                if matcher:
                    #动态属性增加
                    request.args = matcher.group()      #所有分组组成的元组，包括命名的
                    request.kwargs = DictObj(matcher.groupdict())       #命名分组组成的字典
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
    res.server = 'eysdo/Server_v13'
    return res
@py.post(r'/(\w+)') #匹配/python/xxx
def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v13'
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