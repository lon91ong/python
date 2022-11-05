#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from sys import argv
from time import sleep
from os import path
from base64 import b64encode
from logging import getLogger
from subprocess import Popen as subOpen
from funApi import app_root, lab_root, single_instance, labDic
from winsystray import SysTrayIcon
from winsystray.win32_adapter import NIIF_USER, NIIF_NOSOUND

single_instance('oflLab.win_tray')
logger = getLogger('[log]')
port = argv[1] if len(argv)==2 and argv[1].isdigit() else '9542'
WebClient_app = lab_root + '/USTCORi.WebLabClient.exe'
#print('Lab_root:',lab_root,'\napproot',app_root)

def serviceSvr():
    from falRes import FalRes, Serv
    mySvr=Serv(FalRes(),port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()

class LabTray(SysTrayIcon):
    def __init__(self, icon, labs):
        super().__init__(icon,'实验服务端',None, ('退出', self.on_quit),
                    left_click=self.on_left_click, right_click=self.on_right_click)
        self.labs = labs
        self.running = True
        self.last_main_menu = None
    
    def on_quit(self, systray):
        self.running = False

    def balloons_info(self, infostr = ''):
        # from ctypes import windll
        # MessageBox = windll.user32.MessageBoxW
        # about = f'脱机仿真 v0.9.9\n\n文件服务器: http://{downSvr["Host"]}:{downSvr["Port"]}/'
        # MessageBox(None, about, '关于', 0)
        self.show_balloon(infostr, '提示', NIIF_USER | NIIF_NOSOUND, 5)
        
    def on_left_click(self, systray):
        from falRes import downSvr
        self.show_balloon('脱机仿真 v0.9.9\n-----------------\n'+
                    f'http://{downSvr["Host"]}:{downSvr["Port"]}', 
                    '提示', NIIF_USER | NIIF_NOSOUND, 5)
        
    def on_right_click(self, systray):
        self.build_menu()
        self._show_menu()
        
    def build_menu(self):
        from winsystray.win32_adapter import MFS_DISABLED
        main_menu = []
        for k in self.labs.keys():
            main_menu.append((k, 'pass', MFS_DISABLED))
            for j in self.labs[k]:
                burl = bytes('/'+j['ID']+f'/127.0.0.1/{port}/userid/op/1/2',encoding='utf-8')
                burl = r'lab:\\{}/'.format(b64encode(burl).decode('utf-8'))
                main_menu.append(('   '+j['Lab'], lambda x, arg=burl: subOpen(WebClient_app+' '+arg)))
            main_menu.append((None, '-'))
        main_menu.append((None, '-'))
        main_menu = tuple(main_menu)
        if main_menu != self.last_main_menu:
            self.update(menu=main_menu)
            self.last_main_menu = main_menu

if len(argv)==2 and argv[1][-3:]=='xml':
    labs = labDic(argv[1])
else:
    labs = labDic(lab_root + '/Download/Updata/Download/download.xml')  

my_tray = LabTray(path.join(app_root, 'Artua.ico'), labs)
my_tray.start()
serviceSvr()
sleep(2)
my_tray.balloons_info(f'服务端成功启动，端口:{port}。\n'+
          '------------------------------\n  ---> 右击下方图标选择实验\n')
while my_tray.running:
    sleep(2)
