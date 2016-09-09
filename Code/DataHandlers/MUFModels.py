#-----------------------------------------------------------------------------
# Name:        MUFModels
# Purpose:     A module that holds the models associated with the Microwave Uncertainty Framework
# Author:      Aric Sanders
# Created:     3/31/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A module that holds the models associated with the Microwave Uncertainty Framework.
Most models are xml based"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.XMLModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.XMLModels was not found,"
          "please put it on the python path")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class MUFParameter(XMLBase):
    pass
class MUFModel(XMLBase):
    pass
class MUFVNAUncert(XMLBase):
    pass
class MUFVNAUncertArchive(XMLBase):
    pass
class MUFMeasurement(XMLBase):
    pass
class MUFSolution(XMLBase):
    pass

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass