#-----------------------------------------------------------------------------
# Name:        RadiCALModels
# Purpose:     To handle output from the radiCAL program written by Nate Orloff
# Author:      Aric Sanders
# Created:     9/8/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Handles the data saved after running Radical to analyze data. The assumed
 format is .mat V7.3, if saved in the older format, resave by setting preferences
 in matlab Environment->Preferences->General->MAT-Files->V7.3. This stores the result
 as an hd5 file with a .mat extension. Previous versions of matlab can be handled using
 scipy.io.loadmat, but this module does not use this function
 Examples
--------
    #!python
    >>rad=RadicalDataModel("radical_datafile")
    >>rad.show()



Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [types](https://docs.python.org/2/library/types.html)
+ [pyMez](https://github.com/aricsanders/pyMez)
+ [h5py][http://www.h5py.org/]


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
import os
import sys
#-----------------------------------------------------------------------------
# Third Party Imports
# magic statement that injects the pyMez folder into sys.path
# This allows Code to be imported skipping pyMez/.__init__.py
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.TouchstoneModels import *
except:
    print("The module pyMez.Code.DataHandlers.TouchstoneModels was not found or had an error,"
          "please put it on the python path")
    raise
try:
    import h5py
except:
    print("The module h5py was not found or had an error,"
          "please put it on the python path or resolve the error. (pip install h5py)")
    raise

try:
    import numpy as np
except:
    print("The module numpy was not found or had an error,"
          "please put it on the python path or resolve the error. (pip install numpy)")
    raise
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def radical_dataset_to_s2p(radical_data_set,frequency_list,**options):
    """Takes a radical data set that is of the form <HDF5 dataset "S1": shape (4, 512), type "|V16"> and outputs
    an S2PV1 python model. Requires frequency_list=np.array(radical_data_file["RadiCalData/StatistiCalData/F"])[0].tolist()
    to be passed"""
    defaults={"frequency_selector":0,"frequency_column_name":"Frequency"}
    s2p_options={}
    for key,value in defaults.items():
        s2p_options[key]=value
    for key,value in options.items():
        s2p_options[key]=value
    input_data=np.array(radical_data_set)
    sparameters=[]
    for index,item in enumerate(frequency_list):
        [S11,S21,S12,S22]=[complex(input_data[0][index][0],input_data[0][index][1]),
                           complex(input_data[1][index][0],input_data[1][index][1]),
                           complex(input_data[2][index][0],input_data[2][index][1]),
                           complex(input_data[3][index][0],input_data[3][index][1])]
        new_row=[item,S11,S21,S12,S22]
        sparameters.append(new_row)
    new_s2p=S2PV1(None,sparameter_complex=sparameters,**s2p_options)
    return new_s2p


def radical_frequency_to_frequency_list(radical_frequency, radical_data_file=None):
    """Takes either the string specifying the radical frequency location ("RadiCalData/StatistiCalData/F") and
    radical data file
    or the data set radical_data_file["RadiCalData/StatistiCalData/F"] and returns a python list of frequencies"""
    try:
        if type(radical_frequency) in StringTypes:
            frequency_list = np.array(radical_data_file[radical_frequency])[0].tolist()
        elif type(radical_frequency) in [h5py._hl.dataset.Dataset]:
            frequency_list = np.array(radical_frequency)[0].tolist()
        elif type(radical_frequency) in [h5py._hl.files.File]:
            frequency_list = np.array(radical_frequency["RadiCalData/StatistiCalData/F"])[0].tolist()
    except:
        print(("Could not change {0} to a python list".format(radical_frequency)))


def radical_error_boxes_to_eight_term_complex(radical_s1, radical_s2, radical_frequency_list, radical_data_file=None):
    """Takes two radical error boxes and a frequency_list (in python format run radical_frequency_to_frequency_list first)
    and converts them into a python list structure
    [[f,S1_11,S1_12,S1_21,S1_22,S2_11,S2_12,S2_21,S_22]] where each component of a matrix is a complex number.
    This list is designed to be used as an input for correct_sparameters_eight_term"""
    try:
        # fist convert the S1 to a numpy array the dimensions are 4 x number of frequencies x 2
        if type(radical_s1) in StringTypes:
            s1_numpy_array = np.array(radical_data_file[radical_s1])
        elif type(radical_s1) in [h5py._hl.dataset.Dataset]:
            s1_numpy_array = np.array(radical_s1)
        elif type(radical_s1) in [np.ndarray]:
            s1_numpy_array = radical_s1
        else:
            raise TypeError("S1 is the wrong type")
        # second convert the S2 to a numpy array are 4 x number of frequencies x 2
        if type(radical_s2) in StringTypes:
            s2_numpy_array = np.array(radical_data_file[radical_s2])
        elif type(radical_s2) in [h5py._hl.dataset.Dataset]:
            s2_numpy_array = np.array(radical_s2)
        elif type(radical_s2) in [np.ndarray]:
            s2_numpy_array = radical_s2
        else:
            raise TypeError("S2 is the wrong type")
        # now arrange each item as complex()
        eight_term_complex_list = []
        for frequency_index, frequency in enumerate(radical_frequency_list):
            new_row = [frequency]
            s1_row = [s1_numpy_array[i][frequency_index] for i in range(len(s1_numpy_array))]
            s1_complex_row = [complex(x[0], x[1]) for x in s1_row]
            s2_row = [s2_numpy_array[i][frequency_index] for i in range(len(s2_numpy_array))]
            s2_complex_row = [complex(x[0], x[1]) for x in s2_row]
            new_row = new_row + s1_complex_row + s2_complex_row
            eight_term_complex_list.append(new_row)
        return eight_term_complex_list
    except:
        print("Could not convert the S1, S2 as given")
        raise

# Does this belong in HD5Models?
def print_hd5_keys(hd5_group):
    """Prints hd5 keys and passes if there are none"""
    try:
        print(hd5_group)
    except: pass

def return_hd5_keys(hd5_group):
    """Returns hd5 keys and passes if there are none"""
    keys=[]
    try:
        hd5_group.visit(lambda x:keys.append(x))
    except: pass
    return keys
#-----------------------------------------------------------------------------
# Module Classes
class RadicalDataModel():
    """RadicalDataModel is a container for data generated by the matlab program radical
    copyright 2011, Nathan Orloff. Typically the file is found in Radical_Solutions/RadicalData.mat or renamed"""
    def __init__(self,file_path=None,**options):
        defaults={}
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        if file_path is None:
            pass
        else:
            self.data_file=h5py.File(file_path,"r")
            # load the frequency list
            self.frequency_list=np.array(self.data_file["RadiCalData/StatistiCalData/F"])[0].tolist()
            # create some s2p file attributes for easy access
            self.uncorrected_short=radical_dataset_to_s2p(self.data_file["RadiCalData/StatistiCalData/S"],
                                                          self.frequency_list)
            self.uncorrected_Rs=radical_dataset_to_s2p(self.data_file["RadiCalData/StatistiCalData/Rs"],
                                                       self.frequency_list)
            self.corrected_Rs=radical_dataset_to_s2p(self.data_file["RadiCalData/Ref/TRL/Models/Rs"],
                                                       self.frequency_list)
            self.corrected_DUT=radical_dataset_to_s2p(self.data_file[self.data_file[np.array(self.data_file["RadiCalData/Dut/Calibrated"])[0][0]][0][0]],
                      self.frequency_list)
            self.propagation_constant=np.array(self.data_file["RadiCalData/Ref/TRL/PropConst"])
    def show(self):
        """Displays corrected DUT as s2p"""
        self.corrected_DUT.show()
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass