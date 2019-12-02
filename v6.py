#!python
#coding: utf-8
'''使用类封装'''
from webob import Response, Request, dec
from wsgiref.simple_server import make_server
class Application:
    def notfound(self,request:Request):
        res = Response()
        res.status_code = 404
        res.body = 'Not Found!'.encode()
        res.content_type = 'text/html; charset=utf-8'
        res.server = 'eysdo/Server_v6'
        return res
    #路由表
    ROUTETABLE = {}
    @classmethod
    def register(cls,path,handler):
        cls.ROUTETABLE[path] = handler
    @dec.wsgify
    def __call__(self,request:Request) -> Response:
        print(request.path)
        return self.ROUTETABLE.get(request.path,self.notfound)(request)


def index(request:Request):
    res = Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v6'
    return res

def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v6'
    return res

#注册
Application.register('/',index)
Application.register('/python',showpython)



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