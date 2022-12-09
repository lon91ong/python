# -*- coding: utf-8 -*-
"""
winXray配置丢失补丁
"""

import requests
from os import path, getenv, startfile
from sys import exc_info, executable
from base64 import b64decode
from json import loads
from re import split, search, sub
from urllib3 import disable_warnings
from urllib.request import unquote
#from time import sleep

disable_warnings()
app_root = path.dirname(path.realpath(executable))
wx_exe = (app_root if path.isfile(app_root + r'\WinXray.exe') else path.dirname(app_root)) + r'\WinXray.exe'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

def decode_b64(data):
    from base64 import urlsafe_b64decode
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return urlsafe_b64decode(data).decode()

def getProxy(rawurl, base64=True):
    urlst = [rawurl]+['https://raw.iqiq.io/lon91ong/python/master/sslink',
             'https://raw.fastgit.org/lon91ong/python/master/sslink',
             'https://fastly.jsdelivr.net/gh/lon91ong/python@master/sslink',
             'https://cdn.staticaly.com/gh/lon91ong/python/master/sslink',
             'https://gcore.jsdelivr.net/gh/lon91ong/python@master/sslink']
    proxies = []
    for ral in urlst:
        try:
            ral = ral[:-2] if ral[-2:]=='64' else ral
            resp = requests.get(ral, headers=headers, verify=False, timeout=6)
            if base64:
                proxies = [ral + '64'] + b64decode(resp.content).decode().split('\n')
            else:
                proxies = [ral + '64'] + resp.text.split('\n')[:-1]
        except:
            print(f'{ral} get failed with error:', exc_info()[0])
            continue
        else:
            break
    return proxies
    
with open(path.join(app_root, 'proxy_bak.table'), 'r', encoding='utf-8-sig') as f:
    prtab = f.readlines()
f.close()

try:
    ustr = search('http[\w,:/\.\-\@]+', prtab[4])[0]
    proxies = getProxy(ustr, ustr[-2:]=='64')
    prtab[4] = sub('http[\w,:/\.\-\@]+', proxies[0], prtab[4], 1)
    
    n = 1
    result = ''
    for locp in proxies[1:]:
        if locp[:3] == 'ssr':
            ssrl = split(':|&|/|=', decode_b64(locp[6:]))
            result += f'[{n}]=' + '{protocol="ssr";' + 'id="{}";'.format(decode_b64(ssrl[5])) + \
                      f'obfsParam="";port="{ssrl[1]}";' + f'subscribeUrl="{proxies[0]}";' + \
                      f'address="{ssrl[0]}";obfs="{ssrl[4]}";' + 'ps="{}";'.format(decode_b64(ssrl[-3])) + \
                      f'network="{ssrl[2]}";security="{ssrl[3]}"' + '};'
        elif locp[:5] == 'vmess':
            ssrl = loads(decode_b64(locp[8:]))
            result += f'[{n}' + ']={' + f'tls="{ssrl["tls"]}";path="{ssrl["path"]}";protocol="vmess";alterId={ssrl["aid"]};host="{ssrl["host"]}";' + \
                      f'port="{ssrl["port"]}";alpn="{ssrl["alpn"]}";scy="{ssrl["scy"]}";["type"]="{ssrl["type"]}";network="{ssrl["net"]}";' + \
                      f'subscribeUrl="{proxies[0]}";security="auto";address="{ssrl["add"]}";id="{ssrl["id"]}";sni="{ssrl["sni"]}";ps="{ssrl["ps"]}"'+ '};'
        elif locp[:5] == 'ss://':
            strs = split('@',locp[5:])
            ssrl = split(':', decode_b64(strs[0])) + split(':|#',strs[1])
            result += f'[{n}' + ']={' + f'port={ssrl[3]};network="tcp";address="{ssrl[2]}";id="{ssrl[1]}";' + \
                      f'ps="{ssrl[4]}";protocol="shadowsocks";security="{ssrl[0]}"' + '};'
        elif locp[:6] == 'trojan':
            ssrl = split(':|&|@|\?|#', locp[9:])
            result += f'[{n}' + ']={' + f'tls="{split("=",ssrl[3])[1]}";port={ssrl[2]};protocol="trojan";address="{ssrl[1]}";id="{ssrl[0]}";' + \
                      f'ps="{ssrl[-1]}";subscribeUrl="{proxies[0]}";network="{split("=",ssrl[4])[1]}' + '"};'
        elif locp[:6] == 'vless':
            ssrl = split(':|&|@|\?|#', locp[8:])
            result += f'[{n}' + ']={' + f'tls="{split("=",ssrl[4])[1]}";path="{unquote(split("=",ssrl[6])[1])}";' + \
                      f'network="{split("=",ssrl[5])[1]}";id="{ssrl[0]}";subscribeUrl="{proxies[0]}";port={ssrl[2]};address="{ssrl[1]}";' + \
                      f'ps="{ssrl[7]}";protocol="vless";security="{split("=",ssrl[3])[1]}' + '"};'
        else:
            continue
        n += 1
    print(f'Total of {n - 1} nodes written!')
    prtab[5] = 'outbounds={' + result[:-1] + '};'
    with open(getenv('LocalAppData') + '/winXray/proxy.table', 'w', encoding='utf-8-sig') as f:
        f.writelines(sl for sl in prtab)
except:
    print("Unexpected error:", exc_info()[0:2])
    pass
finally:
    startfile(wx_exe)
#sleep(5)
