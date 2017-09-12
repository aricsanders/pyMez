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

    def get_standard_measurement_locations(self):
        """Returns the file locations for the measurement of the standards in a form of a list"""
        standards = self.etree.findall(".//BeforeCalibration/Item/SubItem[@Index='6']")
        locations=[standard.attrib["Text"] for standard in standards]
        return locations

    def set_standard_location(self,standard_location=None,standard_number=1):
        """Sets the location for the measurement of standard_number"""
        standards = self.etree.findall(".//BeforeCalibration/Item/SubItem[@Index='6']")
        standard=standards[standard_number-1]
        standard.attrib["Text"]=standard_location
        self.update_document()

    def get_number_montecarlo(self):
        "Returns the number of montecarlo simulations"
        montecarlo_text_box=self.etree.findall(".//MenuStripTextBoxes/NumberMonteCarloSimulations")[0]
        number_montecarlo=montecarlo_text_box.attrib["Text"]
        return number_montecarlo

    def set_number_montecarlo(self,number_montecarlo=100):
        """Sets the number of montecarlo trials for the menu"""
        montecarlo_text_box = self.etree.findall(".//MenuStripTextBoxes/NumberMonteCarloSimulations")[0]
        montecarlo_text_box.attrib["Text"]=str(number_montecarlo)
        self.update_document()

    def get_DUTs(self):
        "Returns the names and locations of DUTs"
        duts=[]
        names=map(lambda x: x.attrib["Text"],self.etree.findall(".//DUTMeasurements/Item/SubItem[@Index='0']"))
        locations=map(lambda x: x.attrib["Text"],self.etree.findall(".//DUTMeasurements/Item/SubItem[@Index='1']"))
        for index,name in enumerate(names):
            name_location_dictionary={"name":name,"location":locations[index]}
            duts.append(name_location_dictionary)
        return duts

    def add_DUT(self,location,name=None):
        """Adds a DUT to the DUTMeasurements element"""
        # get the name
        if name is None:
            name=os.path.basename(location).split(".")[0]
        # first get the DUTMeasurement element
        dut_measurement=self.etree.findall(".//DUTMeasurements")[0]
        # next add one to the count attribute
        number_standards=int(dut_measurement.attrib["Count"])
        number_standards+=1
        dut_measurement.attrib["Count"]=str(number_standards)
        # create a Item
        item=etree.SubElement(dut_measurement,"Item",attrib={"Count":"2","Index":str(number_standards),"Text":name})
        etree.SubElement(item,"SubItem",attrib={"Index":"0","Text":name})
        etree.SubElement(item,"SubItem",attrib={"Index":"1","Text":location})
        self.update_document()

    def clear_DUTs(self):
        """Removes all DUTs"""
        dut_measurement = self.etree.findall(".//DUTMeasurements")[0]
        items= self.etree.findall(".//DUTMeasurements/Item")
        for item in items:
            dut_measurement.remove(item)










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
    vna.OnLocationChanged(event)
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