#!python
#coding: utf-8
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
d = {'a':1,'b':2}

do = DictObj(d)
print(do.a)
do.a = 3