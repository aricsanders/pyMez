#-----------------------------------------------------------------------------
# Name:        MUFModels
# Purpose:     A module that holds the models associated with the Microwave Uncertainty Framework
# Author:      Aric Sanders
# Created:     3/31/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A module that holds the models associated with the Microwave Uncertainty Framework.
Most models are xml based. Has an interface for running .net as scripts

Examples
--------
    #!python
    >>vna_uncert=MUFVNAUncert("MyUncertaintyMenu.VNAUncert")
    >>vna_uncert.get_results_directory()

 <h3><a href="../../../Examples/Html/MUFModels_Example.html">MUFModels Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [types](https://docs.python.org/2/library/types.html)
+ [pyMez](https://github.com/aricsanders/pyMez)
+ [pythonnet][https://github.com/pythonnet/pythonnet]


Help
---------------
<a href="./index.html">`pyMez.Code.DataHandlers`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys
import os
import datetime
from types import *
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.XMLModels import *
except:
    print("The module pyMez.Code.DataHandlers.XMLModels was not found,"
          "please put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.GeneralModels import *
except:
    print("The module pyMez.Code.DataHandlers.XMLModels was not found,"
          "please put it on the python path")
    raise ImportError
try:
    import clr
    CLR=True
except:
    print("The module clr had an error or was not found. Please check that it is on the path and "
          "working properly")
    CLR=False
try:
    import matplotlib.pyplot as plt
except:
    print("The module matplotlib had an error or was not found. Please check that it is on the path and "
          "working properly")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
SCRIPTABLE_MUF_LOCATION=r"C:\Share\MUF-develop\VNAUncertainty\bin\Debug"
"""Location of the MUF executable with modifications to make it scriptable."""
MODEL_UNIT_LIST=["Unitless","cm","mm","um","GHz","pf","nH","ohm","mho","pf/cm","ns","ps","mV","mA"]
MODEL_DISTRIBUTION_LIST=["Rectangular","Arc-sine","Bernoulli (binary)","Gaussain",
                         "2-D Uniform-Distribution Radius","2-D Gaussian-Distribution Radius"]

#-----------------------------------------------------------------------------
# Module Functions
def make_parameter_table(parameter_directory):
    """Creates a table from all the parameters in the parameter_directory, returns an AsciiDataTable"""
    file_names=os.listdir(parameter_directory)
    parameter_files=[]
    for file_name in file_names:
        extension = file_name.split(".")[-1]
        if re.search("parameter",extension,re.IGNORECASE) and extension not in ["parameterviewer"] :
            parameter_files.append(os.path.join(parameter_directory,file_name))
    #print("{0} is {1}".format("parameter_files",parameter_files))
    parameter_models=[MUFParameter(file_name) for file_name in parameter_files]
    column_names=["Parameter_Name","Value","Distribution_Type","Width","Standard_Uncertainty","Units"]
    data=[]
    for index,parameter in enumerate(parameter_models):
        print(("Parameter Number: {0}, Name:{1}".format(index,parameter.get_mechanism_name()) ))
        row=[os.path.split(parameter.get_mechanism_name())[-1].split(".")[0],
             parameter.get_value(),parameter.get_distribution_type(),
             parameter.get_distribution_width(),parameter.get_standard_uncertainty(),
             parameter.get_units()]
        data.append(row)
    data_table=AsciiDataTable(column_names=column_names,data=data)
    return data_table



#-----------------------------------------------------------------------------
# Module Classes
class MUFParameter(XMLBase):
    def get_value(self):
        """Returns the value of the parameter"""
        mechanism_value=self.etree.findall(".//MechanismValue")[0]
        value=mechanism_value.attrib["ControlText"]
        return float(value)

    def set_value(self,value):
        """Sets the value (center of distribution)"""
        mechanism_value=self.etree.findall(".//MechanismValue")[0]
        mechanism_value.attrib["ControlText"]=str(value)
        self.update_document()

    def get_distribution_type(self):
        """Returns the type of Distribution. The choices are held in  DistributionType/Item."""
        distribution_type=self.etree.findall(".//DistributionType")[0]
        text=distribution_type.attrib["ControlText"]
        return text

    def set_distribution_type(self,distribution_type):
        """Sets the distribution type, accepts an integer or text value.
        See the constant MODEL_DISTRIBUTION_LIST for possibilities. Rectangular is 0, Gaussian is 3. """
        if type(distribution_type) in [IntType,FloatType]:
            type_number=distribution_type
            type_name=MODEL_DISTRIBUTION_LIST[distribution_type]
        elif distribution_type in MODEL_DISTRIBUTION_LIST:
            type_number=MODEL_DISTRIBUTION_LIST.index(distribution_type)
            type_name=distribution_type
        else:
            print(("Could not set the type {0} please choose a"
                  " type or index from {1}".format(distribution_type,MODEL_DISTRIBUTION_LIST)))
            return
        distribution_type_tag = self.etree.findall(".//DistributionType")[0]
        distribution_type_tag.attrib["ControlText"]=type_name
        distribution_type_tag.attrib["SelectedIndex"]=type_number
        self.update_document()

    def get_distribution_width(self):
        """Returns the wdith of the distribution."""
        distribution_width=self.etree.findall(".//DistributionLimits")[0]
        text=distribution_width.attrib["ControlText"]
        return text

    def set_distribution_width(self,distribution_width):
        """Sets the distribution width"""
        distribution_width = self.etree.findall(".//DistributionLimits")[0]
        distribution_width.attrib["ControlText"]=str(distribution_width)
        self.update_document()

    def get_units(self):
        """Returns the units of the parameter"""
        units=self.etree.findall(".//Units")[0]
        text=units.attrib["ControlText"]
        return text

    def set_units(self,units):
        """Sets the units of the parameter can accept either an index or value. Look at
        MODEL_UNIT_LIST for complete set of possibilities"""
        if type(units) in [IntType,FloatType]:
            unit_number=units
            unit_name=MODEL_DISTRIBUTION_LIST[units]
        elif units in MODEL_DISTRIBUTION_LIST:
            unit_number=MODEL_DISTRIBUTION_LIST.index(units)
            unit_name=units
        else:
            print(("Could not set the units {0} please choose a"
                  " type or index from {1}".format(units,MODEL_UNIT_LIST)))
            return
        unit_tag = self.etree.findall(".//Units")[0]
        unit_tag.attrib["ControlText"]=unit_name
        unit_tag.attrib["SelectedIndex"]=unit_number
        self.update_document()

    def get_mechanism_name(self):
        """Returns the mechanism name"""
        units=self.etree.findall(".//MechanismName")[0]
        text=units.attrib["ControlText"]
        return text

    def get_standard_uncertainty(self):
        """returns the standard uncertainty of the parameter"""
        uncertainty=self.etree.findall(".//StandardUncertainty")[0]
        text = uncertainty.attrib["ControlText"]
        number=float(text.split(":")[-1])
        return number


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
        names=[x.attrib["Text"] for x in self.etree.findall(".//DUTMeasurements/Item/SubItem[@Index='0']")]
        locations=[x.attrib["Text"] for x in self.etree.findall(".//DUTMeasurements/Item/SubItem[@Index='1']")]
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
        self.update_document()

class MUFMeasurement(XMLBase):
    def get_name_parameter_dictionary(self):
        """Returns a dictionary of 'name':'parameter_name' pairs to correlate covariance files with their
        mechanism names"""
        out_dictionary={}
        try:
            names=[x.attrib["Text"] for x in self.etree.findall(".//PerturbedSParams/Item/SubItem[@Index='0']")]
            mechanisms=[x.attrib["Text"] for x in self.etree.findall(".//PerturbedSParams/Item/SubItem[@Index='2']")]
            for index,name in enumerate(names):
                split_parameter_name=os.path.split(mechanisms[index])[-1]
                parameter_name=split_parameter_name.split(".")[0]
                out_dictionary[name]=parameter_name
            return out_dictionary
        except:
            print("Could not retrieve the name - parameter dictionary")
            pass

    def get_covariance_dictionary(self):
        """Returns a list of dictionaries that has the keys name, location, and parameter_location"""
        covariance_list=[]
        try:
            names=[x.attrib["Text"] for x in self.etree.findall(".//PerturbedSParams/Item/SubItem[@Index='0']")]
            locations=[x.attrib["Text"] for x in self.etree.findall(".//PerturbedSParams/Item/SubItem[@Index='1']")]
            mechanisms = [x.attrib["Text"] for x in self.etree.findall(".//PerturbedSParams/Item/SubItem[@Index='2']")]
            for index,name in enumerate(names):
                name_location_dictionary={"name":name,"location":locations[index],"parameter_location":mechanisms[index]}
                covariance_list.append(name_location_dictionary)
            return covariance_list
        except:
            print("Could not retrieve the covariance dictionary")
            pass

    def get_montecarlo_dictionary(self):
        """Returns a list of dictionaries that has the keys name, location"""
        montecarlo_list=[]
        try:
            names=[x.attrib["Text"] for x in self.etree.findall(".//MonteCarloPerturbedSParams/Item/SubItem[@Index='0']")]
            locations=[x.attrib["Text"] for x in self.etree.findall(".//MonteCarloPerturbedSParams/Item/SubItem[@Index='1']")]
            for index,name in enumerate(names):
                name_location_dictionary={"name":name,"location":locations[index]}
                montecarlo_list.append(name_location_dictionary)
            return montecarlo_list
        except:
            print("Could not retrieve the montecarlo dictionary")
            pass

    def get_nominal_dictionary(self):
        "Returns a single dictionary with nominal name and location"
        nominal_dictionary={}
        try:
            location=map(lambda x: x.attrib["Text"],
                      self.etree.findall(".//MeasSParams/Item/SubItem[@Index='1']"))[0]
            name=os.path.split(location)[-1].split(".")[0]
            nominal_dictionary["location"]=location
            nominal_dictionary["name"]=name
            return nominal_dictionary
        except:
            print("Could not get nominal path information")
            pass







class MUFVNAUncertArchive(XMLBase):
    pass

class MUFSolution(XMLBase):
    pass


class MUFComplexModel(AsciiDataTable):
    """MUFComplexModel is built for the .complex files used in eps etc """

    def __init__(self, file_path, **options):
        """Initializes the class MUFComplexModel"""
        defaults = {"data_delimiter": "\t", "column_names_delimiter": ",", "specific_descriptor": 'Complex',
                    "general_descriptor": 'EPS', "extension": 'complex', "comment_begin": "!", "comment_end": "\n",
                    "header": None,
                    "column_names": ["Frequency", "re", "im"],
                    "column_names_begin_token": "!", "column_names_end_token": "\n", "data": None,
                    "row_formatter_string": None, "data_table_element_separator": None, "row_begin_token": None,
                    "row_end_token": None, "escape_character": None,
                    "data_begin_token": None, "data_end_token": None,
                    "column_types": ['float' for i in range(len(["Frequency", "re", "im"]))]
                    }
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        if file_path is not None:
            self.path = file_path
            self.__read_and_fix__()
        AsciiDataTable.__init__(self, None, **self.options)
        if file_path is not None:
            self.path = file_path

    def __read_and_fix__(self):
        """Reads in the data and fixes any problems with delimiters, etc"""
        in_file = open(self.path, 'r')
        lines = []
        for line in in_file:
            lines.append([float(x) for x in line.split("\t")])
        in_file.close()
        self.options["data"] = lines
        self.complex_data = []
        for row in self.options["data"]:
            frequency = [row[0]]
            complex_numbers = row[1:]
            # print np.array(complex_numbers[1::2])
            complex_array = np.array(complex_numbers[0::2]) + 1.j * np.array(complex_numbers[1::2])
            self.complex_data.append(frequency + complex_array.tolist())

    def get_variation_parameter(self):
        try:
            re_data = self["re"][:]
            re_data_var = [re_data[i + 2] - 2.0 * re_data[i + 1] + re_data[i] for i in range(len(re_data) - 2)]
            self.variation_parameter = 100 * max([abs(x) for x in re_data_var])
        except:
            raise
            self.variation_parameter = 0
        return self.variation_parameter

    def get_re_std(self):
        return np.std(self["re"])

    def get_re_mean(self):
        return np.mean(self["re"])

    def get_re_max(self):
        return np.max(self["re"])

    def show(self, **options):
        fig, ax1 = plt.subplots()
        ax1.plot(self["Frequency"], self["re"], 'b-')
        ax1.set_xlabel('Frequency (GHz)')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Real', color='b')
        ax1.tick_params('y', colors='b')

        ax2 = ax1.twinx()
        ax2.plot(self["Frequency"], self["im"], 'r-')
        ax2.set_ylabel('Imaginary', color='r')
        ax2.tick_params('y', colors='r')

        fig.tight_layout()
        plt.show()


#-----------------------------------------------------------------------------
# Module Scripts
if CLR:
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
            print(("VNAUncertainty finished running  at {0}".format(stop)))
            print(("The script took {0} seconds to run".format(runtime.seconds)))


#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass