#-----------------------------------------------------------------------------
# Name:        GeneralAnalysis
# Purpose:    To hold functions and classes for general analysis tasks
# Author:      Aric Sanders
# Created:     7/27/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" GeneralAnalysis is a module containing classes and functions for general analytic tasks.

 Examples
--------


Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [types](https://docs.python.org/2/library/types.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [scipy](https://docs.scipy.org/doc/)
+ [sympy](http://www.sympy.org/en/index.html)

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
import re
import datetime
import sys
import cmath
import math
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    import numpy as np
except:
    np.ndarray='np.ndarray'
    print("Numpy was not imported")
    pass
try:
    import pandas
except:
    print("Pandas was not imported")
    pass
try:
    from scipy.stats.mstats import gmean
except:
    print("The function gmean from the package scipy.stats.mstats did not import correctly ")
try:
    from statsmodels.robust.scale import mad
except:
    print("The function mad from the package statsmodels.robust.scale did not import correctly ")
try:
    #Todo: this could lead to a cyclic dependency, it really should import only the models it analyzes
    #Todo: If analysis is to be in the top import, none of the models should rely on it
    #import pyMez.Code.DataHandlers.NISTModels
    from Code.DataHandlers.NISTModels import *
    from Code.DataHandlers.GeneralModels import *
    from Code.DataHandlers.Translations import *
    #from pyMez import *
except:
    print("The subpackage pyMez.Code.DataHandlers did not import properly,"
          "please check that it is on the python path and that unit tests passed")
    raise
try:
    import matplotlib.pyplot as plt
except:
    print("The module matplotlib was not found,"
          "please put it on the python path")
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def independent_variable_model_collapse(model,independent_column_name="Frequency", **options):
    """Returns a model with a single set of independent variables. Default is to average values together
    but geometric mean, std, variance, rss, mad and median are options.
    Geometric means of odd number of negative values fails"""
    if isinstance(model,pandas.DataFrame):
        model_1 = DataFrame_to_AsciiDataTable(model)
    defaults = {"method": "mean"}
    # load other options from model
    for option, value in model.options.items():
        if not re.search('begin_line|end_line', option):
            defaults[option] = value
    for element in model.elements:
        if model.__dict__[element]:
            if re.search("meta", element, re.IGNORECASE):
                defaults["metadata"] = model.metadata.copy()
            else:
                defaults[element] = model.__dict__[element][:]
    # We need to preserve the frequency column some how
    collapse_options = {}
    for key, value in defaults.items():
        collapse_options[key] = value
    for key, value in options.items():
        collapse_options[key] = value
    unique_independent_variable_list = sorted(list(set(model[independent_column_name])))
    independent_variable_selector = model.column_names.index(independent_column_name)
    out_data = []
    for index, independent_variable in enumerate(unique_independent_variable_list):
        data_row = [x for x in model.data[:] if x[independent_variable_selector] == independent_variable]
        if re.search('mean|av', collapse_options["method"], re.IGNORECASE):
            new_row = np.mean(np.array(data_row), axis=0).tolist()
        elif re.search('median', collapse_options["method"], re.IGNORECASE):
            new_row = np.median(np.array(data_row), axis=0).tolist()
        elif re.search('geometric', collapse_options["method"], re.IGNORECASE):
            new_row = gmean(np.array(data_row), axis=0).tolist()
        elif re.search('st', collapse_options["method"], re.IGNORECASE):
            new_row = np.std(np.array(data_row), axis=0).tolist()
        elif re.search('var', collapse_options["method"], re.IGNORECASE):
            new_row = np.var(np.array(data_row), axis=0, dtype=np.float64).tolist()
        elif re.search('rms', collapse_options["method"], re.IGNORECASE):
            new_row = np.sqrt(np.mean(np.square(np.array(data_row)), axis=0, dtype=np.float64)).tolist()
        elif re.search('rss', collapse_options["method"], re.IGNORECASE):
            new_row = np.sqrt(np.sum(np.square(np.array(data_row)), axis=0, dtype=np.float64)).tolist()
        elif re.search('mad', collapse_options["method"], re.IGNORECASE):
            new_row = mad(np.array(data_row), axis=0).tolist()
        new_row[independent_variable_selector]=independent_variable
        out_data.append(new_row)

    collapse_options["data"] = out_data

    if collapse_options["specific_descriptor"]:
        collapse_options["specific_descriptor"] = collapse_options["method"] + "_" + \
                                                  collapse_options["specific_descriptor"]
    resulting_model = AsciiDataTable(None, **collapse_options)
    return resulting_model


def independent_variable_model_difference(model_1, model_2, independent_column_name="Frequency", **options):
    """Takes the difference of two models that both have frequency and a similar set of columns. Returns an object that is
    a list of [[independent_variable,column_1,..column_n],...] where columns are the same in the models. If  a particular subset of
    columns is desired use columns=[independent_variable,column_name_1,..column_name_n] models
    can be any subclass of AsciiDataTable, SNP, or
    pandas.DataFrame, if a column is a non-numeric type it drops it. """
    # Set up defaults and pass options
    defaults = {"columns": "all", "interpolate": False, "average": True}
    difference_options = {}
    for key, value in defaults.items():
        difference_options[key] = value
    for key, value in options.items():
        difference_options[key] = value

    # first check type, if it is a panadas data frame a little conversion is needed, else is for all other models
    if isinstance(model_1,pandas.DataFrame):
        model_1 = DataFrame_to_AsciiDataTable(model_1)
    if isinstance(model_2,pandas.DataFrame):
        model_2 = DataFrame_to_AsciiDataTable(model_2)
    # now start with a set of frequencies (unique values from both)
    independent_variable_set_1 = set(model_1[independent_column_name])
    independent_variable_set_2 = set(model_2[independent_column_name])
    model_2_independent_variable_selector = model_2.column_names.index(independent_column_name)
    column_names_set_1 = set(model_1.column_names)
    column_names_set_2 = set(model_2.column_names)

    # All points must be in the intersection to be used
    independent_variable_intersection = list(independent_variable_set_1.intersection(independent_variable_set_2))
    column_names_intersection = list(column_names_set_1.intersection(column_names_set_2))

    if not independent_variable_intersection:
        print(("The models do not have any {0} points in common".format(independent_column_name)))
        return None
    new_column_names = [independent_column_name]
    column_types = ['float']
    for column_index, column in enumerate(model_1.column_names):
        if column in column_names_intersection and column not in [independent_column_name]:
            new_column_names.append(column)
            column_types.append(model_1.options["column_types"][column_index])

    difference_data = []
    for row_index, independent_variable in enumerate(model_1[independent_column_name]):
        new_row = [independent_variable]
        if independent_variable in independent_variable_intersection:
            model_2_independent_variable_row = \
            filter(lambda x: x[model_2_independent_variable_selector] == independent_variable,
                   model_2.data)[0]

            for column_index, column in enumerate(model_1.column_names):
                if column in column_names_intersection and column not in [independent_column_name]:
                    model_2_column_selector = model_2.column_names.index(column)
                    if re.search('int|float',
                                 model_1.options["column_types"][column_index],
                                 re.IGNORECASE) and re.search('int|float',
                                                              model_2.options["column_types"][model_2_column_selector],
                                                              re.IGNORECASE):

                        new_row.append(
                            model_1.data[row_index][column_index] - model_2_independent_variable_row[
                                model_2_column_selector])

                        # Print("New Column Names are {0}".format(new_column_names))
                    elif difference_options["columns"] in ["all"]:
                        new_row.append(model_1.data[row_index][column_index])
            difference_data.append(new_row)
    difference_options["column_names"] = new_column_names
    # print("New Column Names are {0}".format(new_column_names))
    difference_options["data"] = difference_data
    difference_options["column_types"] = column_types
    # print column_types
    result = AsciiDataTable(None, **difference_options)
    return result
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    