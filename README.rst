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

Excel2003以前的格式(\*.xls)，简单的读用 *xlrd* 简单的写用 *xlwt* ，功能需求更多用 `xlwings <https://blog.csdn.net/asanscape/article/details/80372743>`_

Excel2010以后的格式(\*.xlsx), 用 *openpyxl*

Tips
,,,,,,,


中文正则表达是匹配，很多很多的答案是 **\[\\u4e00-\\u9fa5]** ,但是在Emeditor里这个不好使，不仅匹配中文

找了一个仅仅匹配中文的正则式子 **\[\一-\龥]** 好用！！！

