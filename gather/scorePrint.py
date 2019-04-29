# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 14:53:17 2019

@author: xiaoniu29
"""

import os, sys
import sqlite3, xlwt

from myMod import mbox, GetDesktopPath, getFile
from getClasses import getClassName

exedir = os.path.dirname(os.path.abspath(sys.argv[0])) # 程序所在目录
docpth = getFile(exedir,'打开课程表',"Word 10文档 (*.docx)|*.docx|Word 03文档 (*.doc)|*.doc||")
if docpth == '':
    mbox( '错误','需要指定课程表文件!', 'error')
    sys.exit(0)
grade, classes = getClassName(docpth) #取年级、班级列表

datapth = getFile(os.path.dirname(os.path.abspath(sys.argv[0])),'打开成绩数据库',"SQLite数据库 (*.db)|*.db||")
if datapth == '':
    mbox( '错误','需要指定成绩数据库文件!', 'error')
    sys.exit(0)

try:
    conn = sqlite3.connect(datapth)
    curs = conn.cursor()
except (sqlite3.OperationalError, TypeError) as err:
    print("Error info: {0}".format(err))
    mbox('错误','数据库错误:{0}\n请查验后重试!'.format(err),'error')
    sys.exit(0)
    
#成绩电子表
wb =xlwt.Workbook(encoding="utf-8")
table = wb.add_sheet("成绩", cell_overwrite_ok=True)
table.write(0, 0,'班级')
for i in range(2,81,2):
    table.write(0,i-1,'姓名'+str(i>>1))
    table.write(0,i,'成绩'+str(i>>1))
for i,cla in enumerate(classes):
    curs.execute('SELECT name,score FROM students where class ="'+cla+'"')
    table.write(i+1, 0,cla)
    ns = curs.fetchall()
    for j in range(len(ns)):
        table.write(i+1,j*2+1,ns[j][0])
        table.write(i+1,j*2+2,ns[j][1] if ns[j][1] != None else 'NaN')

wb.save(GetDesktopPath()+'\\Score.xls') #桌面路径
mbox('完成','请在桌面查看Score.xls文件!','info')
