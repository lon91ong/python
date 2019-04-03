# -*- coding: utf-8 -*-
"""
删除下面的多行注释可以添加SQLite功能，
发现WPS居然不支持SQLite，所以就删了
"""

import sys, re, requests
from lxml import etree 
#import sqlite3
import docx, xlwt
from urllib.parse import quote

def GetDesktopPath():
    from win32com.shell import shell, shellcon
    deskpath =shell.SHGetSpecialFolderLocation(0, shellcon.CSIDL_DESKTOP)
    return shell.SHGetPathFromIDList(deskpath)

def main(argv):
    try:
        word = docx.Document(str(argv[-1]))
        #print('接收到的文件：'+str(argv[-1]))
        #word = docx.Document('E:\\花名\\M2019年春季学期2017级第二轮.docx')
        grade = re.search(r'(?<=20)\d{2}(?=级)',word.paragraphs[0].text).group()
        table = word.tables[0]
        classes = []
        for i in range(1,len(table.rows)):
            for j in range(2,len(table.columns)):
                mach = re.match(r'[\u4e00-\u9fa5]{2,5}\d{1,2}(?=班)',table.cell(i,j).text)
                if mach != None:
                    classes.append(mach.group())
    except:
        print('提取班级信息错误，请查验Word文档！')
        sys.exit()
    #print(classes)
    
    req = requests.get('http://211.81.249.110/hmc/hmc.asp')
    content = req.content.decode('gbk', 'ignore')
    allCla = re.findall(r'[\u4e00-\u9fa5]{2,10}(?=' + grade + '-\d{1,2}</a>)', content)
    allCla = list(set(allCla)) #合并重复，只保留专业全称
    #print(len(allCla))
    
    for i in range(len(classes)):
        temp = []
        for j in range(len(allCla)):
            n = len(classes[i])-1   #尾数不参与比对
            for c in classes[i][:-1]: #简称所有字符都在全称内
                if not(c in allCla[j]):
                    break
                else:
                    n = n-1
            if n==0: #全部找到用全称替换简称
                temp.append(allCla[j])
        #if len(temp)>1:print(classes[i],temp)
        classes[i] = min(temp,key=len)+grade+'-'+classes[i][-1] # 存在多个匹配对象时，取最短的
    #print(classes)
    
    '''
    #conn = sqlite3.connect(os.path.dirname(str(argv[-1]))+'\\hwmy.db') #参数路径
    conn = sqlite3.connect(':memory:') #内存临时
    cursor = conn.cursor()
    conn.text_factory = str #lambda x: str(x, "gbk", "ignore")
    try:
        cursor.execute('create table students'+grade+' (id varchar(12) primary key, name varchar(12) not NULL collate nocase, class text collate nocase, unique (id))')
        cursor.execute('create table classes'+grade+' (id varchar(2), class text not NULL collate nocase, unique (class))')
    except sqlite3.OperationalError as e:
        print(e.args[0])
        pass
    #cursor.executemany('INSERT INTO classes VALUES (?,?,?)',[(3,'name3',19),(4,'name4',26)])
    '''
    #花名电子表
    workbook=xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("花名", cell_overwrite_ok=True)
    worksheet.write(0, 0,'班级')
    for i in range(len(classes)):
        worksheet.write(i+1,0,classes[i])
        '''
        try:
            cursor.execute('insert into classes'+grade+' (id, class) values ("%s","%s")'%(str(i),classes[i]))
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            pass
        '''
        req = requests.get('http://211.81.249.110/hmc/hmc_p.asp?trbj='+quote(classes[i],encoding='gb2312'))
        content = req.content.decode('gbk', 'ignore') # 忽略非法字符，replace则用?取代非法字符；
        ids = re.findall(r'\d{12}', content)   # 所有的学号
        root = etree.HTML(content)
        name = ''
        for j in range(len(ids)):
            name = root.xpath('//td[text()='+ids[j]+']/following-sibling::td[1]/text()')[0].lstrip('\xa0')
            worksheet.write(i+1,j+1,name)
            worksheet.write(0,j+1,'序号'+str(j+1))
            '''
            try:
                cursor.execute('INSERT INTO students'+grade+' (id, name, class) VALUES ("%s", "%s", "%s")' % (ids[j],name,classes[i]))
            except (sqlite3.IntegrityError, sqlite3.OperationalError):
                pass
        
    conn.commit()
    '''
    workbook.save(GetDesktopPath().decode('utf-8')+'\\muster.xls') #桌面路径
    '''
    #cursor.execute('SELECT name FROM students'+grade+' WHERE id="171304011039"')
    #cursor.execute('SELECT * FROM classes'+grade)
    #print(cursor.fetchone()[0])
    #print(len(cursor.fetchall()))
    #cursor.execute("drop table classes") #删除表
    cursor.close()
    conn.close()
    '''

if __name__ == "__main__":
   main(sys.argv[1:])
