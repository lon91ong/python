# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:04:14 2020
@author: lon91ong
@description：根据gbk编码获取汉字首字母
"""

def CnFirstLetter(stc):
    stc = list(stc)
    abc_z = 'abcdefghjklmnopqrstwxyz'
    gbkls = [b'\xb0\xc5',b'\xb2\xc1',b'\xb4\xee',b'\xb6\xea',b'\xb7\xa2',b'\xb8\xc1',b'\xb9\xfe', \
         b'\xbb\xf7',b'\xbf\xa6',b'\xc0\xac',b'\xc2\xe8',b'\xc4\xc3',b'\xc5\xb6',b'\xc5\xbe',b'\xc6\xda', \
         b'\xc8\xbb',b'\xc8\xf6',b'\xcb\xfa',b'\xcd\xda',b'\xce\xf4',b'\xd1\x89',b'\xd4\xd1',b'\xd7\xfa']
    result = ''
    while len(stc) > 0:
        ssc = stc.pop(0).encode('gbk')
        if ssc>b'\xb0\xa0' and ssc<b'\xd7\xfa':
            for i in range(23):
                if ssc < gbkls[i]:
                    result += abc_z[i]
                    break
    return result
