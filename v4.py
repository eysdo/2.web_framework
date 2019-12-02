#!python
#coding: utf-8
from webob import Response, Request, dec
from wsgiref.simple_server import make_server

def index(request:Request):
    res = Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v4'
    return res

def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v4'
    return res

def notfound(request:Request):
    res = Response()
    res.status_code = 404
    res.body = 'Not Found!'.encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v4'
    return res

ROUTETABLE = {
    '/':index,
    '/python':showpython
}

@dec.wsgify
def app(request:Request) -> Response:
    print(request.path)
    return ROUTETABLE.get(request.path,notfound)(request)

def main():
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip,port,app)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()