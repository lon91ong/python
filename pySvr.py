# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""
import falcon, sys

from waitress import serve
#from wsgiref import simple_server
from xml.etree.ElementTree import ElementTree, fromstring
from os import path, system, startfile
from base64 import b64encode
from re import search
from urllib.parse import quote
import requests

system('mode con cols=42 lines=29')
workpth = path.dirname(path.realpath(__file__)) #if getattr(sys, 'frozen', False) else 'D:\\Program Files\\仿真实验'
tree = ElementTree()
labroot = tree.parse(workpth + '/../Download/Updata/Download/download.xml')
tree._setroot(fromstring('''
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
userid = 'userid'
for lab in labroot.findall("Experiment"):
    insp = tree.find('.//div[@sort="{}"]'.format(lab.attrib['Sort'][0]))
    if insp is None: # 初始化分类
        insp = tree.find('.//div[@class="section"]')
        insp.insert(len(insp),fromstring('<div sort="{}"><h2>{}</h2></div>'.format(lab.attrib['Sort'][0],lab.attrib['Sort'])))
        insp = tree.find('.//div[@sort="{}"]'.format(lab.attrib['Sort'][0]))
    burl = bytes('/'+lab.attrib['ID']+'/127.0.0.1/9542/'+userid+'/op/1/2',encoding='utf-8')
    insp.insert(1,fromstring('<p><a class="reference" href="lab://{}/">{}</a></p>'.format(b64encode(burl).decode('utf-8'),lab.attrib['Name'])))
    
tocfile = workpth+'/../实验目录.html' #sys._MEIPASS+'/实验目录.html' if getattr(sys, 'frozen', False) else 
tree.write(tocfile,encoding='utf-8',method='html')
startfile(tocfile)

# web服务
class Resource(object):
    def file_generator(self, url):
        with requests.get(url,stream=True) as r:
            #print("Headers0['Content-Length']:",r.headers['Content-Length'])
            for chunk in r.iter_content(chunk_size=8192):
                yield chunk
        
    def on_get(self, req, resp, labfile):
        #print('URL:{}\nPath:{}'.format(req.url,req.path))
        print('Get Labfile:',labfile)
        resp.downloadable_as=labfile.encode("utf-8").decode("latin1") #编码问题,参见https://github.com/Pylons/waitress/issues/318
        r = requests.head('http://aryun.ustcori.com:9542'+quote(req.path,encoding='gb2312'))
        resp.content_length = r.headers['content-length']
        resp.content_type = r.headers['content-type']
        resp.stream = self.file_generator('http://aryun.ustcori.com:9542'+quote(req.path,encoding='gb2312'))

    def on_post(self, req, resp):
        resp.content_type = 'text/xml; charset=utf-8'
        print('Path:', req.path)
        if req.path == '/BizService.svc':
            dataStr = '' # 响应数据
            # 响应文本预制
            respStr = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoServiceResponse xmlns="http://www.ustcori.com/2009/10"><DoServiceResult xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><Data i:nil="true"/><Message/><RecordCount>0</RecordCount><Status>Success</Status></DoServiceResult></DoServiceResponse></s:Body></s:Envelope>'
            xmls = req.stream.read().decode('utf-8') #req.media
            method = search(r'(?<=<MethodName>).*(?=</MethodName>)',xmls)[0]
            null = None; false = False
            if method == 'FindNewExamRoom':
                labroom = tree.parse(workpth + '/../Download/download.xml')[0].attrib
                dataStr = '<DataString>{"ROOMID":'+labroom['ID']+',"VERSION":"'+labroom['Version']+'"}</DataString>'
            elif method == 'FindByLABID':
                try: # online
                    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': 'http://www.ustcori.com/2009/10/IBizService/DoService','Host': 'aryun.ustcori.com:9542'}
                    xmls = fromstring(requests.post('http://aryun.ustcori.com:9542'+req.path,data=xmls,headers=headers).text)
                    #labid = eval(xmls.findall(".//{http://www.ustcori.com/2009/10}DataString")[0].text)[0]['LabID']
                    print('Online Mode!')
                    dataStr = '<DataString>{}</DataString>'.format(xmls.findall(".//{http://www.ustcori.com/2009/10}DataString")[0].text)
                except: # offline
                    labid = fromstring(xmls).findall(".//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value")[0].text
                    #print('LABID:',labid,type(labid))
                    lab = labroot.findall('.//Experiment[@ID='+labid+']')[0].attrib
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
        
        
if __name__ == '__main__':
    svrRes = Resource()
    app = falcon.API()
    apilst = ['/Upload/lab/{labfile}','/BizService.svc','/ServiceAPI/SetLabTimeRecordStart','/ServiceAPI/UpdateRecord','/FileTransfer.svc']
    for apistr in apilst: app.add_route(apistr, svrRes)
    print("\n运行中...\n")
    serve(app, listen = '127.0.0.1:9542')

