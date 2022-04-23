# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""
if __name__ == '__main__':
    from sys import argv
    from time import sleep
    from os import popen
    from os.path import basename
    from falRes import FalRes, Serv
    from webbrowser import open as wOpen
    
    svrRes = FalRes()
    port = argv[1] if len(argv)==2 and argv[1].isdigit() else '9542'
    mySvr=Serv(1,svrRes,port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()
    if argv[1][-3:]=='xml':
        wOpen('http://127.0.0.1:{}/Upload/lab/'.format(port)+basename(argv[1]))
    else:
        wOpen('http://127.0.0.1:{}/Upload/lab/0'.format(port))
    sleep(90)
    while(popen('tasklist | findstr "WebLabClient"').read()):
        sleep(60) #每分钟检测一次
