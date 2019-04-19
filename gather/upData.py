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
    import win32con
    from win32api import MessageBox
    if style == 'error':
        MessageBox(0, text, title, win32con.MB_ICONERROR)
    elif style == 'info':
        MessageBox(0, text, title, win32con.MB_ICONASTERISK)
    elif style == 'warn':
        MessageBox(0, text, title, win32con.MB_ICONWARNING)
    else:
        MessageBox(0, text, title, win32con.MB_OK)
        
def openDataBaseFile(initdir="C:\\"):
    import win32con
    from win32ui import CreateFileDialog
    dlg = CreateFileDialog(1, None, None,  win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST, "SQLite数据库 (*.db)|*.db||")
    dlg.SetOFNTitle('打开数据库')
    dlg.SetOFNInitialDir(initdir)
    if dlg.DoModal() == win32con.IDOK:
        return dlg.GetPathName()
    else:
        return ''

datapth = ''
if len(sys.argv) < 2: #直接运行程序
    datapth = openDataBaseFile(os.path.dirname(os.path.abspath(sys.argv[0])))
    if datapth == '':
        mbox( '错误','需要指定数据库文件!', 'error')
        sys.exit(0)
#print(datapth)
# 初始化,防止重复打开
try:
    wb = xw.apps.active.books['scoreRecord.xlsm']
except (AttributeError,com_error) as err:
    print("Error info: {0}".format(err))
    wb = xw.Book(getattr(sys,'_MEIPASS',os.path.dirname(os.path.realpath(__file__)))+r'\scoreRecord.xlsm')
    pass
xw.apps.active.api.width = 600

if datapth == '' and wb.sheets[0].cells(3,1).value != '':
    datapth = wb.sheets[0].cells(3,1).value
else:
    wb.sheets[0].cells(3,1).value = datapth
    wb.sheets[0].cells(4,1).value = os.path.dirname(os.path.realpath(sys.argv[0]))

def initonce():
    global datapth
    try:
        conn = sqlite3.connect(datapth)
        curs = conn.cursor()
        curs.execute('SELECT class FROM classes')
    except (sqlite3.OperationalError, TypeError) as err:
        print("Error info: {0}".format(err))
        mbox('错误','数据库错误:{0}\n请查验后重试!'.format(err),'error')
        sys.exit(0)
    #except:
        #mobx('错误','未知错误:', sys.exc_info()[0])
        #sys.exit(0)
    try:
        wb.sheets[0].api.Unprotect('')
        wb.sheets[0].cells(2,11).api.Validation.Delete()
        wb.sheets[0].cells(2,11).api.Validation.Add(3,1,3,','.join([t[0] for t in curs.fetchall()]))
        wb.sheets[0].api.Protect('')
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
    # 从数据库读取学生信息
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
    last_c = wb.sheets[0].cells(5, wb.sheets[0].cells.last_cell.column).end('left').column # 末列，忽略隐藏列
    #while last_c >= 12 and wb.sheets[0].api.Columns(last_c).Hidden:last_c = last_c-1
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

def main(argv):
    global datapth
    if len(argv) == 0: #直接运行程序
        initonce()
    else:
        if argv[0] =='down':
            downData()
        elif argv[0] =='up':
            upData()
        else: #normal
            datapth = os.path.abspath(argv[0]).replace('\\','/') # sqlite not fit \\
            initonce()
    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
