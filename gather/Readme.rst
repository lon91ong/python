Python打包exe可执行文件
===========================

方法一：
---------

打包Python脚本为exe程序的常用方式是使用pyinstaller将所有运行需要的库文件和脚本打包在一起，
好处就是处处（不管装没装python环境）都可以运行。
缺点就是文件很大，而且打包过程经常出错。

安装: *pip install pyinstaller*

打包方法: *pyinstaller -F -w py文件名*

打包完了别急着运行,先看看build目录 **项目名** 子目录下的 **warn-项目名.txt** 文件内容, 
是不是有许多的 *missing module named ...blabla...*
排错路漫漫, 才刚刚开始...

`一些打包心得 <https://zhengzexin.com/2016/11/08/pyinstaller-da-bao-python-jiao-ben-de-yi-xie-xin-de>`_


方法二：
----------
另一种方式是通过批处理或vbs调用python脚本，优点就是文件体积小，缺点就是需要python环境。

打包批处理脚本用的工具：`Bat To Exe Converter <http://www.f2ko.de/en/b2e.php>`_
