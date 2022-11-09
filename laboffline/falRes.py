# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""

from re import search
from urllib.parse import quote
import requests, falcon
from threading import Thread
from xml.etree.ElementTree import ElementTree, fromstring
from sys import exc_info, exit
from os import path, _exit
from winreg import OpenKey, QueryValue, CloseKey, HKEY_CLASSES_ROOT
from json import load
from ctypes import windll
from random import randint, seed
from time import process_time

MessageBox = windll.user32.MessageBoxW
try:
    with open('config.json','r') as json_f:
        loc_user, downSvr = tuple(load(json_f).values())
        #downSvr = load(json_f)["FileSever"]
except:
    info_str = '配置文件(config.json)加载失败，请检查！'
    print("Unexpected error:", exc_info()[0:2])
    # MB_ICONSTOP = MB_ICONERROR = 0x10; MB_ICONWARNING = 0x30; MB_ICONINFORMATION = 0x40
    # MB_OK = 0; MB_OKCANCEL = 1; MB_YESNOCANCEL = 3
    MessageBox(None, info_str, '错误', 0x10 | 0)
    _exit(-1)

app_root = path.dirname(path.realpath(__file__)) # onefile不适用

try:
    key = OpenKey(HKEY_CLASSES_ROOT,'Lab\shell\open\command')
    lab_root = path.dirname(QueryValue(key,'').split('"')[1])
    CloseKey(key)
except:
    if path.isfile(path.join(app_root,r'USTCORi.WebLabClient.exe')):
        lab_root = app_root
    elif path.isfile(path.join(app_root,'..\\USTCORi.WebLabClient.exe')):
        lab_root = path.dirname(app_root)
    else:
        MessageBox(None, '仿真环境未安装!', '错误', 0x10 | 0)
        print('仿真环境未安装!')
        _exit(-1)
    pass
#print(f'LabRoot:{lab_root}\nAppRoot:{app_root}')

# falcon类
class FalRes(object):
    def __init__(self):
        self.tree = ElementTree()
        self.labroot = self.tree.parse(app_root + '/lablist.xml')
        self.port = downSvr["Port"]
        self.fileSvr = downSvr["Host"]
        self.seedLock = 0
        
    def on_get(self, req, resp, labfile):
        #print('URL:{}\nPath:{}'.format(req.url,req.path))
        requ =f'http://{self.fileSvr}:{self.port}'+quote(req.path,encoding='gb2312')
        print('\nGet Labfile:',labfile, end='')
        resp.downloadable_as=labfile.encode("utf-8").decode("latin1") #编码问题,参见https://github.com/Pylons/waitress/issues/318
        resp.set_headers(dict(list(requests.head(requ).headers.items())[:3])) #'Content-Length', 'Content-Type', 'Last-Modified'
        chunk = lambda u: (yield from requests.get(u,stream=True).iter_content(chunk_size=8192))          
        resp.stream = chunk(requ)

    def on_post(self, req, resp):
        resp.content_type = 'text/xml; charset=utf-8'
        print(f'\nPath:{req.path}', end='') # 输出末尾不换行
        if req.path == '/BizService.svc':
            dataStr = '' # 响应数据
            # 响应文本预制
            respStr = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoServiceResponse xmlns="http://www.ustcori.com/2009/10"><DoServiceResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><Data i:nil="true"/><Message/><RecordCount>0</RecordCount><Status>Success</Status></DoServiceResult></DoServiceResponse></s:Body></s:Envelope>'
            xmls = req.stream.read().decode('utf-8') #req.media
            #print("ReqTextInXML:", xmls)
            method = search(r'(?<=<MethodName>).*(?=</MethodName>)',xmls)[0]
            #null = None; false = False
            if method == 'FindNewExamRoom':
                self.seedLock = int(process_time()*100) #for seed lock
                labroom = self.tree.parse(lab_root + '/Download/download.xml')[0].attrib
                dataStr = '<DataString>{"ROOMID":'+labroom['ID']+',"VERSION":"'+labroom['Version']+'"}</DataString>'
            elif method == 'FindByLABID':
                labid = fromstring(xmls).findall(".//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value")[0].text[1:-1]
                lab = self.labroot.findall('.//Experiment[@ID="'+labid+'"]')[0].attrib
                print('实验:',lab['Name'],'分类:',lab['Sort'])
                dataStr = '<DataString>[{' + f'"LabID":{labid},"LABNAME":"{lab["Name"]}","LABTYPEID":null,"LABTYPENAME":"{lab["Sort"]}","INTRODUTION":"","CONTENT":null,"THEORY":null,"INSTRUMENT":null,"QualifiedTime":null,"LabFileUrl":"{lab["LabFile"]}","LabUpTime":null,"SourceFileUrl":null,"SourceUpTime":null,"UpTime":"{lab["UpTime"]}","UPUSER":{loc_user["ID"]},"LabWeight":null,"ReportWeight":null,"ReportFileUrl":null,"ReportUpTime":null'+'}]</DataString>'
            elif method == 'ucControlMethod':
                seed(self.seedLock) # 随机种子, 同一会话期间保持不变
                dataStr = f'<DataString>{randint(160, 260)}</DataString>'
            elif method == 'SetLabTimeRecord':
                dataStr = f'<DataString>{str(self.seedLock +6000)}</DataString>'
            elif method == 'AddOneToLabFileDownLoadCount':
                dataStr = '<DataString>"1"</DataString>'
            elif method == 'JFIsAccess': #计费与否
                dataStr = '<DataString>""</DataString>'
            print(f', Method:{method}, Seed:{self.seedLock}', end='')  #, Data:{dataStr[12:-13]}')
            insp = respStr.index('<Message/>') # 定位插入点
            resp.data = bytes(respStr[:insp] + dataStr + respStr[insp:],encoding='utf-8')            
        elif req.path == '/ServiceAPI/SetLabTimeRecordStart':
            resp.data = str(self.seedLock +6000).encode('utf-8')
        elif req.path == '/ServiceAPI/UpdateRecord':
            xml_text = req.stream.read().decode('utf-8') # 加密后的实验操作数据
            #print(f" FileName:{xml_text[xml_text.index('FileName=')+9:xml_text.index('.xml&')+4]}", end='')
            print(', ' + xml_text.split('&',5)[-2], end='')
            resp.data = '1'.encode('utf-8')
        else:   # /FileTransfer.svc
            resp.data = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><UploadFileResponse xmlns="http://tempuri.org/"/></s:Body></s:Envelope>'.encode('utf-8')
        resp.status = falcon.HTTP_200
        
