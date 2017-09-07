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
try:
    import clr
except:
    print("The module clr had an error or was not found. Please check that it is on the path and "
          "working properly")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
SCRIPTABLE_MUF_LOCATION=r"C:\Share\MUF-develop\VNAUncertainty\bin\Debug"
"""Location of the MUF executable with modifications to make it scriptable."""
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
def run_muf_script(menu_location):
    """Opens a vnauncert or vnauncert_archive and runs it as is."""
    sys.path.append(SCRIPTABLE_MUF_LOCATION)
    clr.AddReference("VNAUncertainty")
    import VNAUncertainty
    from System import EventArgs, Object
    event=EventArgs()
    vna =VNAUncertainty.VNAUncertainty()
    vna.OnLoad(event)
    vna.myOpenMenu(menu_location)
    vna.RunCalibration(0)
    vna.Close()

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass