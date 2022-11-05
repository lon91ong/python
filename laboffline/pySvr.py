#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from sys import argv
from time import sleep
from logging import getLogger
from funApi import single_instance, labDic
from falRes import LabTray, app_root, lab_root

single_instance('oflLab.win_tray', app_root)
logger = getLogger('[log]')
port = argv[1] if len(argv)==2 and argv[1].isdigit() else '9542'
#print('Lab_root:',lab_root,'\napproot',app_root)

def serviceSvr():
    from falRes import FalRes, Serv
    mySvr=Serv(FalRes(),port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()

if len(argv)==2 and argv[1][-3:]=='xml':
    labs = labDic(argv[1])
else:
    labs = labDic(lab_root + '/Download/Updata/Download/download.xml')  

my_tray = LabTray(app_root+'/Artua.ico', labs, port)
my_tray.start()
serviceSvr()
sleep(2)
my_tray.balloons_info(f'服务端成功启动，端口:{port}。\n'+
          '------------------------------\n  ---> 右击下方图标选择实验\n')
while my_tray.running:
    sleep(2)
