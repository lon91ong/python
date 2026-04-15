# -*- coding: utf-8 -*-
"""
合并两个更新频繁的节点:
    Clash节点: https://github.com/chfchf0306/clash
    V2ray节点: https://github.com/freefq/free/blob/master/v2

@author: xiaoniu29
"""

import requests
from yaml import safe_load
from base64 import b64encode, b64decode
from urllib3 import disable_warnings
from sys import exc_info,stderr
from urllib.parse import quote

disable_warnings()

def locReq(pth, sess):
    #from requests.exceptions import ConnectionError, ReadTimeout
    github = 'https://github.com'
    gitraw = [{'direct':True, 'url':'https://ghproxy.com/https://raw.githubusercontent.com'},
        {'direct':True, 'url':'https://raw.fastgit.org'},
        {'direct':True, 'url':'https://cdn.staticaly.com/gh'},
        {'direct':True, 'url':'https://cdn.jsdelivr.net/gh'},
        {'direct':True, 'url':'https://pd.zwc365.com/seturl/https://raw.githubusercontent.com'}]
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
               "Referer": github+pth[0],
               "Upgrade-Insecure-Requests": '1',
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
               "Connection": "close"
        }
    
    headers['Referer']=github+pth[0]+'/blob'+pth[1]
    fail = True # 失败标识
    for rawsvr in gitraw:
        try:
            print("Request URL:",rawsvr['url']+pth[0]+pth[1])
            resp = sess.get(rawsvr['url']+pth[0]+pth[1],headers=headers,verify=False,timeout=6)
        except:
            print("Unexpected error:", exc_info()[0], file=stderr)
            continue
            pass
        #print("Response status:",resp.status_code)
        if resp.status_code == 200:
        #else:
            fail = False
            break
    return '' if fail else resp.content

def gatherProxies():
    projList = [['/freefq/free','/master/v2'],['/chfchf0306/clash','/main/clash']]#,['/alanbobs999/TopFreeProxies','/master/Eternity']]
    # v2ray节点
    b64proxies = []
    failFlag = ['s','s']
    session = requests.Session()
    session.trust_env = False #避免系统代理的影响
    
    for i, proj in enumerate(projList):
        try:
            if 'clash' in proj[1]:
                proxies = safe_load(locReq(proj, session))["proxies"]
                for locp in proxies:
                    locp['name']=locp['name'].lower().replace(r'欢迎订阅youtube：','').replace(r'youtube:8度科技_','')
                    if locp["type"]=='ss':
                        b64s = b64encode(bytes(f'{locp["cipher"]}:{locp["password"]}@{locp["server"]}:{locp["port"]}',encoding='utf-8'))
                        b64proxies.append('ss://{}#{}'.format(b64s.decode('utf-8'),locp["name"].replace(' ','+')))
                    if locp["type"]=='vmess':
                        continue
                        if 'tls' in locp and locp["tls"]:
                            locp["tls"] = "tls"
                        else:
                            locp["tls"] = ""
                        if 'network' in locp:
                            if locp['network'] == 'tcp':
                                b64s = b64encode(bytes('{'+f'\r\n  "v": "2",\r\n  "ps": "{locp["name"]}",\r\n  "add": "{locp["server"]}",\r\n  "port": "{locp["port"]}",\r\n  "id": "{locp["uuid"]}",\r\n  "aid": "{locp["alterId"]}",\r\n  "net": "{locp["network"]}",\r\n  "type": "none",\r\n  "path": "",\r\n  "host": "{locp["server"]}",\r\n  "tls": ""\r\n'+'}',encoding='utf-8'))
                            else:
                                b64s = b64encode(bytes('{'+f'\r\n  "v": "2",\r\n  "ps": "{locp["name"]}",\r\n  "add": "{locp["server"]}",\r\n  "port": "{locp["port"]}",\r\n  "id": "{locp["uuid"]}",\r\n  "aid": "{locp["alterId"]}",\r\n  "net": "{locp["network"]}",\r\n  "type": "none",\r\n  "host": "{locp["ws-headers"]["Host"]}",\r\n  "path": "{locp["ws-path"]}",\r\n  "tls": "{locp["tls"]}"\r\n'+'}',encoding='utf-8'))
                        else:
                            b64s = b64encode(bytes('{'+f'\r\n  "v": "2",\r\n  "ps": "{locp["name"]}",\r\n  "add": "{locp["server"]}",\r\n  "port": "{locp["port"]}",\r\n  "id": "{locp["uuid"]}",\r\n  "aid": "{locp["alterId"]}",\r\n  "net": "",\r\n  "type": "none",\r\n  "host": "{locp["server"]}",\r\n  "path": "",\r\n  "tls": "{locp["tls"]}"\r\n'+'}',encoding='utf-8'))
                        b64proxies.append('vmess://'+b64s.decode('utf-8'))
                    if locp["type"]=='trojan':
                        b64proxies.append(f'trojan://{locp["password"]}@{locp["server"]}:{locp["port"]}#{quote(locp["name"])}')
            else:
                # v2ray节点,无需过多处理
                proxies = b64decode(locReq(proj, session)).decode().split('\n')
                for locp in proxies:
                    if locp[0:5] == 'vmess':
                        continue
                        tempstr = b64decode(locp[8:]).decode().replace('github.com/freefq - ','')
                        b64proxies.append('vmess://'+b64encode(tempstr.encode()).decode('utf-8'))
                    else:
                        b64proxies.append(locp.replace('github.com/freefq%20-%20','').lower().replace('youtube:8度科技_',''))
                #b64proxies.extend(proxies)
        except:
            print("Unexpected error:", exc_info()[0:2], file=stderr)
            print("Project "+proj[0]+" update failed!")
            failFlag[i] = 'f'
            pass
    return [''.join(failFlag),b64encode(bytes('\n'.join(b64proxies),encoding='utf-8')).decode()]

if __name__ == '__main__':
	from os import getcwd
	workpath = getcwd()
	result = gatherProxies()
	print("Status:",result[0])
	with open("/tmp/b64mess.txt","w",encoding='utf-8') as f:
		f.write(result[1])
