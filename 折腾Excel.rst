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
  :align: center

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


.. csv-table:: **Feature Matrix For Integrating Python and Excel**
  :header:  "Feature", "DataNitro", "xlwings", "PyXLL", "Comments"
  :widths: 50, 10, 10, 10, 90
  
  "Basic worksheet functions", "✔", "✔", "✔", "DataNitro and xlwings use an external Python process, xlwings requires VBA wrapper code"
  "Real time data", "✘", "✘", "✔", "Stream real time data into Excel worksheets"
  "Ribbon customisation", "✘", "✘", "✔", "Give users a rich user experience with custom ribbon menus"
  "Menu functions", "✘", "✘", "✔", "Call Python code from the Excel menu"
  "Object Cache", "✘", "✘", "✔", "Pass Python objects between worksheet functions seamlessly via an object cache"
  "IntelliSense", "✘", "✘", "✔", "IntelliSense tooltip as you type – PyXLL integrates with the ExcelDNA Intellisense Addin"
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


简单的读写Excel文件
-------------------

对于某些任务，您可能需要直接读取或写入Excel文件。对于批处理或在服务器上运行的任务，可能未安装Excel。以下软件包允许您直接读取和写入Excel文件，而无需使用Excel。

.. image:: https://i2.wp.com/www.pyxll.com/blog/wp-content/uploads/2018/07/excel-to-xlsx.png?
 :align: center

OpenPyXL
,,,,,,,,,,
 
对于使用Excel 2010以上，OpenPyXL是一个很好的全面选择。使用OpenPyXL，您可以读取和写入xlsx，xlsm，xltx和xltm文件。以下代码显示了如何使用几行Python将Excel工作簿编写为xlsx文件。
 
.. code:: python

 from openpyxl import Workbook
 wb = Workbook()
 # grab the active worksheet
 ws = wb.active
 # Data can be assigned directly to cells
 ws['A1'] = 42
 # Rows can also be appended
 ws.append([1, 2, 3])
 # Save the file
 wb.save('sample.xlsx')

不要将OpenPyXL与PyXLL混淆。两者完全不同，用途不同。 OpenPyXL是用于读取和写入Excel文件的包，而PyXLL是用于构建功能齐全的Excel加载项以将Python代码集成到Excel中的工具。

OpenPyXL涵盖了Excel的更多高级功能，如图表，样式，数字格式和条件格式。它甚至包括一个用于解析Excel公式的tokenizer！

编写报告的一个非常好的功能是它对NumPy和Pandas数据的内置支持。要编写Pandas DataFrame，所需的只是包含的'dataframe_to_rows'函数：

.. code:: python

 from openpyxl.utils.dataframe import dataframe_to_rows
 
 wb = Workbook()
 ws = wb.active
 
 for r in dataframe_to_rows(df, index=True, header=True):
 ws.append(r)
 
 wb.save('pandas_openpyxl.xlsx')

如果您需要读取Excel文件来提取数据，那么OpenPyXL也可以这样做。 Excel文件类型非常复杂，openpyxl在将它们读入易于在Python中访问的表单方面做得非常出色。虽然openpyxl无法加载某些内容，例如图表和图像，因此如果您打开文件并使用相同的名称保存它，则某些元素可能会丢失。

.. code:: python

 from openpyxl import load_workbook
 
 wb = load_workbook(filename = 'book.xlsx')
 sheet_ranges = wb['range names']
 print(sheet_ranges['D18'].value)

OpenPyXL的一个可能的缺点是处理大文件可能会非常慢。如果你必须编写包含数千行的报告，并且你的应用程序是时间敏感的，那么XlsxWriter或PyExcelerate可能是更好的选择。

- `openpyxl官方文档 <https://openpyxl.readthedocs.io/en/stable>`_

XlsxWriter
,,,,,,,,,,,,

如果您只需要编写Excel工作簿而不是阅读它们，那么XlsxWriter是一个易于使用的软件包，可以很好地使用。如果您正在处理大文件或者特别关注速度，那么您可能会发现XlsxWriter比OpenPyXL更好。

XlsxWriter是一个Python模块，可用于在Excel 2007+ XLSX文件中写入多个工作表的文本，数字，公式和超链接。它支持格式化等功能，包括：

- 100% compatible Excel XLSX files.
- Full formatting.
- Merged cells.
- Defined names.
- Charts.
- Autofilters.
- Data validation and drop down lists.
- Conditional formatting.
- Worksheet PNG/JPEG/BMP/WMF/EMF images.
- Rich multi-format strings.
- Cell comments.
- Textboxes.
- Integration with Pandas.
- Memory optimization mode for writing large files.

使用XlsxWriter编写Excel工作簿非常简单。可以使用Excel地址表示法（如“A1”）或行号和列号来写入单元格。下面是一个基本示例，显示创建工作簿，添加一些数据并将其另存为xlsx文件。

.. code:: python

 import xlsxwriter
 
 workbook = xlsxwriter.Workbook('hello.xlsx')
 worksheet = workbook.add_worksheet()
 
 worksheet.write('A1', 'Hello world')
 
 workbook.close()
 
