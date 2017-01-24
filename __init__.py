"""pyMeasure is an open source package for scientific data handling, analysis and acquisition. By loading the pyMeasure
package with the from pyMeasure import *, the user gets the designed API with finished functionality. The
pyMeasure library itself has other helper modules that are directly accessible by importing them in the standard
fashion (from pyMeasure.Code.Subpackage.Module import class_or_function. For optimization purposes the pyMeasure
package importer (this file) has a constant VERBOSE_IMPORT = True that prints a list of each of the packages as it is
imported.
Designed by Aric Sanders 2016
"""
#TODO: Fix any circular imports, I am not sure if __all__ is the right way to do this
# It appears any import of pyMeasure. causes this file to execute, creating a circular import
import os
import sys
VERBOSE_IMPORT=True
sys.path.append(os.path.dirname( __file__ ))
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
if VERBOSE_IMPORT:print("Importing {0}".format("Code.InstrumentControl.Instruments"))
from Code.InstrumentControl.Instruments import *
if VERBOSE_IMPORT:print("Importing {0}".format("Code.InstrumentControl.Experiments"))
from Code.InstrumentControl.Experiments import *
#from pyMeasure.Code.FrontEnds import AdvancedInterfaceFrame



# __all__=["Code"]