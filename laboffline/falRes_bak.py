# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""
from base64 import b64encode
from re import search
from urllib.parse import quote
import requests, falcon
from xml.etree.ElementTree import ElementTree, fromstring, tostring
from os.path import join, dirname, realpath
from sys import exit, executable
from winreg import OpenKey, QueryValue, CloseKey, HKEY_CLASSES_ROOT

try:
    key = OpenKey(HKEY_CLASSES_ROOT,'Lab\shell\open\command')
    workpth = dirname(QueryValue(key,'').split('"')[1])
    CloseKey(key)
except:
    print('\n未找到注册表项, 请先执行安装!')
    exit(0)
    
# web服务
class FalRes(object):
    def __init__(self):
        self.tree = ElementTree()
        self.labroot = self.tree.parse(workpth + '/Download/Updata/Download/download.xml')
        
    def file_generator(self, url):
        with requests.get(url,stream=True) as r:
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk
    
    def treeHtml(self, labxml=''):
        if labxml: self.labroot = self.tree.parse(labxml)
        self.tree._setroot(fromstring('''
        <!DOCTYPE html>
        <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><title>实验目录</title><style>
        body {font-family: Arial, "Microsoft YaHei"}
        .container {max-width: 320px;margin: 0 auto 20px auto;}
        .section {padding: 0.5em 1em;background-color: #fff;}
        h1,h2 {text-align: center;padding: 0;font-style: bold;}
        h1 {font-size: 32px;color: #2d2e36;margin: 20px 0 5px;border-bottom: 3px solid #999;}
        h2 {font-size: 24px;color: #009688;margin: 15px 0 5px;border-bottom: 1px solid #aaa;background-color: #eee;}
        p {font-size: 20px;text-align: left;margin: 10px 0 10px 1em;}
        a:link {color: #5cb3cc;} 
        a:visited {color: #c02c38;} 
        a:hover {color: #2b73af;text-decoration: underline;}
        a:active {color: gray;}
        a {text-decoration: none;}</style></head>
        <body><div class="container"><h1>实验目录</h1><div class="section"></div></div></body></html>
        '''))
        #userid = 'userid'
        for lab in self.labroot.findall("Experiment"):
            insp = self.tree.find('.//div[@sort="{}"]'.format(lab.attrib['Sort'][0]))
            if insp is None: # 初始化分类
                insp = self.tree.find('.//div[@class="section"]')
                insp.insert(len(insp),fromstring('<div sort="{}"><h2>{}</h2></div>'.format(lab.attrib['Sort'][0],lab.attrib['Sort'])))
                insp = self.tree.find('.//div[@sort="{}"]'.format(lab.attrib['Sort'][0]))
            burl = bytes('/'+lab.attrib['ID']+'/127.0.0.1/9542/userid/op/1/2',encoding='utf-8')
            insp.insert(1,fromstring('<p><a class="reference" href="lab://{}/">{}</a></p>'.format(b64encode(burl).decode('utf-8'),lab.attrib['Name'])))
        return tostring(self.tree.getroot(), encoding='utf-8', method='html')
        
    def on_get(self, req, resp, labfile):
        #print('URL:{}\nPath:{}'.format(req.url,req.path))
        if labfile =='0': # tocfile
            resp.content_type = 'text/html; charset=utf-8'
            resp.data = self.treeHtml()
        elif labfile[-3:] =='xml':
            print(labfile)
            resp.content_type = 'text/html; charset=utf-8'
            resp.data = self.treeHtml(join(dirname(realpath(executable)),labfile))
        else:
            print('Get Labfile:',labfile)
            resp.downloadable_as=labfile.encode("utf-8").decode("latin1") #编码问题,参见https://github.com/Pylons/waitress/issues/318
            r = requests.head('http://aryun.ustcori.com:9542'+quote(req.path,encoding='gb2312'))
            resp.content_length = r.headers['content-length']
            resp.content_type = r.headers['content-type']
            resp.stream = self.file_generator('http://aryun.ustcori.com:9542'+quote(req.path,encoding='gb2312'))

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
                    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': 'http://www.ustcori.com/2009/10/IBizService/DoService','Host': 'aryun.ustcori.com:9542'}
                    xmls = fromstring(requests.post('http://aryun.ustcori.com:9542'+req.path,data=xmls,headers=headers).text)
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