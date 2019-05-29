# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:24:17 2019

@author: xiaoniu29
"""

from sqlite3 import connect, OperationalError
from socket import socket, timeout
from time import localtime
from os import path
from sys import exit as sysexit
from myMod import mbox

sock = socket(2, 1) #socket.AF_INET=2, socket.SOCK_STREAM=1
sock.bind(('0.0.0.0', 8001))
sock.listen(5)
if localtime().tm_mon < 8:
    dbpath = "./hwmy"+str(localtime().tm_year-2)[-2:]+".db"
else:
    dbpath = "./hwmy"+str(localtime().tm_year-1)[-2:]+".db"
if not path.isfile(dbpath):
    print('No database file in exe path, check please!')
    mbox('错误','未能在程序目录下找到数据库文件{}！\n请查验后重试！'.format(dbpath[2:]),'error')
    sysexit(0)
conn = connect(dbpath)
curs = conn.cursor()
while True:
    connection,address = sock.accept()
    try:
        connection.settimeout(5)
        sql = connection.recv(1024).decode('utf-8')
        if len(sql)>0 and sql[:6]!='UPDATE':
            try:
                curs.execute(sql)
                conn.commit()
                datas = curs.fetchall()
                connection.send(str(datas).encode('gbk'))
            except OperationalError as e:
                connection.send(str(e).encode('gbk'))
        elif len(sql)>0 and sql[:6]=='UPDATE':
            print(sql[7:11])
            if sql[7:11] =='list': # 批量更新成绩
                scores = eval(sql[11:])
                #print(scores)
                for i in range(len(scores)):
                    curs.execute('UPDATE students SET score = '+str(scores[i][1])+' WHERE ID = "'+scores[i][0]+'"')
            else:
                curs.execute(sql)
            conn.commit()
            connection.send('"OK"'.encode('gbk'))
        else:
            connection.send('"Sql command format error!"'.encode('gbk'))
    except timeout:
        print('time out')
        connection.close()