class Serv(Thread):
    def __init__(self, mRes, svrp):
        Thread.__init__(self)
        self.port = svrp
        self.svrRes = mRes
        self.app = falcon.App()

    def run(self):
        from waitress import serve
        apilst = ['/Upload/lab/{labfile}','/BizService.svc','/ServiceAPI/SetLabTimeRecordStart','/ServiceAPI/UpdateRecord','/FileTransfer.svc']
        for apistr in apilst: self.app.add_route(apistr, self.svrRes)
        print(f"\n服务端启动...端口:{self.port}")
        try:
            serve(self.app, listen = '127.0.0.1:'+self.port)
        except:
            print(f'错误:网络端口({self.port})可能被占用!')
            exit(0)

from winsystray import SysTrayIcon
from winsystray.win32_adapter import NIIF_USER, NIIF_NOSOUND
class LabTray(SysTrayIcon):
    def __init__(self, icon, labs, port):
        super().__init__(icon,'实验服务端',None, ('退出', self.on_quit),
                    left_click=self.on_left_click, right_click=self.on_right_click)
        self.labs, self.port = labs, port
        self.running = True
        self.last_main_menu = None
        self.WebClient_app = lab_root + '/USTCORi.WebLabClient.exe'
    
    def on_quit(*self):
        self[0].running = False

    def balloons_info(self, infostr = ''):
        self.show_balloon(infostr, '提示', NIIF_USER | NIIF_NOSOUND, 5)
        
    def on_left_click(*self):
        from falRes import downSvr
        self[0].show_balloon('脱机仿真 v0.9.9\n-----------------\n'+
                    f'http://{downSvr["Host"]}:{downSvr["Port"]}', 
                    '提示', NIIF_USER | NIIF_NOSOUND, 5)
        
    def on_right_click(*self):
        self[0].build_menu()
        self[0]._show_menu()
        
    def build_menu(self):
        from base64 import b64encode
        from subprocess import Popen as subOpen
        from winsystray.win32_adapter import MFS_DISABLED
        main_menu = []
        for k in self.labs.keys():
            main_menu.append((k, 'pass', MFS_DISABLED))
            for j in self.labs[k]:
                burl = bytes('/'+j['ID']+f'/127.0.0.1/{self.port}/{loc_user["ID"]}/op/1/0',encoding='utf-8')
                burl = r'lab:\\{}/'.format(b64encode(burl).decode('utf-8'))
                # 迈克尔逊 lab://LzM2Mi8xMjcuMC4wLjEvOTU0Mi8yMDIxMTU1MzEwMDEvb3AvMS8y/
                main_menu.append(('   '+j['Lab'], lambda x, arg=burl: subOpen(self.WebClient_app+' '+arg)))
            main_menu.append((None, '-'))
        main_menu.append((None, '-'))
        main_menu = tuple(main_menu)
        if main_menu != self.last_main_menu:
            self.update(menu=main_menu)
            self.last_main_menu = main_menu
