用Python折腾Excel的工具集
=============================

`原文链接 <https://www.pyxll.com/blog/tools-for-working-with-excel-and-python/>`_


Microsoft Excel几乎适用于所有行业。其直观的界面和易用性，可用于组织数据，执行计算和数据集分析，从而使其广泛应用于全球无数不同的领域。

无论您是否是Excel的粉丝，在某些时候您都必须处理它！对于许多应用程序，您不希望在Excel本身中执行复杂计算或管理大型数据集，但您可能需要从Excel中获取值作为输入，以Excel格式生成报表或向Excel用户提供工具。 Python可以是复杂任务的更好选择，幸运的是，有许多工具可供Python开发人员使用，因此Excel和Python可以一起使用。

这篇文章概述了一些最流行和最有用的工具，可以帮助您选择适合您特定应用的工具。

下面是一个功能矩阵，概述了从Excel调用Python的包的不同功能。

.. contents:: 文档目录

使用Excel作为前端构建交互式Python工具
---------------------------------------

Excel是许多任务的众所周知且非常好的用户界面。当您进入更复杂的任务并处理更大的数据集时，您很快就可以达到Excel中可以实现的极限。 Python是数据科学和其他学科的流行选择，因为它可以比单独的Excel更好地处理这些复杂的案例。通过同时使用它们并识别每个的优点，您可以使用Excel作为用户友好的前端构建非常强大的交互式工具，并在Python中完成所有繁重的工作。

.. image:: https://i0.wp.com/www.pyxll.com/blog/wp-content/uploads/2018/07/python-in-excel.png
   :align: center

Python是一种非常强大的语言，具有广泛的第三方库生态系统。在Excel电子表格中利用Python可以提高您的工作效率，并且无需将数据导入和导出Excel。交互式工作表可以使用Python代码开发，就像使用VBA一样，但具有Python的所有优点。

有一些工具可用于将Python引入Excel，并且很难知道哪种工具适合不同的情况。下面是每个的概述，我希望将突出它们之间的差异，并帮助您确定哪些是适合您需要实现的。

PyXLL – The Python Excel Add-In
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

PyXLL是目前唯一允许开发人员在Python中编写功能齐全的Excel插件的软件包。它将Python解释器嵌入到Excel中，以便它可以用作完整的VBA替换。您可以从概念上将其视为类似于Excel-DNA for C＃之类的东西，除了它是动态的并在Excel运行时导入您的Python代码 - 所以没有加载项来构建，并且在修改时不需要重新启动Excel Python代码。

.. code:: python

  from pyxll import xl_func
 
  @xl_func
  def py_test(a, b, c):
      return (a + b) * c

.. image:: https://i0.wp.com/www.pyxll.com/blog/wp-content/uploads/2018/07/zvM2CX1ACA.gif

更多特色功能：

- **Array functions**

 PyXLL可以处理数据数组，并支持NumPy和Pandas类型。返回数组的函数可以自动调整大小，以避免在结果的维度发生更改时出错。

- **Real Time Data**

 使用PyXLL的实时数据功能从Python将实时数据流式传输到Excel中。

- **Object Cache**
 对于返回Python对象的函数，而不是简单类型（字符串，数字等）或数组（NumPy数组和Pandas DataFrames或Series），PyXLL具有聪明的“对象缓存”。返回对象标识符，并且当传递到另一个函数时，标识符用于查找原始对象。这允许使用Excel公式在Python函数之间传递对象。这在处理大型数据集时非常有用，其中整个数据集不需要一次在Excel中可见，而是在Python函数之间传递 - 例如，加载大型数据集并执行一些聚合操作并在Excel中显示汇总结果。

- **Excel Object Model**

 PyXLL集成了主要的COM包pywin32和comtypes，它们允许从Excel宏和使用PyXLL编写的函数中使用整个Excel对象模型。这使得可以在VBA中完成的任何操作都可以在Python中完成。它还与xlwings集成，因此xlwings API也可用于从Excel读取和写入。

pywin32 / comtypes
,,,,,,,,,,,,,,,,,,,,

整个Excel API（或对象模型）通过COM公开。可以使用pywin32或comtypes在Python中使用Excel COM API编写可以编写为VBA宏的所有内容。

Excel COM API可以在Excel之外使用（例如，从正在运行的Python提示符，脚本或Jupyter笔记本）。如果您已经知道如何在VBA中执行某些操作，那么通过COM API在Python中执行等效任务通常非常简单。可以使用PyXLL使用Excel中的pywin32或comtypes调用例程（例如，从功能区栏，菜单项或宏上的按钮）。

假设把下面的VBA脚本转换成对应的Python语句

VBA

.. code:: VBA

 Sub Macro1()
    Range('B11:K11').Select
    Selection.AutoFill Destination:=Range('B11:K16'), Type:=xlFillDefault
    Columns('B:K').Select
    Selection.ColumnWidth = 4
 End Sub

Python

