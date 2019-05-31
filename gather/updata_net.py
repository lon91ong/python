# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019

@author: xiaoniu29
"""

import xlwings as xw
import sys, os
from pywintypes import com_error
from urllib.parse import quote
from myMod import mbox

# 初始化,防止重复打开
def netsql(sqlcmd):
    from websocket import create_connection
    from time import sleep
    try:
        ws = create_connection('ws://10.0.18.207:8001')
        sleep(1)
        ws.send(sqlcmd)
        sleep(1)
        datas = eval(ws.recv()) #eval(sock.recv(1280).decode('gbk'))
    except:
        print("Server connect error! Code:",sys.exc_info()[1])
        datas = []
    else:
        ws.close()
    return datas

def initonce(filename):
    wb = xw.apps.active.books[filename]
    classes = netsql('SELECT class FROM classes')
    if len(classes)==0:
        mbox('错误','数据库服务连接失败！\n请查验后重试！','error')
        sys.exit(0)
    if wb == None:
        wb = xw.Book(getattr(sys,'_MEIPASS',os.path.dirname(os.path.realpath(__file__)))+r'\scoreRecord.xlsm')
        wb.sheets[0].cells(4,1).value = os.path.realpath(sys.argv[0])
    try:
        wb.sheets[0].api.Unprotect()
        wb.sheets[0].cells(2,11).api.Validation.Delete()
        wb.sheets[0].cells(2,11).api.Validation.Add(3,1,3,','.join([t[0] for t in classes]))
        wb.sheets[0].api.Protect()
    except com_error as err:
        print("com_error: {}".format(err))
        pass
    
def downData(filename):
    wb = xw.apps.active.books[filename]
    # 清楚原有数据
    last_r = max(5,wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row)
    wb.sheets[0].range('A5:J'+str(last_r)).api.ClearContents()
    
    cla = wb.sheets[0].cells(2,11).value
    #mbox('信息','班级：'+cla,'info')
    if cla == None:
        print("没有该班级信息!")
        sys.exit(0)
    # 从数据库读取学生信息
    wb.sheets[0].range("A5").value = netsql('SELECT id,name FROM students where class ="'+quote(cla)+'"')

def upData(filename):
    wb = xw.apps.active.books[filename]
    # 成绩所在列为第5行末列
    last_c = wb.sheets[0].cells(5, wb.sheets[0].cells.last_cell.column).end('left').column # 末列，忽略隐藏列
    last_r = max(5,wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row) # 末行
    n = 0
    scores = []
    for i in range(5,last_r+1):
        if wb.sheets[0].cells(i,last_c).value == '': #成绩为空
            print("成绩数据为空!")
            continue
        scores = scores + [(wb.sheets[0].cells(i,1).value,int(round(wb.sheets[0].cells(i,last_c).value * 100) / 100.0))]
        #curs.execute('UPDATE students SET score = '+str(int(wb.sheets[0].cells(i,last_c).value))+' WHERE ID = "'+wb.sheets[0].cells(i,1).value+'"')
        n = n+1
    status = netsql('UPDATE list'+str(scores))
    if status == 'OK':
        mbox('完成','成功录入 '+str(n)+' 条成绩数据!','info')
    #mbox.showinfo('完成','成功录入 '+str(n)+' 条成绩数据!')

def main(argv):
    if len(argv) <2: # 直接执行程序
        mbox('错误','服务性后台程序，勿点击运行！','error')
    elif argv[0] =='init':
        initonce(argv[1])
    elif argv[0] =='down':
        downData(argv[1])
    elif argv[0] =='up':
        upData(argv[1])
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
