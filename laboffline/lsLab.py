# -*- coding: utf-8 -*-
"""
@Author  : lon91ong (lon91ong@gmail.com)
@Version : 0.9.9
"""
from threading import Thread
from os import system, path
from falRes import workpth, FalRes
import falcon

system('mode con cols=52 lines=120')

# web服务
class QuRes(FalRes):
    def __init__(self):
        self.curLab = ''
        self.labSort = '未分类'
        self.lablist = open('lablist.xml',mode='w+',encoding='utf-8')
        self.lablist.write('<?xml version="1.0" encoding="utf-8"?>\n<root>')
        #self.tree = ElementTree()
        
    def on_get(self, req, resp, labfile):
        #print('URL:{}\nPath:{}'.format(req.url,req.path))
        print('LabID:{},LabName:{}'.format(self.curLab,labfile[:-4]))
        self.lablist.write('  <Experiment Sort="{}" Name="{}" UpTime="2021-11-11T11:11:11" ID="{}" />\n'.format(self.labSort,labfile[:-4],self.curLab))
        self.curLab = labfile[:-4]
        resp.status = falcon.HTTP_400

class Serv(Thread):
    def __init__(self, threadID, mRes, svrp):
        Thread.__init__(self)
        self.threadID = threadID
        self.port = svrp
        self.svrRes = mRes
        self.app = falcon.API()

    def run(self):
        from waitress import serve
        apilst = ['/Upload/lab/{labfile}','/BizService.svc','/ServiceAPI/SetLabTimeRecordStart','/ServiceAPI/UpdateRecord','/FileTransfer.svc']
        for apistr in apilst: self.app.add_route(apistr, self.svrRes)
        print("\n服务端启动...\n")
        try:
            serve(self.app, listen = '127.0.0.1:'+self.port)
        except:
            print('错误:网络端口({})可能被占用!'.format(self.port))
            exit(0)
        
def cleanDir(dir, sname):
    from os import listdir, rmdir, remove
    for dire in listdir(dir):
        dire = path.join(dir,dire)
        if path.isfile(dire):
            if sname in path.basename(dire) or path.basename(dire)[:-4] in sname:
                remove(dire)
                #print('删除文件:'+path.basename(dire))
                if not listdir(path.dirname(dire)):
                    rmdir(path.dirname(dire)) #删除空路径
        else:
            cleanDir(dire,sname) #递归子目录

if __name__ == '__main__':
    from subprocess import Popen
    from time import sleep
    from sys import argv
    from base64 import b64encode
    from itertools import chain
    
    falRes = QuRes()
    chal = chain(range(355,400),range(495,520))
    port = '9650'
    if len(argv)==2:
        port = argv[1] #服务端口
    elif len(argv)==3:
        chal = range(int(argv[1]),int(argv[2]))
    mySvr=Serv(1,falRes,port)
    mySvr.daemon = True #服务线程与主线程共存亡
    mySvr.start()
    exeProg = workpth+r'\Download\Updata\WebLabClient.exe'
    sleep(2)
    if(mySvr.is_alive()):
        print("查询到如下的实验项目:")
        #现有的实验分布在356~396,500~512区间; 本地已有的不显示
        for labId in chal:
        #for labId in range(355,360):
            falRes.curLab = str(labId)
            burl = bytes('/'+str(labId)+'/127.0.0.1/'+port+'/userid/op/1/2',encoding='utf-8')
            href='lab://{}/'.format(b64encode(burl).decode('utf-8'))
            pp = Popen([exeProg, href])
            #print('LabID:',labId)
            sleep(1)
            pp.kill()
            sleep(0.5)
            if not falRes.curLab.isdigit():
                cleanDir(workpth+r'\Download\Updata\Download', falRes.curLab)
        print("\n项目查询完毕!")
    else:
        print("\n服务端启动失败, 查询程序退出!")
    falRes.lablist.write('</root>')
    falRes.lablist.close()