.. code:: python

 from win32com.client.gencache import EnsureDispatch
 from win32com.client import constants
 
 def Macro1():
     xl = EnsureDispatch('Excel.Application')
     xl.Range('B11:K11').Select()
     xl.Selection.AutoFill(Destination=xl.Range('B11:K16'), Type=constants.xlFillDefault)
     xl.Columns('B:K').Select()
     xl.Selection.ColumnWidth = 4
    
xlwings
,,,,,,,,

xlwings提供了上述Excel COM API的包装器，用于简化许多常见任务，例如将Pandas DataFrames编写到打开的Excel工作簿。它使用pywin32的COM包装器并允许您访问这些包装器，因此您可以随时根据需要使用常规Excel API。

与pywin32和comtypes一样，xlwings可以从普通的Python提示符或Jupyter笔记本中与Excel对话。为了使用Excel本身的xlwings调用代码，PyXLL提供了一种 `将Excel Application对象作为xlwings对象获取的便捷方法 <https://www.pyxll.com/docs/api/utils.html#xl-app>`_ 。这允许您在Python中编写Excel脚本并触发从功能区按钮或菜单项运行代码。示例用例可以是功能区按钮，用于从数据库中获取数据，构建报告以及将其直接写入正在运行的Excel中。

下面显示了如何读取和写入值到正在运行的Excel工作簿，包括Pandas DataFrame。

.. code:: python

 import xlwings as xw
 
 wb = xw.Book('workbook.xlsx')  # Open an existing Workbook
 sheet = wb.sheets['Sheet1']
 
 # read and write values from the worksheet
 sheet.range('A1').value = 'Foo'
 print(sheet.range('A1').value)
 
 # Write a Pandas DataFrames directly to the Excel sheet
 import pandas as pd
 df = pd.DataFrame([[1,2], [3,4]], columns=['a', 'b'])
 
 sht.range('A1').value = df
 
 # Read the DataFrame back, using the 'expand' option to read the whole table
 sht.range('A1').options(pd.DataFrame, expand='table').value

xlwings包括一种在Python中编写用户定义函数（UDF）或工作表函数的方法，这些函数从Excel中的公式调用，类似于PyXLL提供的用户定义函数。这些依赖于在Excel和VBA包装外部运行的服务器进程来调用该服务器。这是一个简单的解决方案，有一些缺点，例如性能不佳，并且这些功能只能从包含VBA包装器的工作簿中获得。

DataNitro
,,,,,,,,,,

DataNitro是另一种从Python控制Excel的API。目前尚不清楚它的API和现有的，易于理解的Microsoft Excel COM API的优势是什么，但它确实允许您在不离开Excel的情况下编写和运行脚本。它对用户定义的函数（工作表函数）有基本的支持，但它们在Excel进程之外运行，只有在只有一个Excel进程运行时才有效。

目前还不知道DataNitro是否仍处于活跃开发状态，但为了完整性而包含在此处。


.. csv-table:: Frozen Delights!
  :header:  "Feature", "DataNitro", "xlwings", "PyXLL", "Comments""
  :widths: 20, 10, 10, 10, 100"
  
  “Basic worksheet functions", "✔", "✔", "✔", "DataNitro and xlwings use an external Python process, xlwings requires VBA wrapper code"
  ”Real time data", "✘", "✘", "✔", "Stream real time data into Excel worksheets"
  “Ribbon customisation", "✘", "✘", "✔", "Give users a rich user experience with custom ribbon menus"
  ”Menu functions", "✘", "✘", "✔", "Call Python code from the Excel menu"
  “Object Cache", "✘", "✘", "✔", "Pass Python objects between worksheet functions seamlessly via an object cache"
  “IntelliSense", "✘", "✘", "✔", "IntelliSense tooltip as you type – PyXLL integrates with the ExcelDNA Intellisense Addin"
  "Thread safe worksheet functions", "✘", "✘", "✔", "Improve worksheet responsiveness by using Excel's own threadpool to run worksheet functions concurrently"
  "Asynchronous functions", "✘", "✘", "✔", "Don't block Excel waiting for long running functions"
  "Macros", "✘", "✔", "✔", "Macros are functions that can be attached to UI elements like buttons or called from VBA"
  "Keyboard shortcuts", "✘", "✘", "✔", "Keyboard shortcuts can be assigned to macros with PyXLL"
  "Macro sheet equivalent functions", "✘", "✘", "✔", "Call back into Excel from a worksheet function"
  "Function documentation", "✘", "✔", "✔", "Include Python function docstrings in the Excel function wizard"
  "Automatically resize arrays", "✘", "✔", "✔", "Array functions can resize automatically"
  "Volatile Functions", "✘", "✔", "✔", "Volatile functions are called every time a worksheet is recalculated"
  "Full Excel API exposed", "✘", "✔", "✔", "xlwings uses pywin32, PyXLL users can choose between pywin32, comtypes or xlwings"
  "Reload without restarting Excel", "✔", "✔", "✔", "Modules can be reloaded without restarting Excel. PyXLL also supports 'deep reloading' where all module dependencies are also reloaded."





