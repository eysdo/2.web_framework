#!python
#coding: utf-8
from webob import Response, Request
from wsgiref.simple_server import make_server, demo_app
def appication(environ:dict,start_response):
    request = Request(environ)
    print(request.method)
    print(request.path)
    print(request.GET)
    print(request.POST)
    print(request.params)
    print(request.query_string)
    res = Response("<h1>eysdo</h1>")
    return res(environ,start_response) #__call__

def main():
    ip = '127.0.0.1'
    port = 9998
    server = make_server(ip,port,appication)
    server.serve_forever()
    server.server_close()

if __name__ == '__main__':
    main()
