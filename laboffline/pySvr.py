#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from sys import argv
from time import sleep
from funApi import single_instance
from falRes import FalRes, Serv, LabTray, app_root, lab_root

single_instance('oflLab.win_tray', app_root)
port = argv[1] if len(argv)==2 and argv[1].isdigit() else '9542'
#print('Lab_root:',lab_root,'\napproot',app_root)

def labDic(xmlfile):
    from xml.etree.ElementTree import parse
    keys = ('ID','Lab')
    labs={} #返回字典
    for lab in parse(xmlfile).findall("Experiment"):
        k = lab.attrib['Sort']
        if k not in labs.keys():
            labs[k]=[]
        labs[k].append(dict(zip(keys,(lab.attrib['ID'], lab.attrib['Name']))))
    return labs

if len(argv)==2 and argv[1][-3:]=='xml':
    labs = labDic(argv[1])
else:
    labs = labDic(lab_root + '/Download/Updata/Download/download.xml')  
mySvr=Serv(FalRes(),port) #服务端初始化
mySvr.daemon = True #服务线程与主线程共存亡
mySvr.start()
my_tray = LabTray(app_root+'/Artua.ico', labs, port)
my_tray.start() #启动任务栏图标
sleep(1)
my_tray.balloons_info(f'服务端成功启动，端口:{port}。\n'+
          '------------------------------\n  ---> 右击下方图标选择实验\n')
while my_tray.running:  
    sleep(2)
