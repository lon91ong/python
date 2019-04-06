Python相关的脚本联系
======================

gather
--------

抓取教务网站的学生名单

muster.py
------------

也是抓名单的脚本...

netTime.py
---------------

同步本地时间和某个特定网站的时间

Python折腾Excel
-----------------

`中文参考 <https://blog.csdn.net/sinat_28576553/article/details/81275650#%E4%BA%8C%E3%80%81%E4%BD%BF%E7%94%A8xlwt%E6%A8%A1%E5%9D%97%E5%AF%B9%E6%96%87%E4%BB%B6%E8%BF%9B%E8%A1%8C%E5%86%99%E6%93%8D%E4%BD%9C>`_ , `英文参考 <https://www.pyxll.com/blog/tools-for-working-with-excel-and-python/>`_

Excel2003以前的格式(\*.xls)，简单的读用 *xlrd* 简单的写用 *xlwt* ，功能需求更多用 `xlwings <https://blog.csdn.net/asanscape/article/details/80372743>`_

Excel2010以后的格式(\*.xlsx), 用 *openpyxl*

需要分析数据或数据量大可以用 *pandas*

Tips
,,,,,,,

实用的消息框函数

.. code:: python

 def Mbox(title, text, style = ''):
    import win32api,win32con
    if style == 'error':  # 错误
        win32api.MessageBox(0, text, title, win32con.MB_ICONERROR)
    elif style == 'info': # 信息
        win32api.MessageBox(0, text, title, win32con.MB_ICONASTERISK)
    elif style == 'warn': # 警告
        win32api.MessageBox(0, text, title, win32con.MB_ICONWARNING)
    else:
        win32api.MessageBox(0, text, title, win32con.MB_OK)


中文正则表达是匹配，很多很多的答案是 **\[\\u4e00-\\u9fa5]** ,但是在Emeditor里这个不好使，它不仅仅匹配中文。

找了一个仅仅匹配中文的正则式子 **\[\一-\龥]** 好用！！！

