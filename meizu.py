# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time, pickle, cv2

def partshot(webdrv,element,filename):
    webdrv.save_screenshot(filename)    #shot entire page
    rec=element.rect
    points=[rec['x'],rec['y'],rec['x']+rec['width']-5,rec['y']+rec['height']-23]
    scr_img=Image.open(filename)
    scr_img.crop(points).save(filename) #crop partial imge


def discal():
    #构造一个3×3的结构元素 
    element = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    foo1 = cv2.imread('foo1.png',0);
    dilate = cv2.dilate(foo1, element)
    erode = cv2.erode(foo1, element)
    #将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
    foo1 = cv2.absdiff(dilate,erode);
    foo2 = cv2.imread('foo2.png',0);
    dilate = cv2.dilate(foo2, element)
    erode = cv2.erode(foo2, element)
    #将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
    foo2 = cv2.absdiff(dilate,erode);
    
    result = cv2.absdiff(foo2,foo1);
    #上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
    retval, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY); 
    
    locx=result.nonzero()[1]
    dis = max(locx)-56
    cv2.imwrite('foo0.jpg',cv2.bitwise_not(result))
    #print(dis)
    return dis
    

#profile = webdriver.FirefoxProfile()
#profile.set_preference("general.useragent.override",       # Mobile phone
#                       "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI 5LTE Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/6.9 Mobile Safari/537.36")
fox=webdriver.Firefox()
#mycookies= pickle.load(open("cookies.pkl", "rb"))
fox.get("https://login.flyme.cn")
#for cookie in mycookies:
#    fox.add_cookie(cookie)
fox.implicitly_wait(3)
try:
    buybtn=fox.find_element_by_css_selector('a[id="J_btnBuy"]')
    buybtn.click()
except:
    pass
if fox.title=="验证码登录":
    tepbtn=fox.find_element_by_css_selector('a[id="toAccountLogin"]')
    tepbtn.click()
if fox.title=="登录Flyme 账号":
    fox.find_element_by_css_selector('input[id="account"]').send_keys("********")
    fox.find_element_by_css_selector('input[id="password"]').send_keys("*********")
slider=fox.find_element_by_css_selector('div[class="gt_slider_knob gt_show"]')
ActionChains(fox).move_to_element(slider).perform()
time.sleep(1)
gt_box=fox.find_element_by_css_selector('div[class="gt_box"]')

span="再来一次:"
while fox.title=="登录Flyme 账号":  #span!="验证通过:":
    time.sleep(1)   #等待人工验证
    '''
        #ref_btn=fox.find_element_by_css_selector('a[class="gt_refresh_button"]')
        #ActionChains(fox).click(ref_btn).perform()
    ActionChains(fox).move_by_offset(-200,-200).perform()
    if span=="再来一次:" or span=="尝试过多:":
        time.sleep(3)
        ActionChains(fox).move_to_element(slider).perform()
        time.sleep(2)
        partshot(fox,gt_box,'foo1.png')
    ActionChains(fox).click_and_hold(slider).perform()
    time.sleep(0.5)    
    partshot(fox,gt_box,'foo2.png')
    time.sleep(1)
    #ActionChains(fox).release(slider).perform()
    try:
        offset = discal()
        print(offset)
        #for i in range(1,offset,3):
        ActionChains(fox).move_by_offset(offset,0).perform()
        ActionChains(fox).release(slider).perform()
    except ValueError:
        #fox.refresh()
        #fox.implicitly_wait(6)
        ActionChains(fox).release(slider).perform()
        continue
    
    #ActionChains(fox).move_to_element(slider).perform()
    #ActionChains(fox).click_and_hold(slider).perform()
    
    #ActionChains(fox).move_by_offset(offset,0).perform()
    #ActionChains(fox).release(slider).perform()
    
    #span=fox.find_element_by_css_selector('span[class="gt_info_type"]').text
    span=fox.find_element_by_xpath('//div[@class="gt_info_text"]/span').text
    if span!='':print(span)
    

fox.find_element_by_xpath('//span[@class="mzchkbox"]/span/i').click()
fox.find_element_by_css_selector('a[id="login"]').click()
'''
fox.find_element_by_css_selector('input[placeholder="省/直辖市"]').click();
fox.find_element_by_xpath('//div[@class="mz-downmenu"]/ul/li[24]').click();  #河北省24, 山西省28
fox.find_element_by_css_selector('input[placeholder="城市"]').click();
fox.find_element_by_xpath('//div[@class="mz-downmenu"][2]/ul/li[11]').click();  #秦皇岛11, 太原3
fox.find_element_by_css_selector('input[placeholder="区/县"]').click();
fox.find_element_by_xpath('//div[@class="mz-downmenu"][3]/ul/li[1]').click();   #海港区1, 万柏林区5
fox.find_element_by_css_selector('input[placeholder="乡镇/街道"]').click();
fox.find_element_by_xpath('//div[@class="mz-downmenu"][4]/ul/li[10]').click();    #白塔岭10, 兴华街4
fox.find_element_by_css_selector('input[id="addressFormDetail"]').send_keys("燕山大学西校区")

'''
buybtn=fox.find_element_by_css_selector('a[id="J_btnBuy"]')
buybtn.click()
fox.implicitly_wait(9)  #9秒内如果网页加载完成则不再等待
addbtn=fox.find_element_by_css_selector('div[id="addressOpenBtn"]')
addbtn.location_once_scrolled_into_view
addbtn.click()
fox.find_element_by_css_selector('input[id="addressFormName"]').send_keys("牛延强")
fox.find_element_by_css_selector('input[id="addressFormPhone"]').send_keys("13930369014")
province = fox.find_element_by_css_selector('input[placeholder="省/直辖市"]')
province.click()
downmenu=fox.find_element_by_css_selector('div[class="mz-downmenu"]')
dic=downmenu.get_attribute("stytle")
print (dic)
#print (dic["display"])
downmenu.find_element_by_link_text('河北省').location_once_scrolled_into_view

#picrange.screenshot('foo.png')

#inputbox=fox.find_element_by_css_selector('input[name="wd"]')
#btn=fox.find_element_by_css_selector('input[class="bg s_btn"]')
#inputbox.send_keys("diarybook.site")
#btn.click()
#time.sleep(15)
#fox.quit()
'''
