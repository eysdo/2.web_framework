#!python
#coding: utf-8
'''发布'''
from distutils.core import setup
#导入setup函数并传参
setup(
    name = 'EWeb',  #名字
    version = 'v1.0',    #版本
    description = 'Python WSGI WEB Framework',  #描述信息
    author = 'eysdo',   #作者
    author_email='308418897@qq.com',    #作者邮箱地址
    url = 'https://github.com/eysdo',   #包的主页，可以不写
    packages=['eysdoweb']   #打包列表，指定eysdoweb就会把eysdoweb所有的非目录子模块打包
    #packages = ['m','m.m1','m.m2','m.m2.m21']
)

#打包及安装命令
'''
    把setup.py文件放置在eysdoweb同级目录
    python setup.py sdist   #打包
    running sdist
    running check
    warning: sdist: manifest template 'MANIFEST.in' does not exist (using default file list)

    warning: sdist: standard file not found: should have one of README, README.txt, README.rst

    warning: sdist: standard file 'setup.py' not found

    writing manifest file 'MANIFEST'
    creating EWeb-v1.0
    creating EWeb-v1.0\eysdoweb
    making hard links in EWeb-v1.0...
    hard linking eysdoweb\__init__.py -> EWeb-v1.0\eysdoweb
    hard linking eysdoweb\app.py -> EWeb-v1.0\eysdoweb
    hard linking eysdoweb\setup.py -> EWeb-v1.0\eysdoweb
    hard linking eysdoweb\web.py -> EWeb-v1.0\eysdoweb
    creating dist
    Creating tar archive
    removing 'EWeb-v1.0' (and everything under it)
    pip install .\dist\EWeb-v1.0.tar.gz    #安装到D:\ProgramData\Anaconda3\Lib\site-packages\eysdoweb
    Building wheels for collected packages: EWeb
    Building wheel for EWeb (setup.py) ... done
    Stored in directory: C:\Users\eysdo\AppData\Local\pip\Cache\wheels\51\5a\89\cb2de63db7677f30a01d7ff4ee58b3a7e476b9a0b79bed8413
    Successfully built EWeb
    Installing collected packages: EWeb
    Successfully installed EWeb-1.0
'''
