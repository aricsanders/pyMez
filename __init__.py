"""
pyMeasure is an open source package for scientific data handling, analysis and acquisition. By loading the pyMeasure
package with the from pyMeasure import * style, the user gets the designed API with finished functionality. The
pyMeasure library itself has other helper modules that are directly accessible by importing them in the standard
fashion (from pyMeasure.Code.Subpackage.Module import class_or_function). For optimization purposes the pyMeasure
package importer (this file) has a constant VERBOSE_IMPORT = True that prints a list of each of the packages as it is
imported. To change the imported API, change the import statements in this __init__.py file.
Designed by Aric Sanders 2016

 Examples
--------
    #!python
    >>from pyMeasure import *
    >>test_AdvancedInterfaceFrame()

 <h3><a href="../../../Examples/html/Examples_Home.html">All Examples</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [lxml](http://lxml.de/)
+ [types](https://docs.python.org/2/library/types.html)
+ [pyMeasure](https://github.com/aricsanders/pyMeasure)
+ [xml](https://docs.python.org/2/library/xml.html)
+ [datetime](https://docs.python.org/2/library/datetime.html)
+ [urlparse](https://docs.python.org/2/library/urlparse.html)
+ [socket](https://docs.python.org/2/library/socket.html)
+ [fnmatch](https://docs.python.org/2/library/fnmatch.html)
+ [wx](https://wxpython.org/)
+ [pandas](http://pandas.pydata.org/)
+ [scipy](http://www.scipy.org/)
+ [visa](https://pyvisa.readthedocs.io/en/stable/)

Help
---------------
<a href="./index.html">`pyMeasure.Code.DataHandlers`</a>
<div>
<a href="../pyMeasure_Documentation.html">Documentation Home</a> |
<a href="./index.html">API Documentation Home</a> |
<a href="../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../Reference_Index.html">Index</a>
</div>

"""


import os
import sys
VERBOSE_IMPORT=True
"Constant that determines if import statements are echoed to output"
# This makes sure this file is the one loaded
sys.path.append(os.path.dirname( __file__ ))
# To tune the imported API change the modules imported
if VERBOSE_IMPORT:print("Importing {0}".format("Code.Utils.Names"))
from Code.Utils.Names import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.NISTModels"))
from Code.DataHandlers.NISTModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.GeneralModels"))
from Code.DataHandlers.GeneralModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.TouchstoneModels"))
from Code.DataHandlers.TouchstoneModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.XMLModels"))
from Code.DataHandlers.XMLModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.RadiCALModels"))
from Code.DataHandlers.RadiCALModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.ZipModels"))
from Code.DataHandlers.ZipModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.Translations"))
from Code.DataHandlers.Translations import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.StatistiCALModels"))
from Code.DataHandlers.StatistiCALModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.DataHandlers.MUFModels"))
from Code.DataHandlers.MUFModels import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.Analysis.SParameter"))
from Code.Analysis.SParameter import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.Analysis.Uncertainty"))
from Code.Analysis.Uncertainty import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.InstrumentControl.Instruments"))
from Code.InstrumentControl.Instruments import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.InstrumentControl.Experiments"))
from Code.InstrumentControl.Experiments import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.FrontEnds.AdvancedInterfaceFrame"))
from pyMeasure.Code.FrontEnds.AdvancedInterfaceFrame import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.FrontEnds.ShellPanel"))
from pyMeasure.Code.FrontEnds.ShellPanel import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.FrontEnds.IEPanel"))
from pyMeasure.Code.FrontEnds.IEPanel import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.FrontEnds.MatplotlibWxPanel"))
from pyMeasure.Code.FrontEnds.MatplotlibWxPanel import *

# __all__=["Code"]