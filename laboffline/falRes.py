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
from sys import exit
from funApi import lab_root as workpth

# falcon类
class FalRes(object):
    def __init__(self, downPort='9562'):
        self.tree = ElementTree()
        self.labroot = self.tree.parse(workpth + '/Download/Updata/Download/download.xml')
        self.dp = downPort
        
    def on_get(self, req, resp, labfile):
        #print('URL:{}\nPath:{}'.format(req.url,req.path))
        requ ='http://aryun.ustcori.com:'+self.dp+quote(req.path,encoding='gb2312')
        print('Get Labfile:',labfile) #, '\nURL:',requ, '\nDownPort:',self.dp)
        resp.downloadable_as=labfile.encode("utf-8").decode("latin1") #编码问题,参见https://github.com/Pylons/waitress/issues/318
        resp.set_headers(dict(list(requests.head(requ).headers.items())[:3])) #'Content-Length', 'Content-Type', 'Last-Modified'
        chunk = lambda u: (yield from requests.get(u,stream=True).iter_content(chunk_size=8192))
        resp.stream = chunk(requ)

    def on_post(self, req, resp):
        resp.content_type = 'text/xml; charset=utf-8'
        #print('Path:', req.path)
        if req.path == '/BizService.svc':
            dataStr = '' # 响应数据
            # 响应文本预制
            respStr = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoServiceResponse xmlns="http://www.ustcori.com/2009/10"><DoServiceResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><Data i:nil="true"/><Message/><RecordCount>0</RecordCount><Status>Success</Status></DoServiceResult></DoServiceResponse></s:Body></s:Envelope>'
            xmls = req.stream.read().decode('utf-8') #req.media
            method = search(r'(?<=<MethodName>).*(?=</MethodName>)',xmls)[0]
            null = None; false = False
            if method == 'FindNewExamRoom':
                labroom = self.tree.parse(workpth + '/Download/download.xml')[0].attrib
                dataStr = '<DataString>{"ROOMID":'+labroom['ID']+',"VERSION":"'+labroom['Version']+'"}</DataString>'
            elif method == 'FindByLABID':
                labid = fromstring(xmls).findall(".//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value")[0].text
                #self.curLab=labid
                try: # online
                    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': 'http://www.ustcori.com/2009/10/IBizService/DoService','Host': 'aryun.ustcori.com:'+self.dp}
                    xmls = fromstring(requests.post('http://aryun.ustcori.com:'+self.dp+req.path,data=xmls,headers=headers).text)
                    #print('Online Mode!')
                    dataStr = '<DataString>{}</DataString>'.format(xmls.findall(".//{http://www.ustcori.com/2009/10}DataString")[0].text)
                except: # offline
                    lab = self.labroot.findall('.//Experiment[@ID='+labid+']')[0].attrib
                    print('实验:',lab['Name'],'分类:',lab['Sort'])
                    dataStr = '<DataString>[{"LabID":'+labid+',"LABNAME":"'+lab['Name']+'","LABTYPEID":null,"LABTYPENAME":"'+lab['Sort']+'","INTRODUTION":"","CONTENT":null,"THEORY":null,"INSTRUMENT":null,"QualifiedTime":null,"LabFileUrl":"'+lab['Name']+'.lab","LabUpTime":null,"SourceFileUrl":null,"SourceUpTime":null,"UpTime":"'+lab['UpTime']+'","UPUSER":null,"LabWeight":null,"ReportWeight":null,"ReportFileUrl":null,"ReportUpTime":null}]</DataString>'
                
            elif method == 'ucControlMethod':
                dataStr = '<DataString>192</DataString>'
            elif method == 'SetLabTimeRecord':
                dataStr = '<DataString>9000</DataString>'
            elif method == 'AddOneToLabFileDownLoadCount':
                dataStr = '<DataString>"1"</DataString>'
            elif method == 'JFIsAccess':
                dataStr = '<DataString>""</DataString>'
            insp = respStr.index('<Message/>') # 定位插入点
            resp.data = bytes(respStr[:insp] + dataStr + respStr[insp:],encoding='utf-8')            
        elif req.path == '/ServiceAPI/SetLabTimeRecordStart':
            resp.data = '7777'.encode('utf-8')
        elif req.path == '/ServiceAPI/UpdateRecord':
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
        print(f"\n服务端启动...端口{self.port}\n")
        try:
            serve(self.app, listen = '127.0.0.1:'+self.port)
        except:
            print(f'错误:网络端口({self.port})可能被占用!')
            exit(0)
