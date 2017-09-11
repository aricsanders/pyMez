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
import datetime
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
    def get_results_directory(self):
        "Returns the results directory"
        results_directory=self.etree.findall(".//MenuStripTextBoxes/ResultsDirectory")[0].attrib["Text"]
        return results_directory

    def set_results_directory(self,directory=None):
        "Sets the results directory, default is the current working directory"
        if directory is None:
            directory=os.getcwd()
        results_directory = self.document.getElementsByTagName("ResultsDirectory")[0]
        results_directory.setAttribute(attname="Text", value=directory)
        check_box=self.document.getElementsByTagName("SelectResultsDirectoryToolStripMenuItem")[0]
        check_box.setAttribute(attname="Checked", value="True")
        self.update_etree()

    def get_number_standards(self):
        "Returns the number of calibration standards in the before calibration"
        sub_items = self.etree.findall(".//BeforeCalibration/Item")
        return len(sub_items)

    def get_standard_definition(self,standard_number=1):
        "Returns the xml definition of the standard in position standard_number"
        sub_items = self.etree.findall(".//BeforeCalibration/Item")
        return etree.tostring(sub_items[standard_number-1])

    def set_standard_location(self,standard_location=None,standard_number=1):
        """Sets the location for the measurement of standard_number"""
        pass



class MUFVNAUncertArchive(XMLBase):
    pass
class MUFMeasurement(XMLBase):
    pass
class MUFSolution(XMLBase):
    pass

#-----------------------------------------------------------------------------
# Module Scripts
def run_muf_script(menu_location,timeit=True):
    """Opens a vnauncert or vnauncert_archive and runs it as is."""

    start=datetime.datetime.utcnow()
    sys.path.append(SCRIPTABLE_MUF_LOCATION)
    clr.AddReference("VNAUncertainty")
    import VNAUncertainty
    from System import EventArgs, Object
    event=EventArgs()
    vna =VNAUncertainty.VNAUncertainty()
    vna.OnLoad(event)
    vna.myOpenMenu(menu_location)
    vna.UpdateResultsDirectory(True)
    vna.RunCalibration(0)
    vna.Close()
    if timeit:
        stop=datetime.datetime.utcnow()
        runtime=stop-start
        print("VNAUncertainty finished running  at {0}".format(stop))
        print("The script took {0} seconds to run".format(runtime.seconds))


#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass