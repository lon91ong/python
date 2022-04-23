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
from falRes import FalRes, Serv
from os import popen

def releasePort(port):
    rut=popen('netstat -aon | findstr {}'.format(port)).read()
    pids = [u.split()[-1] for u in rut.split('\n') if 'LISTENING' in u]
    for pid in pids:
        popen('taskkill -f -pid {}'.format(pid))

if __name__ == '__main__':
    from time import sleep
    #system('mode con cols=42 lines=29')
    svrRes = FalRes()
    port = '9542'
    releasePort(port) #释放端口
    mySvr=Serv(1,svrRes,port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()
    if len(argv)==1: # 直接打开程序的情况
        wOpen("http://127.0.0.1:9542/Upload/lab/0")
    elif argv[1][-3:]=='xml':
        wOpen("http://127.0.0.1:9542/Upload/lab/"+basename(argv[1]))
    sleep(90)
    while(popen('tasklist | findstr "WebLabClient"').read()):
        sleep(60) #每分钟检测一次