如果您正在使用Pandas，那么您将需要使用XlsxWriter的Pandas集成。将Pandas DataFrames写入Excel，甚至创建图表都需要付出艰辛的努力。

.. code:: python

 import pandas as pd
 
 # Create a Pandas dataframe from the data.
 df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})
 
 # Create a Pandas Excel writer using XlsxWriter as the engine.
 writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
 
 # Get the xlsxwriter objects from the dataframe writer object.
 workbook  = writer.book
 worksheet = writer.sheets['Sheet1']
 
 # Create a chart object.
 chart = workbook.add_chart({'type': 'column'})
 
 # Configure the series of the chart from the dataframe data.
 chart.add_series({'values': '=Sheet1!$B$2:$B$8'})
 
 # Insert the chart into the worksheet.
 worksheet.insert_chart('D2', chart)
 
 # Convert the dataframe to an XlsxWriter Excel object.
 df.to_excel(writer, sheet_name='Sheet1')
 
 # Close the Pandas Excel writer and output the Excel file.
 writer.save()
 
在工作表中引用Pandas数据时（如上图中的公式所示），您必须确定数据在工作表中的位置，以便公式指向正确的单元格。对于涉及大量公式或图表的报告，这可能会产生问题，因为做一些简单的事情就像添加额外的行需要调整所有受影响的公式一样。对于像这样的报告'xltable'包可以提供帮助。

XLTable
,,,,,,,,,

XLTable是一个更高级别的库，用于从pandas DataFrames构建Excel报告。不是逐个单元地或逐行地编写工作簿，而是添加整个表，并且可以包括引用其他表的公式，而不必提前知道这些表的位置。对于涉及公式的更复杂的报告，xltable非常有用。

使xltable比直接编写Excel文件更有用的主要特性是，它可以处理包含与工作簿中的单元格相关的公式的表，而无需事先知道这些表将放在工作表上的位置。因此，只有将所有表添加到工作簿并且正在编写工作簿时，才会将公式解析为其最终单元格地址。

如果您需要编写包含公式而不仅仅是数据的报表，XLTable可以通过跟踪单元格引用使其更容易，因此您不必手动构造公式，并担心在表增长或新行或列时更改引用添加。

.. code:: python

 from xltable import *
 import pandas as pd
 
 # create a dataframe with three columns where the last is the sum of the first two
 dataframe = pd.DataFrame({
        'col_1': [1, 2, 3],
        'col_2': [4, 5, 6],
        'col_3': Cell('col_1') + Cell('col_2'),
    }, columns=['col_1', 'col_2', 'col_3'])
 
 # create the named xltable Table instance
 table = Table('table', dataframe)
 
 # create the Workbook and Worksheet objects and add table to the sheet
 sheet = Worksheet('Sheet1')
 sheet.add_table(table)
 
 workbook = Workbook('example.xlsx')
 workbook.add_sheet(sheet)
 
 # write the workbook to the file using xlsxwriter
 workbook.to_xlsx()
 
XLTable可以使用XlsxWriter编写xlsx文件，也可以使用pywin32（win32com）直接写入打开的Excel应用程序（仅限Windows）。直接写入Excel有利于交互式报告。例如，您可以在Excel功能区中使用一个按钮，用户可以按此按钮查询某些数据并生成报告。通过将其直接写入Excel，他们可以立即在Excel中获取该报告，而无需先将其写入文件。有关如何在Excel中自定义Excel功能区的详细信息，请参阅PyXLL：`自定义功能区 <https://www.pyxll.com/docs/userguide/ribbon.html>`_ 。

- `XLTable官方文档 <http://xltable.readthedocs.io/>`_

Pandas
,,,,,,,

为了处理数据范围并将它们读取或写入没有多余装饰的Excel工作簿，使用pandas可以是一种非常快速有效的方法。如果您不需要太多的格式化，只关心将数据导入或导出Excel工作簿，那么pandas函数“read_excel”和“to_excel”可能正是您所需要的。

.. code:: python

 df = pd.DataFrame([
        ('string1', 1),
        ('string2', 2),
        ('string3', 3)
    ], columns=['Name', 'Value'])
 
 # Write dataframe to an xlsx file
 df.to_excel('tmp.xlsx')
 
对于更复杂的任务，因为XlsxWriter，OpenPyXL和XLTable都具有Pandas集成，其中任何一个也可用于将Pandas DataFrames写入Excel。但是，如上所述直接使用Pandas将数据导入Excel非常方便。

xlrd/xlwt
,,,,,,,,,,

xlrd和xlwt分别读取和写入旧的Excel .xls文件。这些包含在此列表中是为了完整性，但现在实际上仅在您被迫处理遗留xls文件格式时使用。它们都非常成熟，非常强大且稳定，但xlwt永远不会扩展为支持更新的xlsx / xlsm文件格式，因此对于处理现代Excel文件格式的新代码，它们不再是最佳选择。

- `xlrd文档 <http://xlrd.readthedocs.io/>`_
- `xlwt文档 <http://xlwt.readthedocs.io/>`_
