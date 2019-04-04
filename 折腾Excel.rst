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

