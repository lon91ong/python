# -*- coding: utf-8 -*-
"""
winXray配置丢失补丁
"""

import requests
from os import path, getenv
from base64 import b64decode
from re import split
from sys import executable
from urllib3 import disable_warnings
disable_warnings()
app_root = path.join(path.dirname(path.realpath(executable)))

def decode_b64(data):
    from base64 import urlsafe_b64decode
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '='* (4 - missing_padding)
    return urlsafe_b64decode(data).decode()

rawurl = 'https://gitee.com/sobweb/FreeD/raw/master/tv/movies.m3u'
headers = {"Referer": "https://www.gitee.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
    }

resp = requests.get(rawurl,headers=headers,verify=False,timeout=6)
proxies = b64decode(resp.content).decode().split('\n') if resp.status_code == 200 else []
n = 1; result =''
for locp in proxies:
    if locp[:3] == 'ssr':
        ssrl = split(':|&|/|=',decode_b64(locp[6:]))
        result += f'[{n}]='+'{protocol="ssr";'+'id="{}";'.format(decode_b64(ssrl[5]))+ \
            f'obfsParam="";port="{ssrl[1]}";'+ \
            'subscribeUrl="https://gitee.com/sobweb/FreeD/raw/master/tv/movies.m3u";'+ \
            f'address="{ssrl[0]}";obfs="{ssrl[4]}";'+'ps="{}";'.format(decode_b64(ssrl[-3]))+ \
            f'network="{ssrl[2]}";security="{ssrl[3]}"'+'};'
        n +=1

with open(path.join(app_root,'proxy_bak.table'), 'r', encoding='utf-8-sig') as f:
    prtab = f.readlines()
f.close()

with open(getenv('LocalAppData')+'/winXray/proxy.table', 'w', encoding='utf-8-sig') as f:
    for sl in prtab:
        if sl[:9] == 'outbounds':
            f.write('outbounds={'+result[:-1]+'};')
        else:
            f.write(sl)
f.close()

    
