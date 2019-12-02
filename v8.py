#!python
#coding: utf-8
'''装饰器实现路由注册'''
from webob import Response, Request, dec, exc
from wsgiref.simple_server import make_server
class Application:
    #路由表
    ROUTETABLE = {}
    @classmethod
    def register(cls,path):
        def wrapper(handler):
            cls.ROUTETABLE[path] = handler
            return handler
        return wrapper
    @dec.wsgify
    def __call__(self,request:Request) -> Response:
        print(request.path)
        #return self.ROUTETABLE.get(request.path,self.notfound)(request)
        try:
            return self.ROUTETABLE[request.path](request)
        except:
            raise exc.HTTPNotFound("您访问的网页被外星人劫持了")

@Application.register('/') #index = Application.register('/')(index)
def index(request:Request):
    res = Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v8'
    return res

@Application.register('/python')
def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v8'
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