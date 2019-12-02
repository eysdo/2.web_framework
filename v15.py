#!python
#coding: utf-8
'''功能增强：拦截器interceptor，请求拦截和响应拦截'''
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

class Context(dict):    #app使用
    def __getattr__(self,item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format(item))
    def __setattr__(self,key,value):
        self[key] = value

class NestedContext(Context):   #router使用
    def __init__(self,globalcontext:Context=None):
        super().__init__()
        self.relate(globalcontext)
    def relate(self,globalcontext:Context=None):
        self.globalcontext = globalcontext
    def __getattr__(self,item):
        if item in self.keys():
            return self[item]
        return self.globalcontext[item]

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
        self.ctx = NestedContext()  #未绑定时的全局上下文
        self.preinterceptor = []
        self.postinterceptor = []
    def reg_preinterceptor(self,fn):
        self.preinterceptor.append(fn)
        return fn
    def reg_postinterceptor(self,fn):
        self.postinterceptor.append(fn)
        return fn
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
        for fn in self.preinterceptor:
            request = fn(self.ctx,request)
        for methods, pattern, translator, handler in self.__routetable:
            #methods为None时表示支持任意http请求方法
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.prefix,'',1))
                if matcher:
                    newdict = {}
                    for k, v in matcher.groupdict().items():
                        newdict[k] = translator[k](v)
                    request.vars = DictObj(newdict) #request.vars.id    request.vars.name
                    response = handler(self.ctx,request)
                    for fn in self.postinterceptor:
                        response = fn(self.ctx,request,response)
                    return response


class Application:
    ctx = Context() #全局上下文对象
    def __init__(self,**kwargs):
        self.ctx.app = self
        for k, v in kwargs:
            self.ctx[k] = v
    #前缀开头的所有router对象
    ROUTERS = []

    #拦截器
    PREINTERCEPTOR = []
    POSTINTERCEPTOR = []
    @classmethod
    def reg_preinterceptor(cls,fn):
        cls.PREINTERCEPTOR.append(fn)
        return fn
    @classmethod
    def reg_postinterceptor(cls,fn):
        cls.POSTINTERCEPTOR.append(fn)
        return fn
    @classmethod
    def register(cls,router:Router):
        router.ctx.relate(cls.ctx)
        router.ctx.router = router
        cls.ROUTERS.append(router)
        return router

    @dec.wsgify
    def __call__(self,request:Request) -> Response:
        for fn in self.PREINTERCEPTOR:
            request = fn(self.ctx,request)
        for router in self.ROUTERS:
            response = router.match(request)
            if response:
                for fn in self.POSTINTERCEPTOR:
                    response = fn(self.ctx,request,response)
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
    res.server = 'eysdo/Server_v15'
    return res
@py.post(r'/{name}/{id}') #匹配/python/xxx/123
def showpython(request:Request):
    res = Response()
    res.body = "<h1>python</h1> {}".format(request.vars.id).encode()
    res.content_type = 'text/html; charset=utf-8'
    res.server = 'eysdo/Server_v15'
    return res

#拦截器demo
@Application.reg_preinterceptor     #全局拦截器
def showheaders(ctx:Context,request:Request) -> Request:
    print(request.path)
    print(request.user_agent)
    return request
@py.reg_preinterceptor          #router实例拦截器
def showprefix(ctx:Context,request:Request) -> Request:
    print('~~~prefix = {}'.format(ctx.router.prefix))
    return request

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