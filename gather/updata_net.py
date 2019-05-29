# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019

@author: xiaoniu29
"""

import xlwings as xw
import sys, os
from pywintypes import com_error
from myMod import mbox

# 初始化,防止重复打开
try:
    wb = xw.apps.active.books['scoreRecord.xlsm']
except (AttributeError,KeyError,com_error) as err:
    print("Error info: {0}".format(err))
    wb = xw.Book(getattr(sys,'_MEIPASS',os.path.dirname(os.path.realpath(__file__)))+r'\scoreRecord.xlsm')
    pass

def netsql(sqlcmd):
    from socket import socket,error
    from time import sleep
    sock = socket(2,1) #socket.AF_INET=2, socket.SOCK_STREAM=1
    try:
        sock.connect(('10.0.18.207', 8001))
        sleep(1)
        #sock.send('hwmy17.db,SELECT class FROM classes'.encode('utf-8'))
        sock.send(sqlcmd.encode('utf-8'))
        datas = eval(sock.recv(1280).decode('gbk'))
    except error:
        print("Server connect error! Code:",sys.exc_info()[1])
        datas = []
    finally:
        sock.close()
    return datas

def initonce():
    classes = netsql('SELECT class FROM classes')
    if len(classes)==0:
        print("班级列表查询失败，请检查服务端!")
        sys.exit(0)
    try:
        wb.sheets[0].api.Unprotect()
        wb.sheets[0].cells(2,11).api.Validation.Delete()
        wb.sheets[0].cells(2,11).api.Validation.Add(3,1,3,','.join([t[0] for t in classes]))
        wb.sheets[0].api.Protect()
    except com_error as err:
        print("com_error: {}".format(err))
        pass
    
def downData():
    # 清楚原有数据
    last_r = max(5,wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row)
    wb.sheets[0].range('A5:J'+str(last_r)).api.ClearContents()
    
    cla = wb.sheets[0].cells(2,11).value
    #mbox('信息','班级：'+cla,'info')
    if cla == None:
        print("没有该班级信息!")
        sys.exit(0)
    # 从数据库读取学生信息
    wb.sheets[0].range("A5").value = netsql('SELECT id,name FROM students where class ="'+cla+'"')

def upData():
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
        initonce()
    elif argv[0] =='down':
        downData()
    elif argv[0] =='up':
        upData()
    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])