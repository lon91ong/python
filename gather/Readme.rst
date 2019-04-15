Python打包exe可执行文件
===========================

代码用途：
-----------

爬取教务网站的学生名单

方法一：
---------

打包Python脚本为exe程序的常用方式是使用pyinstaller将所有运行需要的库文件和脚本打包在一起，
好处就是处处（不管装没装python环境）都可以运行。
缺点就是文件很大，而且打包过程经常出错。

安装: *pip install pyinstaller*

打包方法: *pyinstaller py文件* 打包好的程序在 *dist* 目录下，默认不是单文件的形式，-F 参数指定单文件打包， -w 去黑屏

打包完了运行试试！ 不成功的话, 看看 **build\\项目名\\warn-项目名.txt** 内容, 
是不是有许多的 *missing module named ...blabla...*，
排错路漫漫...

参考笔记(按价值排序)
,,,,,,,,,,,,,,,,,,,,,,

`某侠笔记 <https://www.crifan.com/use_pyinstaller_to_package_python_to_single_executable_exe/>`_

`Pyinstaller打包用spec添加资源文件 <https://www.yuanrenxue.com/tricks/pyinstaller-spec.html>`_

`PyInstaller打包详解 <https://yujunjiex.gitee.io/2018/10/18/PyInstaller%E6%89%93%E5%8C%85%E8%AF%A6%E8%A7%A3/>`_

`官方排错参考 <https://pyinstaller.readthedocs.io/en/stable/when-things-go-wrong.html?highlight=win32com>`_

`某虾心得 <https://zhengzexin.com/2016/11/08/pyinstaller-da-bao-python-jiao-ben-de-yi-xie-xin-de>`_


方法二：
----------
另一种方式是通过批处理或vbs调用python脚本，优点就是文件体积小，缺点就是需要python环境。

打包批处理脚本用的工具：`Bat To Exe Converter <http://www.f2ko.de/en/b2e.php>`_

如果需要能直接用python脚本对某个文件进行读写的操作，想绕过命令行调用，直接鼠标拖上去执行，方法二就挺适合。

这个方法的缺点在于，会报毒！基本上所有的脚本语言打包成的exe都有这个问题！
