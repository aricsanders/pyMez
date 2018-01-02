"""
 Code is  the package designed as the top level of python code for pyMez. To reduce the burden of the
 importing of all subpackages/modules in pyMez internal code uses this as the starting place for the import. For
 example, in a module in the <a href="./DataHandlers">`DataHandlers subpackage</a>,
 first you import the os and sys packages.

    #!python
    import os
    import sys

 then you add the code folder to the python path with

    #!python
    sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))

 or the second package above the module itself. By doing this you can now import another module from pyMez
 such as Code.Utils.Names without going through the pyMez `__init__.py` file that determines the full API.
 For helper
 functions that do not need all of pyMez this greatly speeds their standalone performance.

Help
----
<a href="../index.html">`pyMez`</a>

<div>
<a href="../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../index.html">API Documentation Home</a> |
<a href="../../Examples/Html/Examples_Home.html">Examples</a> |
<a href="../../Reference_Index.html">Index</a>
</div>
"""
