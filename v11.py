#!python
#coding: utf-8
'''支持正则表达式分组捕获'''
from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server
from re import compile
class Application:
    GET = 'GET'
    POST = "POST"
    HEAD = 'HEAD'
    PUT = 'PUT'
    #路由表
    #/python/tv/123 -> /python/(\w+)/(\d+)
    ROUTETABLE = []
    @classmethod
    def route(cls,pattern,*methods):
        def wrapper(handler):
            cls.ROUTETABLE.append((methods,compile(pattern), handler))
            return handler
        return wrapper
    @classmethod
    def get(cls,pattern):
        return cls.route(pattern,'GET','POST')
    @classmethod
    def post(cls,pattern):
        return cls.route(pattern,'POST')
    @dec.wsgify
    def __call__(self,request:Request) -> Response:
        print(request.path)
        #return self.ROUTETABLE.get(request.path,self.notfound)(request)
        for methods, pattern, handler in self.ROUTETABLE:
            #methods为None时表示支持任意http请求方法
            if not methods or request.method.upper() in methods:
                    matcher = pattern.match(request.path)
                    if matcher:
                        #动态属性增加
                        request.args = matcher.group()      #所有分组组成的元组，包括命名的
                        request.kwargs = matcher.groupdict()        #命名分组组成的字典
                        return handler(request)
        raise exc.HTTPNotFound("您访问的网页被外星人劫持了")

@Application.get('^/$') #index = Application.get('^/$')(index)
def index(request:Request):
    res = Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v11'
    return res

@Application.post('/python')
def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v11'
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