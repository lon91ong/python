#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

from time import sleep
from os import path, _exit
from sys import executable
from logging import warning as warnlog, error as errlog
from threading import _start_new_thread as start_new_thread
from winreg import OpenKey, QueryValue, CloseKey, HKEY_CLASSES_ROOT

app_root = path.join(path.dirname(path.realpath(executable)))

try:
    key = OpenKey(HKEY_CLASSES_ROOT,'Lab\shell\open\command')
    lab_root = path.dirname(QueryValue(key,'').split('"')[1])
    CloseKey(key)
except:
    if path.isfile(path.join(app_root,r'USTCORi.WebLabClient.exe')):
        lab_root = app_root
    elif path.isfile(path.join(app_root,'..\\USTCORi.WebLabClient.exe')):
        lab_root = path.dirname(app_root)
    else:
        print('仿真环境未安装!')
        _exit(-1)
    pass
    
def spawn_later(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        sleep(seconds)
        try:
            target(*args, **kwargs)
        except Exception as e:
            warnlog('%s.%s 错误：%s', target.__module__, target.__name__, e)
    start_new_thread(wrap, args, kwargs)

def spawn_loop(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        while True:
            sleep(seconds)
            try:
                target(*args, **kwargs)
            except Exception as e:
                warnlog('%s.%s 错误：%s', target.__module__, target.__name__, e)
    start_new_thread(wrap, args, kwargs)

def wait_exit(msg, *msgargs, exc_info=False, wait=30, code=-1):
    from os import _exit
    errlog(msg, exc_info=exc_info, *msgargs)
    print(u'\n按回车键或 %d 秒后自动退出……' % wait)
    spawn_later(wait, _exit, code)

    input()
    _exit(code)

def single_instance(name):
    from os import remove
    lock_file = path.join(app_root, name + '.lock')

    def unlock():
        lock.close()
        remove(lock_file)

    while True:
        try:
            lock = open(lock_file, 'xb', 0)
        except FileExistsError:
            try:
                remove(lock_file)
            except:
                wait_exit('已经有一个 %s 实例正在运行中。', name)
        else:
            from atexit import register as regi
            regi(unlock)
            break

def labDic(xmlfile):
    from xml.etree.ElementTree import parse
    keys = ('ID','Lab')
    labs={}
    for lab in parse(xmlfile).findall("Experiment"):
        k = lab.attrib['Sort']
        if k not in labs.keys():
            labs[k]=[]
        labs[k].append(dict(zip(keys,(lab.attrib['ID'], lab.attrib['Name']))))
    return labs
