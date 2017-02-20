"""
<a href="../index.html">`pyMeasure`</a>

<div>
<a href="../../pyMeasure_Documentation.html">Documentation Home</a> |
<a href="../index.html">API Documentation Home</a> |
<a href="../../Reference_Index.html">Index of all Functions and Classes in pyMeasure</a>
</div>

 Code is  the package designed as the top level of python code for pyMeasure. To reduce the burden of the
 importing of all subpackages/modules in pyMeasure internal code uses this as the starting place for the import. For
 example, in a module in the DataHandlers subpackage, first you import the os and sys packages.
 import os
 import sys

 then you add the code folder to the python path with

 sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))

 or the second package above the module itself. By doing this you can now import another module from pyMeasure
 such as Code.Utils.Names without going through the pyMeasure __init__.py file that determines the full API. For helper
 functions that do not need all of pyMeasure this greatly speeds their standalone performance.
"""
