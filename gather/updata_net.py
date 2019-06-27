# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:50:32 2019

@author: xiaoniu29
"""

import xlwings as xw
import sys
from pywintypes import com_error
from urllib.parse import quote
from myMod import mbox, GetDesktopPath

try:
    #wb = xw.apps.active.books[sys.argv[2]]
    wb = xw.books.active
    ws = wb.sheets.active
except:
    print("Unexpected error:",sys.exc_info()[0])
    mbox('错误','服务性后台程序，勿点击运行！','error')
    sys.exit(0)
bkfile = '.\\成绩备份.xlsx'
if not path.exists(bkfile):
    bkfile = GetDesktopPath()+'\\成绩备份.xlsx'

def netsql(sqlcmd):
    from websocket import create_connection
    #from time import sleep
    try:
        wsn = create_connection('ws://10.0.18.207:8001')
    except:
        print("Server connect error! Code:",sys.exc_info()[1])
        datas = []
    else:
        wsn.send(sqlcmd)
        #sleep(1)
        datas = eval(wsn.recv()) #eval(sock.recv(1280).decode('gbk'))
        wsn.close()
    return datas

def initonce():
    classes = netsql('SELECT class FROM classes')
    if len(classes) == 0:
        mbox('错误','班级列表为空！\n请查验后重试！','error')
    else:
        try:
            wb.sheets[0].api.Unprotect()
            wb.sheets[0].cells(2,11).api.Validation.Delete()
            wb.sheets[0].cells(2,11).api.Validation.Add(3,1,3,','.join(t[0] for t in classes))
            wb.sheets[0].api.Protect()
            wb.sheets[1].api.Unprotect()
            wb.sheets[1].cells(1,2).api.Validation.Delete()
            wb.sheets[1].cells(1,2).api.Validation.Add(3,1,3,','.join(t[0] for t in classes))
            wb.sheets[1].api.Protect()
        except com_error as err:
            print("com_error: {}".format(err))
            pass

def downData():
    global ws
    # 清楚原有数据
    last_r = max(5,ws.range('A' + str(ws.cells.last_cell.row)).end('up').row)
    ws.api.Unprotect()
    if ws.index == 1:
        ws.range('A5:J'+str(last_r)).api.ClearContents()
        cla = wb.sheets[0].cells(2,11).value
    else:
        ws.range('A5:C'+str(last_r)).api.ClearContents()
        cla = wb.sheets[1].cells(1,2).value
        #mbox('信息','班级：'+cla,'info')
    if cla == None:
        print("没有该班级信息!")
    else:
        ws.range("A5").value = netsql('SELECT id,name FROM students where class ="'+quote(cla)+'"')
    ws.api.Protect()
    
    if ws.index == 1 and path.exists(bkfile):
        # 查询备份
        last_r = max(5,ws.range('A' + str(ws.cells.last_cell.row)).end('up').row)
        app=xw.App(visible=False,add_book=False)
        app.display_alerts=False
        app.screen_updating=False
        wbb = app.books.open(bkfile)
        try:
            ws.range("C5").value = wbb.sheets[cla].range('B2:G'+str(last_r-3)).value
            ws.cells(2,13).value = wbb.sheets[cla].cells(1,1).value
            ws.cells(3,13).value = wbb.sheets[cla].cells(1,2).value
        except:
            print("无成绩备份!")
            pass
        wbb.close()
        app.quit()

def upData():
    global ws
    # 成绩所在列为第5行末列
    last_c = ws.cells(5, ws.cells.last_cell.column).end('left').column # 末列，忽略隐藏列
    last_r = max(3,ws.range('A' + str(ws.cells.last_cell.row)).end('up').row) # 末行
    n = 0
    scores = []
    for i in range(5,last_r+1):
        if ws.cells(i,last_c).value == '' or ws.cells(i,last_c).value == None: #成绩为空
            continue
        scores += [(ws.cells(i,1).value,int(round(ws.cells(i,last_c).value * 100) / 100.0))]
        #curs.execute('UPDATE students SET score = '+str(int(wb.sheets[0].cells(i,last_c).value))+' WHERE ID = "'+wb.sheets[0].cells(i,1).value+'"')
        n = n+1
    status = netsql('UPDATE list'+str(scores))
    if status == 'OK':
        mbox('完成','成功录入 '+str(n)+' 条成绩数据!','info')
    # 成绩备份到桌面
    if ws.index == 1:
        app=xw.App(visible=False,add_book=False)
        app.display_alerts=False
        app.screen_updating=False
        if path.exists(bkfile): #已存在
            wbb = app.books.open(bkfile)
            try:
                ws = wbb.sheets.add(wb.sheets[0].cells(2,11).value)
            except ValueError:
                ws = wbb.sheets[wb.sheets[0].cells(2,11).value]
        else:   # 新建
            wbb = app.books.add()
            wbb.sheets[0].name = wb.sheets[0].cells(2,11).value
            wbb.save(bkfile)
            #ws = wbb.sheets.add(wb.sheets[0].cells(2,11).value)
            #wbb.sheets[1].delete()
            ws = wbb.sheets[0]
        ws.range('A2').value = wb.sheets[0].range('B5:H'+str(last_r)).value
        #if last_c == 13:
        ws.cells(1,1).value = wb.sheets[0].cells(2,13).value
        ws.cells(1,2).value = wb.sheets[0].cells(3,13).value
        wbb.save()
        wbb.close()

def main(argv):
    #if len(argv) <2: # 直接执行程序
    if argv[0] =='init':
        initonce()
    elif argv[0] =='down':
        downData()
    elif argv[0] =='up':
        upData()
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
