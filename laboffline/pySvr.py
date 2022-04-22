# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""
import falcon
from waitress import serve
#from os import system
from sys import argv
from os.path import basename
from webbrowser import open as wOpen
from falRes import FalRes

def releasePort(port):
    from os import popen
    rut=popen('netstat -aon | findstr {}'.format(port)).read()
    try:
        pids = [u[-10:].lstrip() for u in rut.split('\n') if 'LISTENING' in u]
        for pid in pids:
            popen('taskkill -f -pid {}'.format(pid))
    except:
        pass

if __name__ == '__main__':
    #system('mode con cols=42 lines=29')
    svrRes = FalRes()
    app = falcon.API()
    apilst = ['/Upload/lab/{labfile}','/BizService.svc','/ServiceAPI/SetLabTimeRecordStart','/ServiceAPI/UpdateRecord','/FileTransfer.svc']
    for apistr in apilst: app.add_route(apistr, svrRes)
    print("\n运行中...\n")
    if len(argv)==1: # 直接打开程序的情况
        wOpen("http://127.0.0.1:9542/Upload/lab/0")
    elif argv[1][-3:]=='xml':
        wOpen("http://127.0.0.1:9542/Upload/lab/"+basename(argv[1]))
    releasePort('9542') #释放端口
    serve(app, listen = '127.0.0.1:9542')
