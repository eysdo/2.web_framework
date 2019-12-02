#!python
#coding: utf-8
#支持json格式返回
from json import dumps
from .web import EWeb
def jsonify(**kwargs):
    content = dumps(kwargs)
    response = EWeb.Response()
    response.content_type = "application/json"
    response.charset = 'utf-8'
    response.body = "{}".format(content).encode()
    return response