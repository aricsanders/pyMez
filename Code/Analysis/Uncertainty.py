#-----------------------------------------------------------------------------
# Name:        Uncertainty
# Purpose:    To hold general functions and classes related to uncertainty
# Author:      Aric Sanders
# Created:     11/9/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Uncertainty is a collection of general classes and functions that pertain to uncertainty calculations.
 For specific uncertainty calculations look for modules with a modifier in the name such as  NISTUncertainty.

  Examples
--------
    #!python
    >>test_standard_error()

 <h3><a href="../../../Examples/html/Uncertainty_Example.html">Uncertainty Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [math](https://docs.python.org/2/library/math.html)
+ [pyMez](https://github.com/aricsanders/pyMez)

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
import math
import re
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.NISTModels import *
except:
    print("Code.DataHandlers.NISTModels did not import correctly")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def normalized_error(value_1,value_2,uncertainty,expansion_factor=1):
    """normalized error returns the  scalar normalized error (delta value/ (expansion_factor*uncertainty))"""
    return (value_2-value_1)/(uncertainty*expansion_factor)
def normalized_error_test(value_1,value_2,uncertainty,expansion_factor=1):
    """normalized error returns true if the scalar normalized error (delta value/ (expansion_factor*uncertainty))
    is less than or equal to one"""
    if normalized_error(value_1,value_2,uncertainty,expansion_factor)<=1:
        return True
    else:
        return False

def standard_error(value_1,uncertainty_value_1,value_2,uncertainty_value_2=0,expansion_factor=2):
    """calculates the standard errror (delta value/ (expansion factor * Sqrt(ua^2+ub^2)))"""
    return abs((value_2-value_1))/(math.sqrt(uncertainty_value_1**2+uncertainty_value_2**2)*expansion_factor)

def standard_error_data_table(table_1,table_2,**options):
    """standard error data table takes two tables and creates a table that is the standard error of the two tables,
    at least one table must have uncertainties associated with it. The input tables are assumed to have data
    in the form [[x, y1, y2,...]..] Uncertainties can be specified as a column name in the respective
    table, fractional, constant, or a function of the values. The returned table is an object
    of the class StandardErrorModel(AsciiDataTable) that has data in the form
    [[independent_varaible,SEValue1,SEValue2...]...] where column names are formed by
    appending SE to the value column names. To plot the table use result.show()
    """
    defaults={}
    error_options={"independent_variable_column_name":"Frequency",
                  "value_column_names":['magS11','argS11','magS21',
                                                'argS21','magS22','argS22'],
                  "table_1_uncertainty_column_names":['uMgS11','uAgS11',
                                                      'uMgS21','uAgS21','uMgS22','uAgS22'],
                  "table_2_uncertainty_column_names":['uMgS11','uAgS11',
                                                      'uMgS21','uAgS21','uMgS22','uAgS22'],
                   "uncertainty_table_1":None,
                   "uncertainty_table_2":None,
                   "uncertainty_function_table_1":None,
                   "uncertainty_function_table_2":None,
                   "uncertainty_function":None,
                   "uncertainty_type":None,
                   "table_1_uncertainty_type":"table",
                   "table_2_uncertainty_type":None,
                   "expansion_factor":1,
                   'debug':False}

    for key,value in defaults.items():
        error_options[key]=value
    for key,value in options.items():
        error_options[key]=value
    # Begin by checking at least one table has an error associated with it
    if error_options["table_1_uncertainty_type"] is None and error_options["table_2_uncertainty_type"] is None:
        raise StandardErrorError("Undefined Error For Both Tables: Define at least one of "
                                 "table_1_uncertainty_type or table_2_uncertainty_type to be a value other than None")
    if error_options["expansion_factor"]:
        expansion_factor=float(error_options["expansion_factor"])
    else:
        expansion_factor=1
    # first find a unique list of the independent variable for both curves
    if error_options["debug"]:
        begin_time=datetime.datetime.utcnow()
        print(("started finding intersection of"
              "table_1[{0}] and table_2[{1}] at {2}".format(error_options["independent_variable_column_name"],
                                                           error_options["independent_variable_column_name"],
                                                           begin_time)))
    x_set_table_1=set(table_1[error_options["independent_variable_column_name"]])
    x_set_table_2=set(table_2[error_options["independent_variable_column_name"]])
    unique_x=sorted(list(x_set_table_1.intersection(x_set_table_2)))
    if error_options["debug"]:
        end_time=datetime.datetime.utcnow()
        print(("finished finding intersection at {0}".format(end_time)))
        delta_time=end_time-begin_time
        print(("it took {0} to find the intersection that contained {1} points".format(delta_time,len(unique_x))))
    if not unique_x:
        raise StandardErrorError("No points in the intersection, please either interpolate one data set or compare"
                                 "with another data set")

    # next build the new data set
    out_data=[]
    x_column_index_table_1=table_1.column_names.index(error_options["independent_variable_column_name"])
    x_column_index_table_2=table_2.column_names.index(error_options["independent_variable_column_name"])
    # we choose the row by using unique_x
    for x_value in unique_x:
        # here if there are multiple values for x_value we ignore them
        table_1_row=list(filter(lambda x: x[x_column_index_table_1]==x_value,table_1.data))[0]
        # we begin a new_row
        table_2_rows=[x for x in table_2.data if x[x_column_index_table_2]==x_value]
        if error_options["debug"]:
            print(("{0} is {1}".format("table_2_rows",table_2_rows)))
        for table_2_row in table_2_rows:
            new_row=[x_value]
            for column_index,column_name in enumerate(error_options["value_column_names"]):
                value_1_column_selector=table_1.column_names.index(column_name)
                value_2_column_selector=table_2.column_names.index(column_name)
                value_1=table_1_row[value_1_column_selector]
                value_2=table_2_row[value_2_column_selector]
                # now we assign the error to value 1
                if error_options["table_1_uncertainty_type"] is None:
                    error_1=0
                elif re.search("table|list",error_options["table_1_uncertainty_type"],re.IGNORECASE):
                    error_1_column_selector=table_1.column_names.index(error_options["table_1_uncertainty_column_names"][column_index])
                    error_1=table_1_row[error_1_column_selector]
                elif re.search("con|fixed",error_options["table_1_uncertainty_type"],re.IGNORECASE):
                    error_1=float(error_options["uncertainty_table_1"])
                elif re.search("fract",error_options["table_1_uncertainty_type"],re.IGNORECASE):
                    error_1=float(error_options["uncertainty_table_1"])*value_1
                elif re.search("func",error_options["table_1_uncertainty_type"],re.IGNORECASE):
                    error_1=error_options["uncertainty_table_1_function"](value_1)
                else:
                    error_1=0
                # now the same for table 2
                if error_options["table_2_uncertainty_type"] is None:
                    error_2=0
                elif re.search("table|list",error_options["table_2_uncertainty_type"],re.IGNORECASE):
                    error_2_column_selector=table_2.column_names.index(error_options["table_2_uncertainty_column_names"][column_index])
                    error_2=table_2_row[error_2_column_selector]
                elif re.search("con|fixed",error_options["table_2_uncertainty_type"],re.IGNORECASE):
                    error_2=float(error_options["uncertainty_table_2"])
                elif re.search("fract",error_options["table_2_uncertainty_type"],re.IGNORECASE):
                    error_2=float(error_options["uncertainty_table_2"])*value_2
                elif re.search("func",error_options["table_2_uncertainty_type"],re.IGNORECASE):
                    error_2=error_options["uncertainty_table_2_function"](value_2)
                else:
                    error_2=0
                # now calculate the value and append
                try:
                    standard_error=(value_1-value_2)/(expansion_factor*math.sqrt(error_1**2+error_2**2))
                except:
                    standard_error=0
                new_row.append(standard_error)
            out_data.append(new_row)
        # now we handle the standard error table creation
    standard_error_column_names=[error_options["independent_variable_column_name"]]
    for column_name in error_options["value_column_names"]:
        standard_error_column_names.append("SE"+column_name)
    error_options["column_names"]=standard_error_column_names[:]
    if error_options["debug"]:
        print(("{0} is {1}".format("standard_error_column_names",standard_error_column_names)))
        print(("{0} is {1}".format("out_data",out_data)))
    error_options["column_types"]=['float' for column in  standard_error_column_names[:]]
    error_options["data"]=out_data[:]
    out_table=StandardErrorModel(None,**error_options)
    return out_table



#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_standard_error(test_list=None):
    """Tests the standard error function using a test_list=[first_value,first_error,
    second_value,second_error]"""
    if test_list is None:
        [first_value,first_error,second_value,second_error]=[2.75,.1,3.45,.2]
    print(("The 1st value is {0}, with an uncertainty of {1}".format(first_value,first_error)))
    print(("The 2nd value is {0}, with an uncertainty of {1}".format(second_value, second_error)))
    print(("The standard_error is {0}".format(standard_error(first_value,
                                                            first_error,
                                                            second_value,second_error))))
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    