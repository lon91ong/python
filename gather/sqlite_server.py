# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:24:17 2019

@author: xiaoniu29
"""

import socket,sqlite3
from time import localtime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8001))
sock.listen(5)
if localtime().tm_mon < 8:
    dbpath = "E:/Programs/hwmy"+str(localtime().tm_year-2)[-2:]+".db"
else:
    dbpath = "E:/Programs/hwmy"+str(localtime().tm_year-1)[-2:]+".db"
conn = sqlite3.connect(dbpath)
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
            except sqlite3.OperationalError as e:
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
    except socket.timeout:
        print('time out')
        connection.close()