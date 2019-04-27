# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 16:57:59 2019

@author: xiaoniu29
"""
import sqlite3, os, sys
from myMod import mbox, GetDesktopPath

def main(argv):
    if len(argv)<1:
        mbox( '错误','需要指定数据库文件!', 'error')
        sys.exit()
    
    conn = sqlite3.connect(os.path.abspath(argv[0]))  # 分表
    curs = conn.cursor()
    curs.execute('select id,score from students where score not NULL')
    scores=curs.fetchall()
    curs.close()
    conn.close()
    
    conn = sqlite3.connect(GetDesktopPath()+'\\汇总.db') # 总表
    curs=conn.cursor()
    for i,s in scores:
        curs.execute('UPDATE students SET score = '+str(s)+' WHERE id = "'+i+'"')
    conn.commit()
    curs.close()
    conn.close()
    mbox('完成','累计汇总 '+str(len(scores))+' 条成绩数据!\n\n结果见桌面“汇总.db”文件。','info')
    
if __name__ == "__main__":
   main(sys.argv[1:])
   
