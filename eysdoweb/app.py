from wsgiref.simple_server import make_server
from eysdoweb import EWeb,Context,jsonify
idx = EWeb.Router()
py = EWeb.Router('/python')
EWeb.register(idx)
EWeb.register(py)

@idx.get(r'^/$') #只匹配根/
def index(request:EWeb.Request):
    res = EWeb.Response()
    res.body = "<h1>eysdo</h1>".encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v17'
    return res
@py.post(r'/{name}/{id}') #匹配/python/xxx/123
def showpython(request:EWeb.Request):
    res = EWeb.Response()
    res.body = "<h1>python</h1> {}".format(request.vars.id).encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v17'
    return res

#拦截器demo
@EWeb.reg_preinterceptor     #全局拦截器
def showheaders(ctx:Context,request:EWeb.Request) -> EWeb.Request:
    print(request.path)
    print(request.user_agent)
    return request
@py.reg_preinterceptor          #router实例拦截器
def showprefix(ctx:Context,request:EWeb.Request) -> EWeb.Request:
    print('~~~prefix = {}'.format(ctx.router.prefix))
    return request
@py.reg_postinterceptor
def showjson(ctx:Context,request:EWeb.Request,response:EWeb.Response) -> EWeb.Response:
    body = response.body.decode()
    return jsonify(body=body)
def main():
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip,port,EWeb())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

if __name__ == '__main__':
    main()