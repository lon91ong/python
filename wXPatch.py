# -*- coding: utf-8 -*-
"""
winXray配置丢失补丁
"""

import requests
from os import path, getenv, startfile
from sys import exc_info
from base64 import b64decode
from re import split, search
from urllib3 import disable_warnings

disable_warnings()
app_root = path.dirname(path.realpath(__file__))


def decode_b64(data):
    from base64 import urlsafe_b64decode
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return urlsafe_b64decode(data).decode()


def getProxy(rawurl):
    urlst = ['https://raw.iqiq.io/lon91ong/python/master/sslink64',
             'https://fastly.jsdelivr.net/gh/lon91ong/python@master/sslink64',
             'https://cdn.staticaly.com/gh/lon91ong/python/master/sslink64',
             'https://gcore.jsdelivr.net/gh/lon91ong/python@master/sslink64']
    try:
        resp = requests.get(rawurl, headers=headers, verify=False, timeout=6)
        proxies = b64decode(resp.content).decode().split('\n') if resp.status_code == 200 else []
    except:
        print("Unexpected error:", exc_info()[0])
        for ral in urlst:
            try:
                print(ral)
                resp = requests.get(ral, headers=headers, verify=False, timeout=6)
                proxies = b64decode(resp.content).decode().split('\n') if resp.status_code == 200 else []
                break
            except:
                print("Unexpected error:", exc_info()[0])
                continue
    return proxies


with open(path.join(app_root, 'proxy_bak.table'), 'r', encoding='utf-8-sig') as f:
    prtab = f.readlines()
f.close()

for st in prtab:
    if st[:13] == 'subscribeUrls':
        rawurl = search('http[\w,:/\.\-]+', st)[0]
# print(rawurl)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}
# app_root = r'D:\Tools\WinXray'
if path.isfile(path.join(app_root, r'WinXray.exe')):
    wx_exe = path.join(app_root, r'WinXray.exe')
elif path.isfile(path.join(app_root, '..\\WinXray.exe')):
    wx_exe = path.join(path.dirname(app_root), r'WinXray.exe')

try:
    proxies = getProxy(rawurl)
    n = 1
    result = ''
    for locp in proxies:
        if locp[:3] == 'ssr':
            ssrl = split(':|&|/|=', decode_b64(locp[6:]))
            result += f'[{n}]=' + '{protocol="ssr";' + 'id="{}";'.format(decode_b64(ssrl[5])) + \
                      f'obfsParam="";port="{ssrl[1]}";' + f'subscribeUrl="{rawurl}";' + \
                      f'address="{ssrl[0]}";obfs="{ssrl[4]}";' + 'ps="{}";'.format(decode_b64(ssrl[-3])) + \
                      f'network="{ssrl[2]}";security="{ssrl[3]}"' + '};'
            n += 1
    print(f'Total of {n - 1} SSR nodes written!')
    with open(getenv('LocalAppData') + '/winXray/proxy.table', 'w', encoding='utf-8-sig') as f:
        for sl in prtab:
            if sl[:9] == 'outbounds':
                f.write('outbounds={' + result[:-1] + '};')
            else:
                f.write(sl)
    f.close()
except:
    pass
finally:
    startfile(wx_exe)
