# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019
抓取教务网站学生花名册
@author: xiaoniu29
"""

import sys, os, re
from lxml import etree 
import sqlite3, requests, xlwt
from urllib.parse import quote

from myMod import mbox, GetDesktopPath, getFile
from getClasses import getClassName

def main(argv):
    exedir = os.path.dirname(os.path.abspath(sys.argv[0])) # 程序所在目录
    if len(sys.argv) < 2: #直接运行程序
        docpth = getFile(exedir,'打开课程表',"Word 10文档 (*.docx)|*.docx|Word 03文档 (*.doc)|*.doc||")
        if docpth == '':
            mbox( '错误','需要指定课程表文件!', 'error')
            sys.exit(0)
    else:
        docpth = os.path.abspath(sys.argv[-1])
    grade, classes = getClassName(docpth) #取年级、班级列表
    #print(classes)
    
    conn = sqlite3.connect(exedir+'/hwmy'+grade+'.db') #参数路径
    #mbox('info',os.path.dirname(os.path.realpath(sys.argv[0])),'info')
    #conn = sqlite3.connect(':memory:') #内存临时
    curs = conn.cursor()
    conn.text_factory = str #lambda x: str(x, "gbk", "ignore")
    '''
    try:
        curs.execute('select * from sqlite_master where type = "table" and name = "students"')
        if curs.fetchone() == None:
            curs.execute('create table students (id varchar(12) primary key, name varchar(12) not NULL collate nocase, class text collate nocase, score unsigned tinyint, unique (id))')
        curs.execute('select count(*) from sqlite_master where type = "table" and name = "classes"')
        if curs.fetchone() == 0:
            curs.execute('create table classes (id INTEGER PRIMARY KEY AUTOINCREMENT, class text not NULL collate nocase, unique (class))')
    except sqlite3.OperationalError as e:
        print("Error info:",e.args[0])
        pass
    '''
    curs.execute('create table if not exists students (id varchar(12) primary key, name varchar(12) not NULL collate nocase, class text collate nocase, score unsigned tinyint, unique (id))')
    curs.execute('create table if not exists classes (id INTEGER PRIMARY KEY AUTOINCREMENT, class text not NULL collate nocase, unique (class))')
    
    #curs.executemany('INSERT INTO classes VALUES (?,?,?)',[(3,'name3',19),(4,'name4',26)])
    
    #花名电子表
    workbook=xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("花名", cell_overwrite_ok=True)
    worksheet.write(0, 0,'班级')
    for i in range(len(classes)):
        worksheet.write(i+1,0,classes[i])
        
        try:
            curs.execute('insert into classes (class) values ("{0}")'.format(classes[i]))
        except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
            print("Error info:",e.args[0])
            pass
        
        req = requests.get('http://211.81.249.110/hmc/hmc_p.asp?trbj='+quote(classes[i],encoding='gb2312'))
        content = req.content.decode('gbk', 'ignore') # 忽略非法字符，replace则用?取代非法字符；
        ids = re.findall(r'\d{12}(?=</td>)', content)   # 所有的学号
        if len(ids) == 0:
            print(ids)
            mbox('获取名单失败!','无法获取名单，请手动检查教务名单页面！','error')
            sys.exit(0)
        root = etree.HTML(content)
        name = ''
        for j in range(len(ids)):
            name = root.xpath('//td[text()='+ids[j]+']/following-sibling::td[1]/text()')[0].lstrip('\xa0')
            worksheet.write(i+1,j+1,name)
            worksheet.write(0,j+1,'序号'+str(j+1))
            
            try:
                curs.execute('INSERT INTO students (id, name, class) VALUES ("%s", "%s", "%s")' % (ids[j],name,classes[i]))
            except (sqlite3.IntegrityError, sqlite3.OperationalError):
                pass
        
    conn.commit()
    
    workbook.save(GetDesktopPath()+'\\muster.xls') #桌面路径
    
    #curs.execute('SELECT name FROM students WHERE id="171304011039"')
    #curs.execute('SELECT * FROM classes)
    #print(curs.fetchone()[0])
    #print(len(curs.fetchall()))
    #curs.execute("drop table classes") #删除表
    curs.close()
    conn.close()
    
    mbox('完成','请在桌面查看muster.xls文件!','info')

if __name__ == "__main__":
   main(sys.argv[1:])
