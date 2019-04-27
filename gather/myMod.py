# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:36:01 2019

@author: xiaoniu29
"""
import win32con
def mbox(title, text, style = ''):
    from win32api import MessageBox
    if style == 'error':
        MessageBox(0, text, title, win32con.MB_ICONERROR)
    elif style == 'info':
        MessageBox(0, text, title, win32con.MB_ICONASTERISK)
    elif style == 'warn':
        MessageBox(0, text, title, win32con.MB_ICONWARNING)
    else:
        MessageBox(0, text, title, win32con.MB_OK)

def GetDesktopPath():
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

def getFile(initdir="C:\\",title="Open File", filt = "All files (*.*)|*.*||"):
    from win32ui import CreateFileDialog
    dlg = CreateFileDialog(1, None, None,  win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST, filt)
    dlg.SetOFNTitle(title)
    dlg.SetOFNInitialDir(initdir)
    if dlg.DoModal() == win32con.IDOK:
        return dlg.GetPathName()
    else:
        return ''