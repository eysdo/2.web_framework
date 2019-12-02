class Context(dict):
    def __getattr__(self,item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('Attribute {} Not Found'.format(item))
    def __setattr__(self,key,value):
        self[key] = value

class NestedContext(Context):
    def __init__(self,globalcontext:Context=None):
        super().__init__()
        self.relate(globalcontext)
    def relate(self,globalcontext:Context=None):
        self.globalcontext = globalcontext
    def __getattr__(self,item):
        if item in self.keys():
            return self[item]
        return self.globalcontext[item]

ctx = Context()
ctx.x = 6
ctx.y = 'a'
nc = NestedContext()
nc.relate(ctx)
nc.x = 100
print(nc)
print(nc.x) #自己的x属性
print(nc.y) #全局的y属性
print(nc.z) #KeyError: 'z'