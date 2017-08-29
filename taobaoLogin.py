# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 08:16:12 2017

@author: xiaoniu29
"""

import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import re

# 模拟登录淘宝类
# 登录淘宝流程
# 1、请求地址https://login.taobao.com/member/login.jhtml获取到token
# 2、请求地址https://passport.alibaba.com/mini_apply_st.js?site=0&token=1L1nkdyfEDIA44Hw1FSDcnA&callback=callback 通过token换取st
# 3、请求地址https://login.taobao.com/member/vst.htm?st={st}实现登录
class Taobao:

    # 初始化方法
    def __init__(self):
        # 登录的URL，获取token
        self.request_url = 'https://login.taobao.com/member/login.jhtml'
        # 通过st实现登录的URL
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        # 用户中心地址
        self.user_url = 'https://izhongchou.taobao.com/index.htm'
        # 代理IP地址，防止自己的IP被封禁
        self.proxy_ip = 'http://110.73.32.244:8123'
        # 登录POST数据时发送的头部信息
        self.request_headers =  {
            'Host':'login.taobao.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Referer' : 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection' : 'Keep-Alive'
        }
        # 用户名
        self.username = 'lon91ong'
        # ua字符串，经过淘宝ua算法计算得出，包含了时间戳,浏览器,屏幕分辨率,随机数,鼠标移动,鼠标点击,其实还有键盘输入记录,鼠标移动的记录、点击的记录等等的信息
        self.ua = '098#E1hva9v9vlOvn9CkvvvvvjiPP2M9gj3EnLzytjnEPV/EQm64fVzZ6m64P0MOyc+4RFKx6jEVPssh1j+4RLd9AmDPnVM9yLyCvvBvpvvvCQhvV734zYMwSDKKuufo7Q38sajEsPdovKuqsw6jvpvx4HdNzYAJVTTuir82oIFWAbSjvYUmrQhvHUJVeiu4PY0n1XI8/MKUMijq5M5b9phvVe3J+RJUzHi47esoz0feid58KznsA+5WSdebrQhvCIeEeiujQ2yCvvBvpvvvRphvChCvvvmrvpvEphHlmWGvphZ5dphvmZCCvQFnvhCHOTwCvvBvpvpZRphvChCvvvvCvpvVphhvvvvvuphvmhCvCjyLnkeEkphvCyEmmvpfVbyCvm3vpvvvvvCHtZCvmRgvvh8pphvZ99vvpGavpComvvC2j6CvHUUvvhWNUphCjg5eeyf9DP0n/+2EAJobqIN5ApqqtgcI3TNhmpJ5AKACTggWAJobqIN5AppmMEjD0SKJM9PT5/uJzUqel/mZMOzTzGsPKMu+5dARgb/TFqSYgEImmJ4CTIbeyG9RTOfdkKfUMp5DQbKRKM62mRAEGaM3DpwmMUFtkdRwApf59RmRiYPqmJubt+Fu3pNEtO2y3KAJApf59R4LMaWhvSABtadTk9NcTaKgFN5cAG/13q/bStjBsqAh+UoYFrjUStVYkfFasn8gkG4vKJPNzuqUrW2eD+vEMOe6QPKRMG2T5/0h/tqY2r0P1NF3Dpg8/YTqFddqSGAYFGMuKgqWgRVfgOq59P6mtt856/kjMPS5AJuHtWjWsqdGgUqrkCbUgELymphvLhHiqpmFhmpXEcqyaBTAVA+aWqVxnqW6cjYWAWpfjcH2aZfv+2Kz8Zl9ZRAn+byDCcHhTWeARFxjb9TxfXkK46C+mPLpjC3672XXiXhPvpvhPBsumOwCvvBvppvvdphvmZCmj9klvhChzu6CvvDvpDZUBQCvB8VrvpvEphhBmHUvphcI9phv2Hif9JGxzHi47ePSzghCvCB4cKNSMr147DiISKNGll1N7IdNZbwCvv4EkEu43ekzvpvZ3g44eINZzOzHe9GnqXM53KoC/w+tvpvhphvvvbwCvCoj3tu4e9saFw742Qzr5/JVtUjtAqwCvCoj3iu45FsaFw742Qzr5/JVtUjtAsyCvvBvpvvv9phvVe3JpJJAzHi47dh6zAcjdw/G1AnqBeuqs+RY'
        # 密码，在这里不能输入真实密码，淘宝对此密码进行了加密处理，256位，此处为加密后的密码
        self.password2 = '567c123eae6dd4b875bde649cb925106717d1ff3d00b3082a2e4e2f2e935a6420a30b8cb8af4a69ba8d9d371a2b3a61ce81e8a43299657bddc70d9d3b33169ff2a8515d43321c673496f437d1262a30741a79ab07bf49b8b94c2870de9c938d4e4be5726e3432aab0601a04ae78d1ae6aff6a97b274c74e12e03bde7f82486e9'
        self.post = {
            'TPL_username':self.username,
            'TPL_password':'',
            'ncoSig':'',
            'ncoSessionid':'',
            'ncoToken':'0fb0f7ed54f73f6d0a67e49430110a5682bf8f8d',
            'slideCodeShow':'false',
            'useMobile':'false',
            'lang':'zh_CN',
            'loginsite':'0',
            'newlogin':'0',
            'TPL_redirect_url':'https://izhongchou.taobao.com/index.htm',
            'from':'tb',
            'fc':'default',
            'style':'default',
            'css_style':'',
            'keyLogin':'false',
            'qrLogin':'true',
            'newMini':'false',
            'newMini2':'false',
            'tid':'',
            'loginType':'3',
            'minititle':'',
            'minipara':'',
            'pstrong':'',
            'sign':'',
            'need_sign':'',
            'isIgnore':'',
            'full_redirect':'',
            'sub_jump':'',
            'popid':'',
            'callback':'',
            'guf':'',
            'not_duplite_str':'',
            'need_user_id':'',
            'poy':'',
            'gvfdcname':'10',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61323135702E313539363634362E3735343839343433372E372E34343165323830334F46305A454426663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246697A686F6E6763686F752E74616F62616F2E636F6D253246696E6465782E68746D',
            'from_encoding':'',
            'sub':'',
            'TPL_password_2':self.password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp':'',
            'oslanguage':'zh-CN',
            'sr':'1440*900',
            'osVer':'',
            'naviVer':'chrome|60.03112113',
            'osACN':'Mozilla',
            'osAV':'5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'osPF':'Win32',
            'miserHardInfo':'',
            'appkey':'',
            'nickLoginLink':'',
            'mobileLoginLink':'https://login.taobao.com/member/login.jhtml?redirectURL=https://izhongchou.taobao.com/index.htm&useMobile=true',
            'showAssistantLink':'',
            'um_token':'HV01PAAZ0bb3b0ccd351ff0259a3705101825745',
            'ua':self.ua
        }
        # 将POST的数据进行编码转换
        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='GBK')
        # 设置代理
        self.proxy = urllib.request.ProxyHandler({'http': self.proxy_ip})
        # 设置cookie
        self.cookie = http.cookiejar.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen; 插入self.proxy参数实现代理
        self.opener = urllib.request.build_opener(self.cookieHandler, urllib.request.HTTPHandler)
        # 赋值J_HToken
        self.J_HToken = ''
        # 登录成功时，需要的Cookie
        self.newCookie = http.cookiejar.CookieJar()
        # 登陆成功时，需要的一个新的opener
        self.newOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.newCookie))

    # 利用st码进行登录
    # 这一步我是参考的崔庆才的个人博客的教程，因为抓包的时候并没有抓取到这个url
    # 但是如果不走这一步，登录又无法成功
    # 区别是并不需要传递user_name字段，只需要st就可以了
    def login_by_st(self, st):
        st_url = self.st_url.format(st=st)
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host':'login.taobao.com',
            'Connection' : 'Keep-Alive'
        }
        request = urllib.request.Request(st_url, headers=headers)
        response = self.newOpener.open(request)
        content =  response.read().decode('gbk')

        #检测结果，看是否登录成功
        pattern = re.compile('top.location.href = "(.*?)"', re.S)
        match = re.search(pattern, content)
        #print(match)
        if match:
            self.cookie
            print(u'登录网址成功')
            return True
        else:
            print(u'登录失败')
            return False


    # 程序运行主干
    def login(self):
        try:
            # 请求登录地址， 此时返回的页面中有两个js的引入
            # 位置是页面的前两个JS的引入，其中都带有token参数
            request = urllib.request.Request(self.request_url, self.post_data, self.request_headers)
            response = self.opener.open(request)
            content = response.read().decode('gbk')
            # 抓取页面中的两个获取st的js
            pattern = re.compile('<script src=\"(.*)\"><\/script>')
            match = pattern.findall(content)

            # [
            # 'https://passport.alibaba.com/mini_apply_st.js?site=0&token=1gSq91qelNOc0Y9mmkT1DuQ&callback=callback',
            # 'https://passport.alipay.com/mini_apply_st.js?site=0&token=1SkqPzxjcniMfXh_sM_n4eQ&callback=callback',
            # 'https://g.alicdn.com/kissy/k/1.4.2/seed-min.js',
            # ]
            # 其中第一个是我们需要请求的JS，它会返回我们需要的st
            #print(match)


            # 如果匹配到了则去获取st
            if match:
                # 此时可以看到有两个st， 一个alibaba的，一个alipay的，我们用alibaba的去实现登录
                request = urllib.request.Request(match[0])
                response = urllib.request.urlopen(request)
                content = response.read().decode('gbk')

                # {"code":200,"data":{"st":"1lmuSWeWh1zGQn-t7cfAwvw"} 这段JS正常的话会包含这一段，我们需要的就是st
                #print(content)

                # 正则匹配st
                pattern = re.compile('{"st":"(.*?)"}')
                match = pattern.findall(content)

                # 利用st进行登录
                if match:
                    self.login_by_st(match[0])
                else:
                    print(u'无法获取到st，请检查')
                    return

        except urllib.error.HTTPError as e:
            print(u'请求失败，错误信息：', e.msg)


taobao = Taobao()
taobao.login()


