# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019

@author: xiaoniu29
"""

import sqlite3
import xlwings as xw
import sys, os
from pywintypes import com_error

# 准备消息框
def mbox(title, text, style = ''):
    import win32api,win32con
    if style == 'error':
        win32api.MessageBox(0, text, title, win32con.MB_ICONERROR)
    elif style == 'info':
        win32api.MessageBox(0, text, title, win32con.MB_ICONASTERISK)
    elif style == 'warn':
        win32api.MessageBox(0, text, title, win32con.MB_ICONWARNING)
    else:
        win32api.MessageBox(0, text, title, win32con.MB_OK)

#mbox.showinfo('length',__name__+'\n'+str(sys.argv))
if len(sys.argv) < 2: #命令行参数指定数据库文件
    mbox( '错误','需要指定数据库文件路径!', 'error')
    sys.exit(0)
#print(datapth)
# 初始化,防止重复打开
try:
    wb = xw.apps.active.books.active
except (AttributeError,com_error) as err:
    print("Error info: {0}".format(err))
    wb = xw.Book(getattr(sys,'_MEIPASS',os.path.dirname(os.path.realpath(__file__)))+r'\scoreRecord.xlsm')
    pass
#wb = xw.Book(r'scoreRecord.xlsm')
datapth = wb.sheets[0].cells(3,1).value

def initonce():
    global datapth
    wb.sheets[0].cells(3,1).value=datapth
    wb.sheets[0].cells(4,1).value=os.path.dirname(os.path.realpath(sys.argv[0]))
    try:
        conn = sqlite3.connect(datapth)
        curs = conn.cursor()
        curs.execute('SELECT class FROM classes')
    except (sqlite3.OperationalError, TypeError) as err:
        print("Error info: {0}".format(err))
        mbox('错误','数据库错误:{0}\n请查验后重试!'.format(err),'error')
        sys.exit(0)
    try:
        wb.sheets[0].api.Unprotect('m1101')
        wb.sheets[0].cells(2,11).api.Validation.Delete()
        wb.sheets[0].cells(2,11).api.Validation.Add(3,1,3,','.join([t[0] for t in curs.fetchall()]))
        wb.sheets[0].api.Protect('m1101')
    except com_error as err:
        print("com_error: {0}".format(err))
    #except:
    #    print("Unexpected error:", sys.exc_info()[0])
        pass
    curs.close()
    conn.close()

#if __name__ == "__main__":initonce()

def downData():
    global datapth
    # 清楚原有数据
    last_r = max(5,wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row)
    wb.sheets[0].range('A5:J'+str(last_r)).api.ClearContents()
    
    cla = wb.sheets[0].cells(2,11).value
    #print(cla)
    if cla == None:
        print("没有该班级信息!")
        sys.exit(0)
    if datapth == None:
        initonce()
    conn = sqlite3.connect(datapth)
    curs = conn.cursor()
    curs.execute('SELECT id,name FROM students where class ="'+cla+'"')
    res = curs.fetchall()
    for i in range(len(res)):
        wb.sheets[0].cells(i+5,1).value = res[i][0]
        wb.sheets[0].cells(i+5,2).value = res[i][1]
    curs.close()
    conn.close()

def upData():
    global datapth
    # 成绩所在列为第5行末列
    n = 0
    if wb.sheets[0].cells(3,13).api.EntireColumn.Hidden:
        last_c = 12
    else:
        last_c = wb.sheets[0].cells(5, wb.sheets[0].cells.last_cell.column).end('left').column
    conn = sqlite3.connect(datapth)
    curs = conn.cursor()
    for i in range(5,wb.sheets[0].range('A' + str(wb.sheets[0].cells.last_cell.row)).end('up').row+1):
        if wb.sheets[0].cells(i,last_c).value == '': #成绩为空
            print("成绩数据为空!")
            continue
        try:
            curs.execute('UPDATE students SET score = '+str(int(wb.sheets[0].cells(i,last_c).value))+' WHERE ID = "'+wb.sheets[0].cells(i,1).value+'"')
            n = n+1
        except:
            print("Unexpected error:",i,sys.exc_info()[0])
    conn.commit()
    curs.close()
    conn.close()
    mbox('完成','成功录入 '+str(n)+' 条成绩数据!','info')
    #mbox.showinfo('完成','成功录入 '+str(n)+' 条成绩数据!')

def clean():
    wb.sheets[0].api.Unprotect('m1101')
    wb.sheets[0].cells(2,11).api.Validation.Delete()
    wb.sheets[0].cells(2,11).api.ClearContents()
    wb.sheets[0].cells(3,1).api.ClearContents()
    wb.sheets[0].range('A5:J50').api.ClearContents()
    wb.sheets[0].api.Protect('m1101')
    wb.close()

def main(argv):
    global datapth
    if argv[0] =='down':
        downData()
    elif argv[0] =='up':
        upData()
    elif argv[0] == 'clean':
        clean()
    else: #normal
        datapth = os.path.abspath(argv[0]).replace('\\','/') # sqlite not fit \\
        initonce()
    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
