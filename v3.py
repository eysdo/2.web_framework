#!python
#coding: utf-8
from webob import Response, Request, dec
from wsgiref.simple_server import make_server
@dec.wsgify
def app(request:Request) -> Response:
    print(request.path)
    res = Response()
    if request.path == '/':
        res.body = "<h1>eysdo</h1>".encode()
        res.content_type = 'text/html; charset=utf-8'
        res.server = 'eysdo/Server_v3'
    elif request.path == '/python':
        res.body = "<h1>python</h1>".encode()
        res.content_type = 'text/html; charset=utf-8'
        res.server = 'eysdo/Server_v3'
    else:
        res.status_code = 404
        res.body = 'Not Found!'.encode()
        res.content_type = 'text/html; charset=utf-8'
        res.server = 'eysdo/Server_v3'
    return res

def main():
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip,port,app)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()