# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
参数说明: 三种情况 [[port], [start, end], [port, start, end]]
"""
from os import system
from falRes import downSvr
import requests
from xml.etree.ElementTree import fromstring
from json import loads

system('mode con cols=52 lines=120')

if __name__ == '__main__':
    from time import sleep
    from sys import argv
    from itertools import chain
    
    lablist = open('lablist.xml',mode='w+',encoding='utf-8')
    lablist.write('<?xml version="1.0" encoding="utf-8"?>\n<root>')    
    #现有的实验分布在356~396,500~512区间;
    chal = range(int(argv[-2]),int(argv[-1])) if len(argv)>2 else chain(range(355,400),range(500,520))
    headers = {'Content-Type': 'text/xml; charset=utf-8','SOAPAction': 'http://www.ustcori.com/2009/10/IBizService/DoService','Host': f'{downSvr["Host"]}:{downSvr["Port"]}'}
    #在线查询
    print("在线查询到如下的实验项目:")
    for labId in chal:
        xmls = f'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoService xmlns="http://www.ustcori.com/2009/10"><request xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><BizCode>UstcOri.BLL.BLLLabClent</BizCode><EnableCache>false</EnableCache><MethodName>FindByLABID</MethodName><Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:KeyValueOfstringanyType><a:Key>LabID</a:Key><a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">"{labId}"</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>'
        xmls = requests.post(f'http://{downSvr["Host"]}:{downSvr["Port"]}/BizService.svc',data=xmls,headers=headers).text
        if len(xmls) > 390:
            labDic = loads(fromstring(xmls).findall(".//{http://www.ustcori.com/2009/10}DataString")[0].text[1:-1])
            lablist.write(f'  <Experiment Sort="{labDic["LABTYPENAME"]}" Name="{labDic["LABNAME"]}" UpTime="{labDic["UpTime"]}" ID="{labId}" LabFile="{labDic["LabFileUrl"]}" />\n')
            print(f'LabID:{labId},LabName:{labDic["LABNAME"]}')
        else:
            sleep(0.7)
            continue
    print("\n项目查询完毕!")
    #print("\n服务端启动失败, 查询程序退出!")
    lablist.write('</root>')
    lablist.close()
    sleep(5)
