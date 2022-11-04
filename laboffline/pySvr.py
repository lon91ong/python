#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from sys import argv
from time import sleep
from os import path
from base64 import b64encode
from ctypes import windll
from logging import getLogger
from subprocess import Popen as subOpen
from funApi import app_root, lab_root, single_instance, labDic
from winsystray import SysTrayIcon

single_instance('oflLab.win_tray')
logger = getLogger('[log]')
port = argv[1] if len(argv)==2 and argv[1].isdigit() else '9542'
WebClient_app = lab_root + '/USTCORi.WebLabClient.exe'
#print('Lab_root:',lab_root,'\napproot',app_root)
MessageBox = windll.user32.MessageBoxW

def start_App():
    from falRes import FalRes, Serv
    mySvr=Serv(FalRes(),port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()

def on_quit(systray):
    global running
    running = False

from falRes import downSvr
def balloons_info(systray, infostr = '脱机仿真 v0.9.9\n-----------------\n'+
                f'http://{downSvr["Host"]}:{downSvr["Port"]}'):
    from winsystray.win32_adapter import NIIF_USER, NIIF_NOSOUND
#    about = f'脱机仿真 v0.9.9\n\n文件服务器: http://{downSvr["Host"]}:{downSvr["Port"]}/'
#    MessageBox(None, about, '关于', 0)
    systray.show_balloon(infostr, '提示', NIIF_USER | NIIF_NOSOUND, 5)

def on_right_click(systray):
    build_menu(systray)
    systray._show_menu()
    
def build_menu(systray):
    from winsystray.win32_adapter import MFS_DISABLED
    global last_main_menu, labs
    main_menu = []
    for k in labs.keys():
        main_menu.append((k, 'pass', MFS_DISABLED))
        for j in labs[k]:
            burl = bytes('/'+j['ID']+f'/127.0.0.1/{port}/userid/op/1/2',encoding='utf-8')
            burl = r'lab:\\{}/'.format(b64encode(burl).decode('utf-8'))
            main_menu.append(('   '+j['Lab'], lambda x, arg=burl: subOpen(WebClient_app+' '+arg)))
        main_menu.append((None, '-'))
    main_menu.append((None, '-'))
    main_menu = tuple(main_menu)
    if main_menu != last_main_menu:
        systray.update(menu=main_menu)
        last_main_menu = main_menu
        
last_main_menu = None
if len(argv)==2 and argv[1][-3:]=='xml':
    labs = labDic(argv[1])
else:
    labs = labDic(lab_root + '/Download/Updata/Download/download.xml')  
quit_item = '退出', on_quit
icon_pth = path.join(app_root, 'Artua.ico')
my_tray = SysTrayIcon(icon_pth, '实验服务端', None, quit_item,
                      left_click=balloons_info, right_click=on_right_click)
my_tray.start()
start_App()
sleep(2)
balloons_info(my_tray, f'服务端成功启动，端口:{port}。\n'+
          '------------------------------\n  ---> 右击下方图标选择实验\n')
running = True
while running:
    sleep(2)
