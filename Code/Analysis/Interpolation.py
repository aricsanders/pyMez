#-----------------------------------------------------------------------------
# Name:        Interpolation
# Purpose:     To hold functions and classes for interpolating data
# Author:      Aric Sanders
# Created:     9/9/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Interpolation holds classes and functions important for interpolating data.

  Examples
--------
    #!python
    >>test_interpolate()

 <h3><a href="../../../Examples/html/Interpolation_Example.html">Interpolation Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [types](https://docs.python.org/2/library/types.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [scipy](https://docs.scipy.org/doc/)


Help
---------------
<a href="./index.html">`pyMez.Code.Analysis`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>


 """

#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys
from types import *
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    import numpy as np
except:
    print("Numpy was not imported")
    raise
try:
    from scipy.interpolate import interp1d
except:
    print("The function scipy.interpolate.interp1d did not import properly,"
          "please check that scipy is on the python path and that it is not in an error state")
    raise
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def interpolate_data(data_list,**options):
    """interpolate data takes a list of data in [[x,y1,y2,..yn]..] format and
    returns a list of interpolation functions [f1(x),f2(x),f3(x)...fn(x)]"""
    out_list=[]
    # reorganize the list to [[x,..xm],[y,...ym]]
    vector_list=[]
    for index,column in enumerate(data_list[0]):
        vector=[row[index] for row in data_list]
        vector_list.append(vector)
    # now each function is interp1d of
    for vector in vector_list[1:]:
        f=interp1d(vector_list[0],vector,**options)
        out_list.append(f)
    return out_list

def build_interpolated_data_set(x_list,interpolated_function_list):
    """build_interpolated_data_set takes an input independent variable and a list
    of interpolation functions and returns a data set of the form [..[xi,f1(xi),..fn(xi)]]
    it is meant to create a synthetic data set after using interpolate_data"""
    out_data=[]
    for x in x_list:
        new_row=[]
        new_row.append(x)
        for function in interpolated_function_list:
            # to list is needed if the function returns np.array
            if type(function(x)) in [np.ndarray]:
                new_row.append(function(x).tolist())
            else:
                new_row.append(function(x))
        out_data.append(new_row)
    return out_data

def interpolate_table(table,independent_variable_list):
    """Returns a copy of the table interpolated to the independent variable list
    Assumes there is a single independent variable in the first column"""
    functions=interpolate_data(table.data)
    new_data=build_interpolated_data_set(independent_variable_list,functions)
    new_table=table.copy()
    new_table.data=new_data
    return new_table
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_interpolate(data_set=None):
    if data_set is None:
        data_set=[[i,i**2,i**3] for i in range(100)]
    interpolation_functions=interpolate_data(data_set)
    type_of_f=type(interpolation_functions[0](1))
    print(("The types of of the function results are {0}".format(type_of_f)))
    print(("type(f(x)) == numpy.ndarray is {0}".format(type_of_f in [np.ndarray,"<type 'numpy.ndarray'>"])))
    new_x=[i for i in range(100)]
    interpolated_data=build_interpolated_data_set(new_x,interpolation_functions)
    print("Testing interpolation of data set")
    print(("*"*80))
    print(("the old data set is {0} ".format(data_set)))
    print(("*"*80))
    print(("the new data set is {0}".format(interpolated_data)))
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_interpolate()
    test_interpolate(data_set=[[i,complex(2.2*i,2.5*i)] for i in range(0,200,2)])
