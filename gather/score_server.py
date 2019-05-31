# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:24:17 2019

@author: xiaoniu29
"""

from sqlite3 import connect, OperationalError
from time import localtime
from os import path, system
from sys import exit as sysexit
from myMod import mbox
from websocket_server import WebsocketServer
from urllib.parse import unquote

system("mode con cols=72 lines=30")
server = WebsocketServer(8001,'0.0.0.0')
if localtime().tm_mon < 8:
    dbpath = "./hwmy"+str(localtime().tm_year-2)[-2:]+".db"
else:
    dbpath = "./hwmy"+str(localtime().tm_year-1)[-2:]+".db"
if not path.isfile(dbpath):
    print('No database file in exe path, check please!')
    mbox('错误','未能在程序目录下找到数据库文件{}！\n请查验后重试！'.format(dbpath[2:]),'error')
    sysexit(0)

def message_received(client, server, sqlcmd):
    global dbpath
    sqlcmd = unquote(sqlcmd)
    print('SQL command:',sqlcmd)
    conn = connect(dbpath)
    curs = conn.cursor()
    if len(sqlcmd)>0 and sqlcmd[:6].upper()=='SELECT':
        try:
            curs.execute(sqlcmd)
            conn.commit()
            datas = list(map(list,curs.fetchall()))
        except OperationalError as e:
            datas = str(e)
    elif len(sqlcmd)>0 and sqlcmd[:6].upper()=='UPDATE':
        if sqlcmd[7:11].lower() =='list': # 批量更新成绩
            scores = eval(sqlcmd[11:])
            #print(scores)
            for i in range(len(scores)):
                curs.execute('UPDATE students SET score = '+str(scores[i][1])+' WHERE ID = "'+scores[i][0]+'"')
            print('更新{}条记录！'.format(str(len(scores))))
        else:
            curs.execute(sqlcmd)
        conn.commit()
        datas = '"OK"'
    else:
        datas = '"Sql command format error!"'
    server.send_message(client,str(datas))
    conn.close()

server.set_fn_message_received(message_received)
server.run_forever()
