# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:04:14 2020
@author: lon91ong
@description：根据gbk编码获取汉字首字母
"""

def CnFirstLetter(stc):
    if len(stc)>1: # Multi
        return CnFirstLetter(stc[0]) + CnFirstLetter(stc[1:])
    else:   # Single
        stc=stc.encode('gbk')
        gbkls = [b'\xb0\xc5',b'\xb2\xc1',b'\xb4\xee',b'\xb6\xea',b'\xb7\xa2',b'\xb8\xc1',b'\xb9\xfe',b'\xbb\xf7', \
                 b'\xbf\xa6',b'\xc0\xac',b'\xc2\xe8',b'\xc4\xc3',b'\xc5\xb6',b'\xc5\xbe',b'\xc6\xda',b'\xc8\xbb', \
                 b'\xc8\xf6',b'\xcb\xfa',b'\xcd\xda',b'\xce\xf4',b'\xd1\x89',b'\xd4\xd1',b'\xd7\xfa']
        abc_z = 'abcdefghjklmnopqrstwxyz'
        
        if stc<b'\xb0\xa1' or stc>b'\xd7\xf9':
            return ''
        else:
            for i in range(23):
                if stc < gbkls[i]:
                    return abc_z[i]
