#!python
#coding: utf-8
from webob import Response, Request, dec
from wsgiref.simple_server import make_server
@dec.wsgify
def app(request:Request) -> Response:
    print(request.method)
    print(request.path)
    print(request.GET)
    print(request.POST)
    print(request.params)
    print(request.query_string)
    return Response("<h1>eysdo</h1>")

def main():
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip,port,app)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()