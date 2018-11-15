"""
pyMez is an open source package for scientific data handling, analysis and acquisition. By loading the pyMez
package with the from pyMez import * style, the user gets the designed API with finished functionality. The
pyMez library itself has other helper modules that are directly accessible by importing them in the standard
fashion (from pyMez.Code.Subpackage.Module import class_or_function). For clarity purposes the pyMez
package importer (this file) has a constant VERBOSE_IMPORT = True that prints a list of each of the packages as it is
imported. To change the imported API, change the dictionary API_MODULES to have an entry
API_MODULE["Code.Subpackage.Module"]=True
 in this __init__.py file.
Designed by Aric Sanders 2016

 Examples
--------
    #!python
    >>from pyMez import *
    >>test_AdvancedInterfaceFrame()

 <h3><a href="../Examples/html/Examples_Home.html">All Examples</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [lxml](http://lxml.de/)
+ [types](https://docs.python.org/2/library/types.html)
+ [pyMez](https://github.com/aricsanders/pyMez)
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
<div>
<a href="../pyMez_Documentation.html">Documentation Home</a> |
<a href="./index.html">API Documentation Home</a> |
<a href="../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../Reference_Index.html">Index</a>
</div>

"""


import os
import sys
VERBOSE_IMPORT=True
TIMED_IMPORT=True

"Constant that determines if import statements are echoed to output"
# control the modules loaded in the API, this should be included in a pyMez Settings file
# The new module load scheme can be for module in API_MODULES.keys()
API_MODULES={"Code.Utils.Names":True,
             "Code.Utils.Alias":False,
             "Code.Utils.DjangoUtils":False,
             "Code.Utils.GetMetadata":False,
             "Code.Utils.HelpUtils":False,
             "Code.Utils.HPBasicUtils":False,
             "Code.Utils.PerformanceUtils":False,
             "Code.Utils.pyMezUnitTest":False,
             "Code.DataHandlers.AbstractDjangoModels":False,
             "Code.DataHandlers.GeneralModels":True,
             "Code.DataHandlers.GraphModels":False,
             "Code.DataHandlers.HTMLModels":True,
             "Code.DataHandlers.MUFModels":False,
             "Code.DataHandlers.NISTModels":True,
             "Code.DataHandlers.RadiCALModels":False,
             "Code.DataHandlers.StatistiCALModels":False,
             "Code.DataHandlers.TouchstoneModels":True,
             "Code.DataHandlers.Translations":False,
             "Code.DataHandlers.XMLModels":True,
             "Code.DataHandlers.ZipModels":True,
             "Code.Analysis.Fitting":False,
             "Code.Analysis.Interpolation":False,
             "Code.Analysis.NISTUncertainty":False,
             "Code.Analysis.Reports":False,
             "Code.Analysis.SParameter":False,
             "Code.Analysis.Transformations":False,
             "Code.Analysis.Uncertainty":False,
             "Code.Analysis.GeneralAnalysis":False,
             "Code.InstrumentControl.Instruments":True,
             "Code.InstrumentControl.Experiments":True,
             "Code.FrontEnds.AdvancedInterfaceFrame":False,
             "Code.FrontEnds.BasicInterfaceFrame":False,
             "Code.FrontEnds.EndOfDayDialog":False,
             "Code.FrontEnds.GeneralInterfaceFrame":False,
             "Code.FrontEnds.HTMLPanel":False,
             "Code.FrontEnds.IEPanel":False,
             "Code.FrontEnds.IPythonPanel":False,
             "Code.FrontEnds.KeithleyIVPanel":False,
             "Code.FrontEnds.MatplotlibWxPanel":False,
             "Code.FrontEnds.ShellPanel":False,
             "Code.FrontEnds.SimpleArbDBLowerInterfacePanel":False,
             "Code.FrontEnds.SimpleLogLowerInterfacePanel":False,
             "Code.FrontEnds.StyledTextCtrlPanel":False,
             "Code.FrontEnds.VisaDialog":False,
             "Code.FrontEnds.WxDialogFunctions":False,
             "Code.FrontEnds.WxHTML2Panel":False,
             "Code.FrontEnds.XMLEditPanel":False,
             "Code.FrontEnds.XMLGeneral":False
             }
"Dictionary that controls the definition of the API, this can be set to leave out any unwanted modules. Also it is" \
"possible to discover all modules by API_MODULES.keys()"

# This makes sure this file is the one loaded
sys.path.append(os.path.dirname( __file__ ))
# To tune the imported API change the API_MODULES dictionary
if TIMED_IMPORT:
    import datetime
    first_timer=datetime.datetime.utcnow()
    start_timer=datetime.datetime.utcnow()
print("Importing pyMez, this should take roughly 30 seconds")
for module in sorted(API_MODULES.keys()):
    if API_MODULES[module]:
        if VERBOSE_IMPORT:
            print(("Importing {0}".format(module)))
        exec('from {0} import *'.format(module))
        if TIMED_IMPORT:
            end_timer=datetime.datetime.utcnow()
            time_difference=end_timer-start_timer
            print(("It took {0} s to import {1}".format(time_difference.total_seconds(),module)))
            start_timer=end_timer
if TIMED_IMPORT:
    end_timer = datetime.datetime.utcnow()
    time_difference = end_timer - first_timer
    print(("It took {0} s to import all of the active modules".format(time_difference.total_seconds())))

