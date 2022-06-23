# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:58:34 2019
@author: Administrator
"""

from sqlite3 import connect#, OperationalError
from time import localtime as lct
from os import path, system
from sys import exit as sysexit
from urllib.parse import unquote

import falcon
from json import dumps,loads
from waitress import serve
from falcon.http_status import HTTPStatus

system('mode con cols=52 lines=36')

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 18000)  # 5 hours
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

class Resource(object):
    def __init__(self, dbpth):
        self.dbpth = dbpth
        if not path.isfile(dbpth):
            print(f'未找到数据库文件:{dbpth}\n自动新建该文件...\n')
            print('用 Navicat 连接数据库, classes 表中添加班级(全)名!\n')
            conn = connect(dbpth)
            curs = conn.cursor()
            conn.text_factory = str #lambda x: str(x, "gbk", "ignore")
            curs.execute('create table if not exists students (id varchar(12) primary key, name varchar(12) not NULL collate nocase, class text collate nocase, score unsigned tinyint, unique (id))')
            curs.execute('create table if not exists classes (id INTEGER PRIMARY KEY AUTOINCREMENT, class text not NULL collate nocase, unique (class))')
            conn.commit()
            curs.close()
            conn.close()

    def dict_factory(self, cursor, row):
        return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))
    def on_get(self, req, resp):
        print("URL:", req.url)
        conn = connect(self.dbpth)
        curs = conn.cursor()
        conn.text_factory = str
        if req.path == '/classes':
            curs.execute('SELECT class FROM classes')
            resp.body = ','.join(t[0] for t in map(list,curs.fetchall()))
        elif req.path =='/class':
            if 'CLIENT' in req.headers and req.headers["CLIENT"]=='Excel':
                conn.row_factory = self.dict_factory
                curs.execute('SELECT id,name,score FROM students where class ="'+unquote(req.query_string)+'"')
                resp.body = dumps(curs.fetchall(),ensure_ascii=False)
            else: # Greasemonkdy Script get scores to fill Web Table
                curs.execute('SELECT id,score FROM students where class ="'+unquote(req.query_string)+'"')
                resp.body = dumps(dict(curs.fetchall()),ensure_ascii=False)
        else:
            resp.body = '非法途径访问！'
        resp.status = falcon.HTTP_200
        curs.close()
        conn.close()
        
    def on_post(self, req, resp):
        print("URL:", unquote(req.url))
        conn = connect(self.dbpth)
        curs = conn.cursor()
        if req.path == '/updata':
            if req.headers["CLIENT"]=='Excel':
                scores = loads(req.media)
                for score in scores:
                    curs.execute('UPDATE students SET score = '+str(score["score"])+' WHERE ID = "'+str(score["id"])+'"')
            elif req.headers["CLIENT"]=='WPS':
                scores = eval(req.media) #loads(req.media, strict=False)
                #print("Length:",len(scores))
                curs.executemany('Insert Or Replace into students (id, name, class, score) values(?,?,?,?)',scores)
            print('更新{}条记录！'.format(len(scores)))
            conn.commit()
            resp.body = dumps({"success": True,"Content":f'更新{len(scores)}条记录！'},ensure_ascii=False)
        else:
            resp.body = '非法途径访问！'
        resp.status = falcon.HTTP_201
        curs.close()
        conn.close()

dbpath = path.dirname(path.realpath(__file__)) + r'\hwmy'
dbpath += f'{str(lct().tm_year-(2 if lct().tm_mon < 8 else 1))[-2:]}.db'

app = falcon.API(middleware=[HandleCORS()])
for ite in ['/classes','/class','/updata']: app.add_route(ite, Resource(dbpath))

print("    数据库服务运行中...")
serve(app, listen='*:8001')
