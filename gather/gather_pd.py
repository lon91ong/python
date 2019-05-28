# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:50:32 2019
抓取教务网站学生花名册
@author: xiaoniu29
"""

import sys, os, re
from lxml import etree 
import sqlite3, requests
from pandas import DataFrame, ExcelWriter
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
    #df_cla = pd.DataFrame(classes,columns=['classes'])
    conn = sqlite3.connect(exedir+'/hwmy'+grade+'.db') #参数路径
    curs = conn.cursor()
    conn.text_factory = str
    curs.execute('create table if not exists classes (id INTEGER PRIMARY KEY AUTOINCREMENT, class text not NULL collate nocase, unique (class))')
    students = []
    for cla in classes:
        curs.execute('Insert Or Replace into classes (class) values ("{0}")'.format(cla))
        try:
            req = requests.get('http://211.81.249.110/hmc/hmc_p.asp?trbj='+quote(classes[i],encoding='gb2312'),verify=False,timeout=(0.5,3))
        except requests.exceptions.RequestException as err:
            mbox('错误','网络连接错误:{0}\n错误类型:{1}\n请查验后重试!'.format(err,type(err)),'error')
            sys.exit(0)
        content = req.content.decode('gbk', 'ignore') # 忽略非法字符，replace则用?取代非法字符；
        ids = re.findall(r'\d{12}(?=</td>)', content)   # 所有的学号
        if len(ids) == 0:
            mbox('获取名单失败!','无法获取{}班名单，请手动检查教务名单页面！'.format(cla),'error')
            sys.exit(0)
        root = etree.HTML(content)
        for idn in ids:
            students.append({'id':idn,'name':root.xpath('//td[text()='+idn+']/following-sibling::td[1]/text()')[0].lstrip('\xa0'),'class':cla,'score':''})
    df_stu = DataFrame(students,columns=['id','name','class','score'])
    students = []
    #pd.io.sql.to_sql(df_cla,name='classes',con=conn,index=False,index_label=None,if_exists='replace')
    df_stu.to_sql(name='students',con=conn,index=False,index_label='id',if_exists='replace')
    #conn.commit()
    conn.close()
    for cla in classes:
        students.append([cla]+df_stu[df_stu['class']==cla]['name'].tolist())
    writer = ExcelWriter(GetDesktopPath()+'\\muster.xls')
    DataFrame(students,columns=['班级']+['序号{}'.format(i) for i in range(1, max(map(len,students)))]).to_excel(writer,'花名',index=False)
    writer.save()
    mbox('完成','请在桌面查看muster.xls文件!','info')

if __name__ == "__main__":
   main(sys.argv[1:])
