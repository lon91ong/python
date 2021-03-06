# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 19:11:14 2017

@author: lon91ong

"""

import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter

base_link='http://211.81.249.110/hmc/'
resp = requests.get(base_link+'hmc.asp')
resp.encoding = 'gbk'
soup=BeautifulSoup(resp.text,'lxml')
trs = soup.find_all('tr',{'bgcolor':'#CCCCCC'})

#print(len(trs))
trs = [tr for tr in trs if tr('td')[1].text =='2015 ' and \
       tr('td')[2].string !='经济管理系' and tr('td')[2].string != '文法外语系']
#print(len(trs))

tab_g = []
for tr in trs:
    tds = tr('td')
    tab_g.append({'grade':tds[1].text[0:4],'series':tds[2].string,'major':tds[3].string,\
                  'class':tds[4].string,'link':tr(href=True)[0].get('href')})

#print(trs[1](href=True)[0].get('href'))
tab_s = []

for g in tab_g:
#if True:
#    g = tab_g[30]
    trs = []; #tab_c = []
    #sleep(2)
    print('班级：',g['class'])
    #print(base_link+quote(g['link'].encode('gbk'), safe='/:?='))
    while len(trs) == 0: # reload
        respl = requests.get(base_link+quote(g['link'].encode('gbk'), safe='/:?='))
        respl.encoding = 'gbk'
        soup=BeautifulSoup(respl.text,'lxml')
        trs = soup.find_all('td',{'align':'left'})
    for i in range(0,len(trs),2):
        tab_s.append({'id':trs[i].text,'name':trs[i+1].text[1:],'class':g['class'],'Grade':''})
    #print(tab_c)
    #tab_s.append(tab_c[:])
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet('tab_g')
col = 0
for key in tab_g[0].keys():
    worksheet.write(0,col,key)
    for i in range(len(tab_g)):
        worksheet.write_string(i+1,col,tab_g[i][key])
    col+=1
worksheet = workbook.add_worksheet('tab_s')
col = 0
for key in tab_s[0].keys():
    worksheet.write(0,col,key)
    for i in range(len(tab_s)):
        worksheet.write_string(i+1,col,tab_s[i][key])
    col+=1
workbook.close()
