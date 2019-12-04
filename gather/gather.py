# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019
抓取教务网站学生花名册
@author: xiaoniu29
"""

import sys, re
from sqlite3 import connect
from os import path
from time import localtime
from xlwt import Workbook
from requests import get as browser
from requests.exceptions import RequestException
from urllib.parse import quote

from myMod import mbox, GetDesktopPath, getFile
from getClasses import getClassName

def main(argv):
    exedir = path.dirname(path.abspath(sys.argv[0])) # 程序所在目录
    if len(sys.argv) < 2: #直接运行程序
        docpth = getFile(exedir,'打开课程表(仅支持docx格式)',"Word 10文档 (*.docx)|*.docx||")
        if docpth == '':
            mbox( '错误','需要指定课程表文件!', 'error')
            sys.exit(0)
    else:
        docpth = path.abspath(sys.argv[-1])
    grade, classes = getClassName(docpth) #取年级、班级列表
    #print(classes)
    if localtime().tm_mon < 8: # 春季学期
        conn = connect(exedir+'/hwmy'+grade+'_spring.db') #参数路径
    else: # 秋季学期
        conn = connect(exedir+'/hwmy'+grade+'_autumn.db')
    #mbox('info',path.dirname(path.realpath(sys.argv[0])),'info')
    #conn = connect(':memory:') #内存临时
    curs = conn.cursor()
    conn.text_factory = str #lambda x: str(x, "gbk", "ignore")
    curs.execute('create table if not exists students (id varchar(12) primary key, name varchar(12) not NULL collate nocase, class text collate nocase, score unsigned tinyint, unique (id))')
    curs.execute('create table if not exists classes (id INTEGER PRIMARY KEY AUTOINCREMENT, class text not NULL collate nocase, unique (class))')
    #花名电子表
    wb = Workbook(encoding="utf-8")
    worksheet = wb.add_sheet("花名", cell_overwrite_ok=True)
    worksheet.write(0, 0,'班级')
    curs.executemany('Insert Or Replace into classes (class) values (?)',[(cla,) for cla in classes])
    students = []
    n = 0
    for i in range(len(classes)):
        worksheet.write(i+1,0,classes[i])
        #curs.execute('Insert Or Replace into classes (class) values ("{}")'.format(classes[i]))
        try:
            req = browser('http://211.81.249.110/hmc/hmc_p.asp?trbj='+quote(classes[i],encoding='gb2312'),verify=False,timeout=(0.5,3))
        except RequestException as err:
            #print("Error class:",sys.exc_info()[0])
            mbox('错误','网络连接错误:{0}\n错误类型:{1}\n请查验后重试!'.format(err,type(err)),'error')
            sys.exit(0)
        #content = req.content.decode('gbk', 'ignore') # 忽略非法字符，replace则用?取代非法字符；
        #res = re.findall(r'\d{12}(?=</td>)', content) # 所有的学号
        res = re.findall(r'(\d{12})</td>\s+<td align="left">&nbsp;([一-龥]{2,5})</td>', req.content.decode('gbk', 'ignore'), re.S) # 成对提取学号和姓名
        if len(res) == 0:
            mbox('获取名单失败!','无法获取{}班名单，请手动检查教务名单页面！'.format(classes[i]),'error')
            sys.exit(0)
        #sum(['序号{0},成绩{0}'.format(i).split(',') for i in range(1, len(res)+1)],['班级'])
        for j in range(1,len(res)+1):
            students += [(res[j-1][0],res[j-1][1],classes[i])]
            worksheet.write(i+1,j,res[j-1][1])
            if j > n: worksheet.write(0,j,'序号'+str(j))
        if n < j: n = j
        #students += list((x[0],x[1],classes[i]) for x in res)
    curs.executemany('Insert Or Replace into students (id, name, class) values(?,?,?)',students)
    conn.commit()
    curs.close()
    conn.close()
    
    wb.save(GetDesktopPath()+'\\muster.xls') #桌面路径
    mbox('完成','请在桌面查看muster.xls文件!','info')

if __name__ == "__main__":
    main(sys.argv[1:])
