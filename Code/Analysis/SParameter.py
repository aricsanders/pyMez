#-----------------------------------------------------------------------------
# Name:        SParameter.py
# Purpose:    Tools to analyze SParameter Data
# Author:      Aric Sanders
# Created:     4/13/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Sparameter is a module with tools for analyzing Scattering parameter data. It contains functions
for comparing, applying corrections, uncertainty analysis and plotting scattering parameters.
see also <a href="./NISTUncertainty.m.html">NISTUncertainty</a>



 Examples
--------
    #!python
    >>test_compare_s2p_plots()

<h3><a href="../../../Examples/html/Applying_Calibration_Example.html">Applying a Correction Example</a></h3>
<h3><a href="../../../Examples/html/Calrep_Example.html">Using the Python Verison of Calrep</a></h3>
<h3><a href="../../../Examples/html/Creating_Comparing_Reference_Curves_MUFModels.html">Analysis of files made by the
NIST Microwave Uncertainty Framework</a></h3>
Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [datetime](https://docs.python.org/2/library/datetime.html)
+ [math](https://docs.python.org/2/library/math.html)
+ [cmath](https://docs.python.org/2/library/cmath.html)
+ [numpy](https://docs.scipy.org/doc/)
+ [scipy](https://docs.scipy.org/doc/)
+ [pandas](http://pandas.pydata.org/)
+ [matplotlib](http://matplotlib.org/)
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
    from Code.DataHandlers.TouchstoneModels import *
    from Code.DataHandlers.GeneralModels import *
    from Code.Analysis.NISTUncertainty import *
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

# Does this belong in tests or a Data folder
#Todo: This should not be here..
ONE_PORT_DUT=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')
#-----------------------------------------------------------------------------
# Module Functions

def cascade(s1,s2):
    """Cascade returns the cascaded sparameters of s1 and s2. s1 and s2 should be in complex list form
    [[f,S11,S12,S21,S22]...] and the returned sparameters will be in the same format. Assumes that s1,s2 have the
    same frequencies. If 1-S2_22*S1_11 is zero we add a small non zero real part or loss."""
    out_sparameters=[]
    for row_index,row in enumerate(s1):
        [f1,S1_11,S1_12,S1_21,S1_22]=row
        [f2,S2_11,S2_12,S2_21,S2_22]=s2[row_index]
        if f1!=f2:
            raise TypeError("Frequencies do not match! F lists must be the same")
        denominator=(1-S1_22*S2_11)
        if denominator ==complex(0,0):
            denominator=complex(10**-20,0)
        S11=S1_11+S2_11*(S1_12*S1_21)/denominator
        S12=S1_12*S2_12/(denominator)
        S21=S1_21*S2_21/denominator
        S22=S2_22+S1_22*(S2_12*S2_21)/denominator
        new_row=[f1,S11,S12,S21,S22]
        out_sparameters.append(new_row)
    return out_sparameters

def add_white_noise_s2p(s2p_model,noise_level=.0005):
    """Adds white noise to a s2p in RI format and returns a new s2p with the noise added to each real and imaginary component"""
    s2p_model.change_data_format("RI")
    s2p_data=s2p_model.data[:]
    noisy_data=[]
    for row in s2p_data:
        new_row=[row[0]]
        sparameters=np.array(row[1:])+np.random.normal(loc=0,scale=noise_level,size=len(row[1:]))
        new_row=new_row+sparameters.tolist()
        noisy_data.append(new_row)
    options=s2p_model.options.copy()
    options["file_path"]=None
    options["data"]=noisy_data
    options["sparameter_complex"]=[]
    noisy_s2p=S2PV1(**options)
    return noisy_s2p

def frequency_model_collapse_multiple_measurements(model, **options):
    """Returns a model with a single set of frequencies. Default is to average values together
    but geometric mean, std, variance, rss, mad and median are options.
    Geometric means of odd number of negative values fails"""
    if type(model) in [pandas.DataFrame]:
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
    unique_frequency_list = sorted(list(set(model["Frequency"])))
    frequency_selector = model.column_names.index("Frequency")
    out_data = []
    for index, frequency in enumerate(unique_frequency_list):
        data_row = [x for x in model.data[:] if x[frequency_selector] == frequency]
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
        new_row[frequency_selector]=frequency
        out_data.append(new_row)

    collapse_options["data"] = out_data

    if collapse_options["specific_descriptor"]:
        collapse_options["specific_descriptor"] = collapse_options["method"] + "_" + \
                                                  collapse_options["specific_descriptor"]
    resulting_model = AsciiDataTable(None, **collapse_options)
    return resulting_model

def frequency_model_difference(model_1, model_2, **options):
    """Takes the difference of two models that both have frequency and a similar set of columns. Returns an object that is
    a list of [[frequency,column_1,..column_n],...] where columns are the same in the models. If  a particular subset of
    columns is desired use columns=["Frequency","magS11] models can be any subclass of AsciiDataTable, SNP, or
    pandas.DataFrame, if a column is a non-numeric type it drops it. The frequency list should be unique
    (no multiple frequencies) for at least one model"""
    # Set up defaults and pass options
    defaults = {"columns": "all", "interpolate": False, "average": True}
    difference_options = {}
    for key, value in defaults.items():
        difference_options[key] = value
    for key, value in options.items():
        difference_options[key] = value

    # first check type, if it is a panadas data frame a little conversion is needed, else is for all other models
    if type(model_1) in [pandas.DataFrame]:
        model_1 = DataFrame_to_AsciiDataTable(model_1)
    if type(model_2) in [pandas.DataFrame]:
        model_2 = DataFrame_to_AsciiDataTable(model_2)
    # now start with a set of frequencies (unique values from both)
    frequency_set_1 = set(model_1["Frequency"])
    frequency_set_2 = set(model_2["Frequency"])
    model_2_frequency_selector = model_2.column_names.index('Frequency')
    column_names_set_1 = set(model_1.column_names)
    column_names_set_2 = set(model_2.column_names)

    # All points must be in the intersection to be used
    frequency_intersection = list(frequency_set_1.intersection(frequency_set_2))
    column_names_intersection = list(column_names_set_1.intersection(column_names_set_2))

    if not frequency_intersection:
        print("The models do not have any frequency points in common")
        return None
    new_column_names = ["Frequency"]
    column_types=['float']
    for column_index, column in enumerate(model_1.column_names):
        if column in column_names_intersection and column not in ["Frequency"]:
            new_column_names.append(column)
            column_types.append(model_1.options["column_types"][column_index])

    difference_data = []
    for row_index, frequency in enumerate(model_1["Frequency"]):
        new_row = [frequency]
        if frequency in frequency_intersection:
            model_2_frequency_row =list( filter(lambda x: x[model_2_frequency_selector] == frequency, model_2.data))[0]
            # print("{0} is {1}".format("model_2_frequency_row",model_2_frequency_row))
            for column_index, column in enumerate(model_1.column_names):
                if column in column_names_intersection and column not in ["Frequency"]:
                    model_2_column_selector = model_2.column_names.index(column)
                    if re.search('int|float',
                                 model_1.options["column_types"][column_index],
                                 re.IGNORECASE) and re.search('int|float',
                                                              model_2.options["column_types"][model_2_column_selector],
                                                              re.IGNORECASE):

                        new_row.append(
                            model_1.data[row_index][column_index] - model_2_frequency_row[model_2_column_selector])

                        # Print("New Column Names are {0}".format(new_column_names))
                    elif difference_options["columns"] in ["all"]:
                        new_row.append(model_1.data[row_index][column_index])
            difference_data.append(new_row)
    difference_options["column_names"] = new_column_names
    # print("New Column Names are {0}".format(new_column_names))
    difference_options["data"] = difference_data
    difference_options["column_types"]=column_types
    #print column_types
    result = AsciiDataTable(None, **difference_options)
    return result


def create_monte_carlo_reference_curve(monte_carlo_directory, **options):
    """Creates a standard curve from a montecarlo directory (from MUF). The standard curve
    has a mean or median and a standard deviation for the uncertainty"""
    defaults = {"method": "mean", "format": "RI", "filter": "s\d+p"}
    reference_options = {}
    for key, value in defaults.items():
        reference_options[key] = value
    for key, value in options.items():
        reference_options[key] = value
    file_names = os.listdir(monte_carlo_directory)
    filtered_file_names = []
    for file_name in file_names[:]:
        if re.search(reference_options["filter"], file_name, re.IGNORECASE):
            filtered_file_names.append(file_name)
    file_names = filtered_file_names
    # print file_names
    initial_file = SNP(os.path.join(monte_carlo_directory, file_names[0]))
    initial_file.change_data_format(reference_options["format"])
    combined_table = Snp_to_AsciiDataTable(initial_file)

    for file_name in file_names[1:]:
        snp_file = SNP(os.path.join(monte_carlo_directory, file_name))
        snp_file.change_data_format(reference_options["format"])
        table = Snp_to_AsciiDataTable(snp_file)
        combined_table + table
    mean_table = frequency_model_collapse_multiple_measurements(combined_table, method=reference_options["method"])
    standard_deviation = frequency_model_collapse_multiple_measurements(combined_table,
                                                                        method='std')
    new_column_names = ['Frequency'] + ['u' + name for name in standard_deviation.column_names[1:]]
    standard_deviation.column_names = new_column_names
    reference_curve = ascii_data_table_join("Frequency", mean_table, standard_deviation)
    reference_curve.options["value_column_names"] = mean_table.column_names[1:]
    reference_curve.options["uncertainty_column_names"] = new_column_names[1:]
    return reference_curve

def create_sensitivity_reference_curve(sensitivity_directory,nominal_file_path="../DUT_0.s2p",**options):
    """Creates a standard curve from a sensitivity_directory usually called Covariance(from MUF). The standard curve
    has a mean or median and a RMS variance from the nominal value for the uncertainty"""
    defaults = {"format": "RI", "filter": "s\d+p"}
    reference_options = {}
    for key, value in defaults.items():
        reference_options[key] = value
    for key, value in options.items():
        reference_options[key] = value
    file_names = os.listdir(sensitivity_directory)
    filtered_file_names = []
    for file_name in file_names[:]:
        if re.search(reference_options["filter"], file_name, re.IGNORECASE):
            filtered_file_names.append(file_name)
    file_names = filtered_file_names
    # print file_names
    nominal_file=SNP(os.path.join(sensitivity_directory, nominal_file_path))
    nominal_file.change_data_format(reference_options["format"])
    initial_file = SNP(os.path.join(sensitivity_directory, file_names[0]))
    initial_file.change_data_format(reference_options["format"])
    initial_difference=frequency_model_difference(nominal_file,initial_file)
    #print initial_difference.column_names
    combined_table = initial_difference
    for file_name in file_names[1:]:
        snp_file = SNP(os.path.join(sensitivity_directory, file_name))
        snp_file.change_data_format(reference_options["format"])
        difference=frequency_model_difference(nominal_file,snp_file)
        #print difference.column_names
#         table = Snp_to_AsciiDataTable(difference)
        combined_table + difference
    #print combined_table.options["column_types"]
    variance = frequency_model_collapse_multiple_measurements(combined_table,
                                                                        method='rss')
    new_column_names = ['Frequency'] + ['u' + name for name in variance.column_names[1:]]
    mean_table=Snp_to_AsciiDataTable(nominal_file)
    variance.column_names = new_column_names
    reference_curve = ascii_data_table_join("Frequency", mean_table, variance)
    reference_curve.options["value_column_names"] = mean_table.column_names[1:]
    reference_curve.options["uncertainty_column_names"] = new_column_names[1:]
    return reference_curve

def plot_reference_curve(reference_curve, **options):
    """Plots a frequency based reference curve by using the options
    value_column_names and uncertainty_column_names."""
    defaults = {"display_legend": False,
                "save_plot": False,
                "directory": os.getcwd(),
                "specific_descriptor": "Reference_Curve",
                "general_descriptor": "Plot",
                "file_name": None,
                "plots_per_column": 2,
                "plot_format": 'b-',
                "fill_color": 'k',
                "fill_opacity": .25,
                "fill_edge_color": 'k',
                "plot_size": (8, 10),
                "dpi": 80,
                "independent_axis_column_name": "Frequency",
                "share_x": "col"}
    plot_options = {}

    for key, value in defaults.items():
        plot_options[key] = value
    for key, value in options.items():
        plot_options[key] = value

    value_columns = reference_curve.options["value_column_names"]
    uncertainty_columns = reference_curve.options["uncertainty_column_names"]
    number_plots = len(value_columns)
    number_columns = int(plot_options["plots_per_column"])
    number_rows = int(round(float(number_plots) / float(number_columns)))
    fig, reference_axes = plt.subplots(nrows=number_rows, ncols=number_columns,
                                       sharex=plot_options["share_x"],
                                       figsize=plot_options["plot_size"],
                                       dpi=plot_options["dpi"])
    x_data = reference_curve[plot_options["independent_axis_column_name"]]
    for axes_index, ax in enumerate(reference_axes.flat):
        y_data = np.array(reference_curve[value_columns[axes_index]])
        error = np.array(reference_curve[uncertainty_columns[axes_index]])
        ax.plot(x_data, y_data, plot_options["plot_format"])
        ax.fill_between(x_data, y_data - error, y_data + error,
                        color=plot_options["fill_color"],
                        alpha=plot_options["fill_opacity"],
                        edgecolor=plot_options["fill_edge_color"])
        ax.set_title(value_columns[axes_index])

    plt.tight_layout()
    # Dealing with the save option
    if plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=plot_options["specific_descriptor"],
                              general_descriptor=plot_options["general_descriptor"],
                              directory=plot_options["directory"], extension='png', padding=3)
    else:
        file_name = plot_options["file_name"]
    if plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def plot_reference_curve_comparison(reference_curve_list, **options):
    """Plots a list of frequency based reference curves
     by using the options value_column_names and uncertainty_column_names.
     Options """
    defaults = {"display_legend": False,
                "save_plot": False,
                "directory": os.getcwd(),
                "specific_descriptor": "Reference_Curve",
                "general_descriptor": "Plot",
                "file_name": None,
                "plots_per_column": 2,
                "plot_format": '-',
                "fill_color": 'k',
                "fill_opacity": .25,
                "fill_edge_color": 'k',
                "plot_size": (8, 10),
                "dpi": 80,
                "independent_axis_column_name": "Frequency",
                "share_x": "col",
                "labels":None}
    plot_options = {}

    for key, value in defaults.items():
        plot_options[key] = value
    for key, value in options.items():
        plot_options[key] = value
    if plot_options["labels"]:
        labels=plot_options["labels"]
    else:
        labels=[x.path for x in reference_curve_list]
    value_columns = reference_curve_list[0].options["value_column_names"]
    uncertainty_columns = reference_curve_list[0].options["uncertainty_column_names"]
    number_plots = len(value_columns)
    number_columns = int(plot_options["plots_per_column"])
    number_rows = int(round(float(number_plots) / float(number_columns)))
    fig, reference_axes = plt.subplots(nrows=number_rows, ncols=number_columns,
                                       sharex=plot_options["share_x"],
                                       figsize=plot_options["plot_size"],
                                       dpi=plot_options["dpi"])
    for index,reference_curve in enumerate(reference_curve_list[:]):
        value_columns = reference_curve.options["value_column_names"]
        uncertainty_columns = reference_curve.options["uncertainty_column_names"]


        x_data = reference_curve[plot_options["independent_axis_column_name"]]
        for axes_index, ax in enumerate(reference_axes.flat):
            y_data = np.array(reference_curve[value_columns[axes_index]])
            error = np.array(reference_curve[uncertainty_columns[axes_index]])
            ax.plot(x_data, y_data, plot_options["plot_format"],label=labels[index])
            ax.fill_between(x_data, y_data - error, y_data + error,
                            color=plot_options["fill_color"],
                            alpha=plot_options["fill_opacity"],
                            edgecolor=plot_options["fill_edge_color"])
            ax.set_title(value_columns[axes_index])

    plt.tight_layout()
    if plot_options["display_legend"]:
        plt.legend()
    # Dealing with the save option
    if plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=plot_options["specific_descriptor"],
                              general_descriptor=plot_options["general_descriptor"],
                              directory=plot_options["directory"], extension='png', padding=3)
    else:
        file_name = plot_options["file_name"]
    if plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def calrep(raw_model,**options):
    """ Performs the calrep analysis routine on a raw data format (such as OnePortRawModel, TwoPortRawModel,PowerRawModel)
    Differs from the HP BASIC program in that it keeps the metadata Needs to be checked, returns 4 error terms for power
    Also does not calculate all the same rows for power, expansion factor is set to 2, requires that the raw model
    has the attribute raw_model.metadata["Connector_Type_Measurement"] defined. If the columns passed in raw_model
    do not have repeat values or contain text the result will set connect uncertainty to zero"""
    try:
        mean_file=frequency_model_collapse_multiple_measurements(raw_model)
    except:
        mean_file=raw_model
    try:
        standard_deviation_file=frequency_model_collapse_multiple_measurements(raw_model,method="std")
    except:
        std_data=[]
        for row in mean_file.data:
            new_row=[]
            for column in mean_file.data[0]:
                new_row.append(0)
            std_data.append(new_row)
        standard_deviation_file=AsciiDataTable(None,column_names=raw_model.column_names,
                                               data=std_data,column_types=raw_model.options["column_types"])
    if "Direction" in mean_file.column_names and "Connect" in mean_file.column_names:
        mean_file.remove_column("Direction")
        mean_file.remove_column("Connect")
    if "Direction" in standard_deviation_file.column_names and "Connect" in standard_deviation_file.column_names:
        standard_deviation_file.remove_column("Direction")
        standard_deviation_file.remove_column("Connect")
    new_data=[]
    new_column_names=[]
    expansion_factor=2
    frequency_index=mean_file.column_names.index("Frequency")
    for row_index,row in enumerate(mean_file.data[:]):
        new_data_row=[]
        for column_index,column_name in enumerate(mean_file.column_names[:]):
            if re.search("frequency",column_name,re.IGNORECASE):
                if row_index==0:
                    new_column_names.append("Frequency")
                new_data_row.append(row[column_index])
            else:
                if re.search("mag",column_name,re.IGNORECASE):
                    error_selector=0
                    error_letter="M"
                    error_parameter=column_name.replace("mag","")
                elif re.search("arg|phase",column_name,re.IGNORECASE):
                    error_selector=1
                    error_letter="A"
                    error_parameter=column_name.replace("arg","")
                elif re.search("Eff",column_name,re.IGNORECASE):
                    error_selector=0
                    error_letter="E"
                    error_parameter=""
                else:
                    error_selector=0
                if row_index==0:
                    # If this is the first row build the column names list
                    new_column_names.append(column_name)
                    new_column_names.append("u"+error_letter+"b"+error_parameter)
                    new_column_names.append("u"+error_letter+"a"+error_parameter)
                    new_column_names.append("u"+error_letter+"d"+error_parameter)
                    new_column_names.append("u"+error_letter+"g"+error_parameter)

                # Mean Value
                new_data_row.append(row[column_index])
                # Type B
                ub=type_b(wr_connector_type=mean_file.metadata["Connector_Type_Measurement"],
                         frequency=row[frequency_index],parameter=column_name,magnitude=row[column_index],format="mag")
                #print("{0} is {1}".format("ub",ub))
                new_data_row.append(ub[error_selector])
                # Type A or SNIST
                ua=S_NIST(wr_connector_type=mean_file.metadata["Connector_Type_Measurement"],
                         frequency=row[frequency_index],parameter=column_name,magnitude=row[column_index],format="mag")
                new_data_row.append(ua[error_selector])

                # Standard Deviation
                ud=standard_deviation_file.data[row_index][column_index]
                new_data_row.append(ud)
                # Total Uncertainty
                #print(" ua is {0}, ub is {1} and ud is {2}".format(ua,ub,ud))
                total_uncertainty=expansion_factor*math.sqrt(ua[error_selector]**2+ub[error_selector]**2+ud**2)
                new_data_row.append(total_uncertainty)
        new_data.append(new_data_row)
    sorted_keys=sorted(mean_file.metadata.keys())
    header=["{0} = {1}".format(key,mean_file.metadata[key]) for key in sorted_keys]
    column_types=["float" for column in new_column_names]
    #todo: Add value_column_names and uncertainty_column_names to conform to reference curve
    calrep=AsciiDataTable(None,data=new_data,column_types=column_types,
                          column_names=new_column_names,header=header,
                          metadata=mean_file.metadata)
    return calrep

def one_port_robin_comparison_plot(input_asc_file,input_res_file,**options):
    """one_port_robin_comparison_plot plots a one port.asc file against a given .res file,
    use device_history=True in options to show device history"""
    defaults={"device_history":False,"mag_res":False}
    plot_options={}
    for key,value in defaults.items():
        plot_options[key]=value
    for key,value in options.items():
        plot_options[key]=value
    history=np.loadtxt(input_res_file,skiprows=1)
    column_names=["Frequency",'magS11','argS11','magS11N','argS11N','UmagS11N','UargS11N']
    options={"data":history.tolist(),"column_names":column_names,"column_types":['float' for column in column_names]}
    history_table=AsciiDataTable(None,**options)
    table=OnePortCalrepModel(input_asc_file)
    if plot_options["device_history"]:
        history_frame=pandas.read_csv(ONE_PORT_DUT)
        device_history=history_frame[history_frame["Device_Id"]==table.header[0].rstrip().lstrip()]
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)

    ax0.errorbar(history_table.get_column('Frequency'),history_table.get_column('magS11N'),fmt='k--',
                yerr=history_table.get_column('UmagS11N'),label="History")
    ax0.errorbar(table.get_column('Frequency'),table.get_column('magS11'),
        yerr=table.get_column('uMg'),fmt='ro',label="Current Measurement",alpha=.3)
    if plot_options["device_history"]:
        ax0.errorbar(device_history['Frequency'].tolist(),device_history['magS11'].tolist(),fmt='bs',
                    yerr=device_history['uMg'].tolist(),label="From .asc", alpha=.5)
    if plot_options["mag_res"]:
        ax0.errorbar(history_table.get_column('Frequency'),history_table.get_column('mag'),fmt='gx',
                    yerr=history_table.get_column('UmagS11N'),label="From mag in res")
    ax0.set_title('Magnitude S11')

    ax1.errorbar(history_table.get_column('Frequency'),history_table.get_column('arg'),fmt='k--',
                yerr=history_table.get_column('UargS11N'),label="history")
    ax1.errorbar(table.get_column('Frequency'),table.get_column('arg'),
                 yerr=table.get_column('uAg'),fmt='ro',label="Current Measurement",alpha=.3)
    if plot_options["device_history"]:
        ax1.errorbar(device_history['Frequency'].tolist(),device_history['arg'].tolist(),fmt='bs',
                    yerr=device_history['uAg'].tolist(),label="From .asc", alpha=.5)
    ax1.set_title('Phase S11')
    ax0.legend(loc='lower left', shadow=True)
    plt.show()
    return fig

def two_port_swap_ports(complex_data):
    """Accepts data in [[frequency, S11, S21, S12, S22]..] format and returns
    [[frequency, S22, S12, S21, S11]..]"""
    out_data=[]
    for row in complex_data:
        [frequency, S11, S21, S12, S22]=row
        new_row=[frequency, S22, S12, S21, S11]
        out_data.append(new_row)
    return out_data

def two_port_complex_to_matrix_form(complex_data):
    """two_port_complex_to_matrix_form takes a list of [[frequency,S11,S21,S12,S22],..] and
    returns a list in the
    form [[frequency,np.matrix([[S11,S12],[S21,S22]])]..], it is meant to prepare data for correction"""
    out_list=[]
    for row in complex_data:
        frequency=row[0]
        [S11,S21,S12,S22]=row[1:]
        m=np.matrix([[S11,S12],[S21,S22]])
        out_list.append([frequency,m])
    #print out_list
    return out_list

def two_port_matrix_to_complex_form(matrix_form_data):
    """two_port_matrix_to_complex_form takes a list of [[frequency,np.matrix([[S11,S12],[S21,S22]])]..]
    and returns a list in the
    form [[frequency,S11,S21,S12,S22],..] , it is meant to undo two_port_complex_to_matrix_form"""
    out_list=[]
    for row in matrix_form_data:
        frequency=row[0]
        m=row[1]
        [S11,S21,S12,S22]=[m[0,0],m[1,0],m[0,1],m[1,1]]
        out_list.append([frequency,S11,S12,S21,S22])
    return out_list

def invert_two_port_matrix_list(two_port_matrix_form):
    """invert_two_port_matrix_list inverts all elements in the list two_port_matrix_form,
    which is in the format [[frequency,np.matrix([[S11,S12],[S21,S22]])]..] and returns a list
    in [[frequency,inv(np.matrix([[S11,S12],[S21,S22]]))]..] format works on any list in the form [value, matrix]
    """
    out_list=[]
    for row in two_port_matrix_form:
        frequency=row[0]
        m=row[1]
        m_inv=np.linalg.inv(m)
        out_list.append([frequency,m_inv])
    return out_list

def polar_average(complex_number_1,complex_number_2):
    """Averages 2 complex numbers in polar coordinates and returns a single complex number"""
    polar_number_1=cmath.polar(complex_number_1)
    polar_number_2=cmath.polar(complex_number_2)
    average_length=(polar_number_1[0]+polar_number_2[0])/2.
    average_phase=(polar_number_1[1]+polar_number_2[1])/2.
    out_value=cmath.rect(average_length,average_phase)
    return out_value

def polar_geometric_average(complex_number_1,complex_number_2):
    """Averages 2 complex numbers in polar coordinates and returns a single complex number"""
    polar_number_1=cmath.polar(complex_number_1)
    polar_number_2=cmath.polar(complex_number_2)
    average_length=(polar_number_1[0]*polar_number_2[0])**.5
    average_phase=(polar_number_1[1]+polar_number_2[1])/2
    out_value=cmath.rect(average_length,average_phase-math.pi)
    return out_value

def S_to_T(S_list):
    """Converts S-parameters into a T Matrix. Input form should be in frequency, np.matrix([[S11,S12],[S21,S22]])
    format. Returns a list in [frequency, np.matrix] format """
    t_complex_list=[]
    t_matrix=[]
    for row in S_list:
        frequency=row[0]
        m=row[1]
        T11=-np.linalg.det(m)/m[1,0]
        T12=m[0,0]/m[1,0]
        T21=-m[1,1]/m[1,0]
        T22=1/m[1,0]
        t_matrix.append([frequency,np.matrix([[T11,T12],[T21,T22]])])
        t_complex_list.append([frequency,T11,T12,T21,T22])
    return t_matrix

def T_to_S(T_list):
    """Converts T Matrix into S parameters. Input form should be in frequency, np.matrix([[T11,T12],[T21,T22]])
    format. Returns a list in [frequency, np.matrix] format."""
    S_list=[]
    for row in T_list:
        frequency=row[0]
        m=row[1]
        S11=m[0,1]/m[1,1]
        S12=np.linalg.det(m)/m[1,1]
        S21=1/m[1,1]
        S22=-m[1,0]/m[1,1]
        S_list.append([frequency,np.matrix([[S11,S12],[S21,S22]])])
    return S_list

def unwrap_phase(phase_list):
    """unwrap_phase returns an unwraped phase list given a wraped phase list,
    assumed units are degrees """
    unwrapped_phase_list=[]
    phase_list_copy=phase_list[:]
    i=1
    n=0
    while(i+1<len(phase_list)):
        if abs(phase_list[i]-phase_list[i-1])>90:
            if phase_list[i]-phase_list[i-1]>0:
                n+=1
            else:
                n-=1
            phase_list_copy[i]=phase_list_copy[i+1]-n*360
        phase_list_copy[i+1]=phase_list_copy[i+1]-n*360
        i+=1

    return phase_list_copy


def correct_sparameters_eight_term(sparameters_complex,eight_term_correction,reciprocal=True):
    """Applies the eight term correction to sparameters_complex and returns
    a correct complex list in the form of [[frequency,S11,S21,S12,S22],..]. The eight term
    correction should be in the form [[frequency,S1_11,S1_21,S1_12,S1_22,S2_11,S2_21,S2_12,S2_22]..]
    Use s2p.sparameter_complex as input."""
    # first transform both lists to matrices
    s2p_matrix_list=two_port_complex_to_matrix_form(sparameters_complex)
    s1_list=[[row[0],row[1],row[2],row[3],row[4]] for row in eight_term_correction]
    s2_list=[[row[0],row[5],row[6],row[7],row[8]] for row in eight_term_correction]
    s1_matrix_list=two_port_complex_to_matrix_form(s1_list)
    s2_matrix_list=two_port_complex_to_matrix_form(s2_list)
    # now transform to T matrices
    t_matrix_list=S_to_T(s2p_matrix_list)
    x_matrix_list=S_to_T(s1_matrix_list)
    y_matrix_list=S_to_T(s2_matrix_list)
    # now invert x
    x_inverse_matrix_list=invert_two_port_matrix_list(x_matrix_list)
    y_inverse_matrix_list=invert_two_port_matrix_list(y_matrix_list)
    # now apply the correction
    t_corrected_list=[]
    for index,row in enumerate(t_matrix_list):
        frequency=row[0]
        t_corrected=x_inverse_matrix_list[index][1]*row[1]*y_inverse_matrix_list[index][1]
        t_corrected_list.append([frequency,t_corrected])
    # now transform back to S
    s_corrected_matrix_list =T_to_S(t_corrected_list)
    # now put back into single row form
    s_corrected_list=two_port_matrix_to_complex_form(s_corrected_matrix_list)
    # now we take the geometric average and replace S12 and S21 with it
    if reciprocal:
        s_averaged_corrected=[]
        phase_last=0
        for row in s_corrected_list:
            [frequency,S11,S21,S12,S22]=row
            # S12 and S21 are averaged together in a weird way that makes phase continuous
            geometric_mean=cmath.sqrt(S21*S12)
            root_select=1
            phase_new=cmath.phase(geometric_mean)
            # if the phase jumps by >180 but less than 270, then pick the other root
            if abs(phase_new-phase_last)>math.pi/2 and abs(phase_new-phase_last)<3*math.pi/2:
                root_select=-1
            mean_S12_S21=root_select*cmath.sqrt(S21*S12)
            s_averaged_corrected.append([frequency,S11,mean_S12_S21,mean_S12_S21,S22])
            phase_last=cmath.phase(mean_S12_S21)
        s_corrected_list=s_averaged_corrected
    else:
        pass

    return s_corrected_list

def uncorrect_sparameters_eight_term(sparameters_complex,eight_term_correction,reciprocal=True):
    """Removes the eight term correction to sparameters_complex and returns
    a uncorrected (reference plane is measurement)
     complex list in the form of [[frequency,S11,S21,S12,S22],..]. The eight term
    correction should be in the form [[frequency,S1_11,S1_21,S1_12,S1_22,S2_11,S2_21,S2_12,S2_22]..]
    Use s2p.sparameter_complex as input."""
    # first transform both lists to matrices
    s2p_matrix_list=two_port_complex_to_matrix_form(sparameters_complex)
    s1_list=[[row[0],row[1],row[2],row[3],row[4]] for row in eight_term_correction]
    s2_list=[[row[0],row[5],row[6],row[7],row[8]] for row in eight_term_correction]
    s1_matrix_list=two_port_complex_to_matrix_form(s1_list)
    s2_matrix_list=two_port_complex_to_matrix_form(s2_list)
    # now transform to T matrices
    t_matrix_list=S_to_T(s2p_matrix_list)
    x_matrix_list=S_to_T(s1_matrix_list)
    y_matrix_list=S_to_T(s2_matrix_list)


    # now apply the correction
    t_uncorrected_list=[]
    for index,row in enumerate(t_matrix_list):
        frequency=row[0]
        t_corrected=x_matrix_list[index][1]*row[1]*y_matrix_list[index][1]
        t_uncorrected_list.append([frequency,t_corrected])
    # now transform back to S
    s_uncorrected_matrix_list =T_to_S(t_uncorrected_list)
    # now put back into single row form
    s_uncorrected_list=two_port_matrix_to_complex_form(s_uncorrected_matrix_list)
    # now we take the geometric average and replace S12 and S21 with it
    if reciprocal:
        s_averaged_corrected=[]
        phase_last=0
        for row in s_uncorrected_list:
            [frequency,S11,S21,S12,S22]=row
            # S12 and S21 are averaged together in a weird way that makes phase continuous
            geometric_mean=cmath.sqrt(S21*S12)
            root_select=1
            phase_new=cmath.phase(geometric_mean)
            # if the phase jumps by >180 but less than 270, then pick the other root
            if abs(phase_new-phase_last)>math.pi/2 and abs(phase_new-phase_last)<3*math.pi/2:
                root_select=-1
            mean_S12_S21=root_select*cmath.sqrt(S21*S12)
            s_averaged_corrected.append([frequency,S11,mean_S12_S21,mean_S12_S21,S22])
            phase_last=cmath.phase(mean_S12_S21)
        s_uncorrected_list=s_averaged_corrected
    else:
        pass

    return s_uncorrected_list

def correct_sparameters_sixteen_term(sparameters_complex,sixteen_term_correction):
    """Applies the sixteen term correction to sparameters and returns a new sparameter list.
    The sparameters should be a list of [frequency, S11, S21, S12, S22] where S terms are complex numbers.
    The sixteen term correction should be a list of
    [frequency, S11, S12, S13,S14,S21, S22,S23,S24,S31,S32,S33,S34,S41,S42,S43,S44], etc are complex numbers
    Designed to use S2P.sparameter_complex and SNP.sparameter_complex"""

    # first create 4 separate matrix lists for 16 term correction
    s1_matrix_list=[]
    s2_matrix_list=[]
    s3_matrix_list=[]
    s4_matrix_list=[]
    # Then populate them with the right values
    for index,correction in enumerate(sixteen_term_correction):
        [frequency, S11, S12, S13,S14,S21, S22,S23,S24,S31,S32,S33,S34,S41,S42,S43,S44]=correction
        s1_matrix_list.append([frequency,np.matrix([[S11,S12],[S21,S22]])])
        s2_matrix_list.append([frequency,np.matrix([[S13,S14],[S23,S24]])])
        s3_matrix_list.append([frequency,np.matrix([[S31,S32],[S41,S42]])])
        s4_matrix_list.append([frequency,np.matrix([[S33,S34],[S43,S44]])])
    sparameter_matrix_list=two_port_complex_to_matrix_form(sparameters_complex)
    # Apply the correction
    sparameter_out=[]
    for index,sparameter in enumerate(sparameter_matrix_list):
        frequency=sparameter[0]
        s_matrix=sparameter[1]
        [s11_matrix,s12_matrix,s21_matrix,s22_matrix]=[s1_matrix_list[index][1],s2_matrix_list[index][1],
                                                   s3_matrix_list[index][1],s4_matrix_list[index][1]]
        corrected_s_matrix=np.linalg.inv(s21_matrix*np.linalg.inv(s_matrix-s11_matrix)*s12_matrix+s22_matrix)
        # This flips S12 and S21
        sparameter_out.append([frequency,corrected_s_matrix[0,0],corrected_s_matrix[1,0],
                                corrected_s_matrix[0,1],corrected_s_matrix[1,1]])
    return sparameter_out

def uncorrect_sparameters_sixteen_term(sparameters_complex,sixteen_term_correction):
    """Removes the sixteen term correction to sparameters and returns a new sparameter list.
    The sparameters should be a list of [frequency, S11, S21, S12, S22] where S terms are complex numbers.
    The sixteen term correction should be a list of
    [frequency, S11, S12, S13,S14,S21, S22,S23,S24,S31,S32,S33,S34,S41,S42,S43,S44], etc are complex numbers
    Designed to use S2P.sparameter_complex and SNP.sparameter_complex.
    Inverse of correct_sparameters_sixteen_term"""

    # first create 4 separate matrix lists for 16 term correction
    s1_matrix_list=[]
    s2_matrix_list=[]
    s3_matrix_list=[]
    s4_matrix_list=[]
    # Then populate them with the right values
    for index,correction in enumerate(sixteen_term_correction):
        [frequency, S11, S12, S13,S14,S21, S22,S23,S24,S31,S32,S33,S34,S41,S42,S43,S44]=correction
        s1_matrix_list.append([frequency,np.matrix([[S11,S12],[S21,S22]])])
        s2_matrix_list.append([frequency,np.matrix([[S13,S14],[S23,S24]])])
        s3_matrix_list.append([frequency,np.matrix([[S31,S32],[S41,S42]])])
        s4_matrix_list.append([frequency,np.matrix([[S33,S34],[S43,S44]])])
    sparameter_matrix_list=two_port_complex_to_matrix_form(sparameters_complex)
    # Apply the correction
    sparameter_out=[]
    for index,sparameter in enumerate(sparameter_matrix_list):
        frequency=sparameter[0]
        s_matrix=sparameter[1]
        [s11_matrix,s12_matrix,s21_matrix,s22_matrix]=[s1_matrix_list[index][1],s2_matrix_list[index][1],
                                                   s3_matrix_list[index][1],s4_matrix_list[index][1]]
        uncorrected_s_matrix=np.linalg.inv(np.linalg.inv(s21_matrix)*(np.linalg.inv(s_matrix)-s22_matrix)*\
                                            np.linalg.inv(s12_matrix))+s11_matrix

        # This flips S12 and S21
        sparameter_out.append([frequency,uncorrected_s_matrix[0,0],uncorrected_s_matrix[1,0],
                               uncorrected_s_matrix[0,1],uncorrected_s_matrix[1,1]])
    return sparameter_out

def correct_sparameters_twelve_term(sparameters_complex,twelve_term_correction,reciprocal=True):
    """Applies the twelve term correction to sparameters and returns a new sparameter list.
    The sparameters should be a list of [frequency, S11, S21, S12, S22] where S terms are complex numbers.
    The twelve term correction should be a list of
    [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr] where Edf, etc are complex numbers"""
    if len(sparameters_complex) != len(twelve_term_correction):
        raise TypeError("s parameter and twelve term correction must be the same length")
    sparameter_out=[]
    phase_last=0.
    for index,row in enumerate(sparameters_complex):
        frequency=row[0]
        Sm=np.matrix(row[1:]).reshape((2,2))
        [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr]=twelve_term_correction[index]
        #        frequency Edf Esf Erf Exf Elf Etf Edr Esr Err Exr Elr Etr.
#         print [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr]
#         print Sm[0,0]
        D =(1+(Sm[0,0]-Edf)*(Esf/Erf))*(1+(Sm[1,1]-Edr)*(Esr/Err))-(Sm[0,1]*Sm[1,0]*Elf*Elr)/(Etf*Etr)
#         print D
        S11 =(Sm[0,0]-Edf)/(D*Erf)*(1+(Sm[1,1]-Edr)*(Esr/Err))-(Sm[0,1]*Sm[1,0]*Elf)/(D*Etf*Etr)
        S21 =((Sm[1,0]-Exr)/(D*Etf))*(1+(Sm[1,1]-Edr)*(Esr-Elf)/Err)
        S12 = ((Sm[0,1]-Exf)/(D*Etr))*(1+(Sm[0,0]-Edf)*(Esf-Elr)/Erf)
        S22 = (Sm[1,1]-Edr)/(D*Err)*(1+(Sm[0,0]-Edf)*(Esf/Erf))-(Sm[0,1]*Sm[1,0]*Elr)/(D*Etf*Etr)
        # S12 and S21 are averaged together in a weird way that makes phase continuous
        geometric_mean=cmath.sqrt(S21*S12)
        root_select=1
        phase_new=cmath.phase(geometric_mean)
        # if the phase jumps by >180 but less than 270, then pick the other root
        if abs(phase_new-phase_last)>math.pi/2 and abs(phase_new-phase_last)<3*math.pi/2:
            root_select=-1
        mean_S12_S21=root_select*cmath.sqrt(S21*S12)
        if reciprocal:
            sparameter_out.append([frequency,S11,mean_S12_S21,mean_S12_S21,S22])
        else:
            sparameter_out.append([frequency,S11,S21,S12,S22])
        phase_last=cmath.phase(mean_S12_S21)
    return sparameter_out

def uncorrect_sparameters_twelve_term(sparameters_complex,twelve_term_correction,reciprocal=True):
    """Removes the twelve term correction to sparameters and returns a new sparameter list.
    The sparameters should be a list of [frequency, S11, S21, S12, S22] where S terms are complex numbers.
    The twelve term correction should be a list of
    [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr] where Edf, etc are complex numbers"""
    if len(sparameters_complex) != len(twelve_term_correction):
        raise TypeError("s parameter and twelve term correction must be the same length")
    sparameter_out=[]
    phase_last=0.
    for index,row in enumerate(sparameters_complex):
        frequency=row[0]
        Sa=np.matrix(row[1:]).reshape((2,2))
        [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr]=twelve_term_correction[index]
        #        frequency Edf Esf Erf Exf Elf Etf Edr Esr Err Exr Elr Etr.
#         print [frequency,Edf,Esf,Erf,Exf,Elf,Etf,Edr,Esr,Err,Exr,Elr,Etr]
#         print Sm[0,0]
        delta=Sa[0,0]*Sa[1,1]-Sa[0,1]*Sa[1,0]
#         print D
        S11 =Edf+(Erf)*(Sa[0,0]-Elf*delta)/(1-Esf*Sa[0,0]-Elf*Sa[1,1]+Esf*Elf*delta)
        S21 =Etf*(Sa[1,0])/(1-Esf*Sa[0,0]-Elf*Sa[1,1]-Esf*Elf*delta)
        S12 = Etr*(Sa[0,1])/(1-Elr*Sa[0,0]-Esr*Sa[1,1]-Esr*Elr*delta)
        S22 = Edr+Err*(Sa[1,1]-Elr*delta)/(1-Elr*Sa[0,0]-Esr*Sa[1,1]-Esr*Elr*delta)
        # S12 and S21 are averaged together in a weird way that makes phase continuous
        geometric_mean=cmath.sqrt(S21*S12)
        root_select=1
        phase_new=cmath.phase(geometric_mean)
        # if the phase jumps by >180 but less than 270, then pick the other root
        if abs(phase_new-phase_last)>math.pi/2 and abs(phase_new-phase_last)<3*math.pi/2:
            root_select=-1
        mean_S12_S21=root_select*cmath.sqrt(S21*S12)
        if reciprocal:
            sparameter_out.append([frequency,S11,mean_S12_S21,mean_S12_S21,S22])
        else:
            sparameter_out.append([frequency,S11,S21,S12,S22])
        phase_last=cmath.phase(mean_S12_S21)
    return sparameter_out
#TODO: Check that this works the way it should
def correct_sparameters(sparameters,correction,**options):
    """Correction sparamters trys to return a corrected set of sparameters given uncorrected sparameters
    and a correction. Correct sparameters will accept file_name's, pyMez classes,
    complex lists or a mixture, returns value in the form it was entered. Correction is assumed reciprocal
    unless reciprocal=False"""
    defaults={"reciprocal":True,"output_type":None,"file_path":None}
    correction_options={}
    for key,value in defaults.items():
        correction_options[key]=value
    for key,value in options.items():
        correction_options[key]=value
    try:
        # import and condition sparameters and correction
        if isinstance(sparameters, StringType):
            # Assume sparameters is given by file name
            sparameters_table=S2PV1(sparameters)
            sparameters=sparameters_table.sparameter_complex
            output_type='file'
        elif re.search('S2PV1',type(sparameters)):
            output_type='S2PV1'
            sparameters=sparameters.sparameter_complex
        elif isinstance(sparameters, ListType):
            # check to see if it is a list of complex variables or matrix
            if isinstance(sparameters[1], ComplexType):
                output_type='complex_list'
            # Handle frequency, matrix lists
            elif type(sparameters[1]) in ['np.array','np.matrix'] and isinstance(sparameters, FloatType) :
                output_type='matrix_list'
                sparameters=two_port_matrix_to_complex_form(sparameters)
            # handle matrix
        elif type(sparameters) in ['np.array','np.matrix']:
            output_type='matrix'
            raise
        # Handle the correction types
        if len(correction) is 13:
            corrected_sparameters=correct_sparameters_twelve_term(sparameters,correction)
        elif len(correction) is 17:
            corrected_sparameters=correct_sparameters_sixteen_term(sparameters,correction)
        elif len(correction) is 9:
            corrected_sparameters=correct_sparameters_eight_term(sparameters,correction)
        # Handle the output type using the derived one or the one entered as an option
        if correction_options["output_type"] is None:
            pass
        else:
            output_type=correction_options["output_type"]
        if re.match('file',output_type, re.IGNORECASE):
            output_table=S2PV1(correction_options["file_path"],sparameter_complex=corrected_sparameters)
            output_table.save()
            print(("Output was saved as {0}".format(output_table.path)))
        elif re.search("complex",output_type,re.IGNORECASE):
            return corrected_sparameters
        elif re.search("matrix_list",output_type,re.IGNORECASE):
            return two_port_complex_to_matrix_form(corrected_sparameters)
        elif re.search("matrix",output_type,re.IGNORECASE):
            raise

    except:
        print("Could not correct sparameters")
        raise

def average_one_port_sparameters(table_list,**options):
    """Returns a table that is the average of the Sparameters in table list. The new table will have all the unique
    frequency values contained in all of the tables. Tables must be in Real-Imaginary format or magnitude-angle format
    do not try to average db-angle format. """
    #This will work on any table that the data is stored in data, need to add a sparameter version
    defaults={"frequency_selector":0,"frequency_column_name":"Frequency"}
    average_options={}
    for key,value in defaults.items():
        average_options[key]=value
    for key,value in options.items():
        average_options[key]=value
    frequency_list=[]
    average_data=[]
    for table in table_list:
        frequency_list=frequency_list+table.get_column("Frequency")
    unique_frequency_list=sorted(list(set(frequency_list)))
    for frequency in unique_frequency_list:
        new_row=[]
        for table in table_list:
            data_list=[x for x in table.data if x[average_options["frequency_selector"]]==frequency]
            table_average=np.mean(np.array(data_list),axis=0)
            new_row.append(table_average)
            #print new_row
        average_data.append(np.mean(new_row,axis=0).tolist())
    return average_data

def two_port_comparison_plot_with_residuals(two_port_raw,mean_frame,difference_frame):
    """Creates a comparison plot given a TwoPortRawModel object and a pandas.DataFrame mean frame"""
    fig, axes = plt.subplots(nrows=3, ncols=2, sharex='col',figsize=(8,6),dpi=80)
    measurement_date=two_port_raw.metadata["Measurement_Date"]
    ax0,ax1,ax2,ax3,ax4,ax5 = axes.flat
    compare_axes=[ax0,ax1,ax2,ax3,ax4,ax5]
    diff_axes=[]
    for ax in compare_axes:
        diff_axes.append(ax.twinx())
    #diff_axes=[diff_ax0,diff_ax1,diff_ax2,diff_ax3,diff_ax4,diff_ax5]
    column_names=['Frequency','magS11','argS11','magS21','argS21','magS22','argS22']
    for index,ax in enumerate(diff_axes):
        ax.plot(difference_frame['Frequency'].tolist(),difference_frame[column_names[index+1]].tolist(),'r-x')
        ax.set_ylabel('Difference',color='red')
        if re.search('mag',column_names[index+1]):
            ax.set_ylim(-.02,.02)
        #ax.legend_.remove()
    for index, ax in enumerate(compare_axes):
        ax.plot(two_port_raw.get_column('Frequency'),two_port_raw.get_column(column_names[index+1]),
                'k-o',label=measurement_date)
        ax.plot(mean_frame['Frequency'].tolist(),mean_frame[column_names[index+1]].tolist(),'gs',label='Mean')
        ax.set_title(column_names[index+1])
        ax.legend(loc=1,fontsize='8')
        #ax.xaxis.set_visible(False)
        if re.search('arg',column_names[index+1]):
            ax.set_ylabel('Phase(Degrees)',color='green')
        elif re.search('mag',column_names[index+1]):
            ax.set_ylabel(r'|${\Gamma} $|',color='green')
        #ax.sharex(diff_axes[index])
    ax4.set_xlabel('Frequency(GHz)',color='k')
    ax5.set_xlabel('Frequency(GHz)',color='k')
    fig.subplots_adjust(hspace=0)
    fig.suptitle(two_port_raw.metadata["Device_Id"]+"\n",fontsize=18,fontweight='bold')
    plt.tight_layout()
    plt.show()
    return fig

def two_port_difference_frame(two_port_raw,mean_frame):
    """Creates a difference pandas.DataFrame given a two port raw file and a mean pandas.DataFrame"""
    difference_list=[]
    for row in two_port_raw.data[:]:
        #print row[0]
        mean_row=mean_frame[abs(mean_frame["Frequency"]-row[0])<abs(.01)].as_matrix()
        #print mean_row
        try:
            mean_row=mean_row[0]
            difference_row=[row[i+2]-mean_row[i] for i in range(1,len(mean_row))]
            difference_row.insert(0,row[0])
            difference_list.append(difference_row)
        except:pass
    column_names=['Frequency','magS11','argS11','magS21','argS21','magS22','argS22']
    diff_data_frame=pandas.DataFrame(difference_list,columns=column_names)
    return diff_data_frame

def two_port_mean_frame(device_id,system_id=None,history_data_frame=None):
    """Given a Device_Id and a pandas data frame of the history creates a mean data_frame"""
    device_history=history_data_frame[history_data_frame["Device_Id"]==device_id]
    if system_id is not None:
        device_history=device_history[device_history["System_Id"]==system_id]
    column_names=['Frequency','magS11','argS11','magS21','argS21','magS22','argS22']
    unique_frequency_list=device_history["Frequency"].unique()
    mean_array=[]
    for index,freq in enumerate(unique_frequency_list):
        row=[]
        for column in column_names:
            values=np.mean(device_history[device_history["Frequency"]==unique_frequency_list[index]][column].as_matrix())
            #print values
            mean_value=np.mean(values)
            row.append(mean_value)
        mean_array.append(row)
    mean_frame=pandas.DataFrame(mean_array,columns=column_names)
    return mean_frame

def mean_from_history(history_frame,**options):
    """mean_from_history creates a mean_frame given a full history frame (pandas.DataFrame object),
    by setting options it selects column names
    to output and input values to filter on. Returns a pandas.DataFrame object with column names = column_names,
    and filtered by any of the following: "Device_Id","System_Id","Measurement_Timestamp",
    "Connector_Type_Measurement", "Measurement_Date" or "Measurement_Time" """

    defaults={"Device_Id":None, "System_Id":None,"Measurement_Timestamp":None,
              "Connector_Type_Measurement":None,
             "Measurement_Date":None,"Measurement_Time":None,"Direction":None,
              "column_names":['Frequency','magS11','argS11'],"outlier_removal":True}
    mean_options={}
    for key,value in defaults.items():
        mean_options[key]=value
    for key,value in options.items():
            mean_options[key]=value

    filters=["Device_Id","System_Id","Measurement_Timestamp","Connector_Type_Measurement",
             "Measurement_Date","Measurement_Time","Direction"]
    temp_frame=history_frame.copy()
    for index,filter_type in enumerate(filters):
        if mean_options[filter_type] is not None:
            temp_frame=temp_frame[temp_frame[filter_type]==mean_options[filter_type]]
#     temp_frame=temp_frame[temp_frame["Device_Id"]==mean_options["Device_Id"]]
#     temp_frame=temp_frame[temp_frame["System_Id"]==mean_options["System_Id"]]
    if mean_options["outlier_removal"]:
        mean_s11=np.mean(temp_frame["magS11"])
        std_s11=np.std(temp_frame["magS11"])
        temp_frame=temp_frame[temp_frame["magS11"]<(mean_s11+3*std_s11)]
        temp_frame = temp_frame[temp_frame["magS11"] > (mean_s11 - 3 * std_s11)]
    unique_frequency_list=temp_frame["Frequency"].unique()
    mean_array=[]
    for index,freq in enumerate(unique_frequency_list):
        row=[]
        for column in mean_options["column_names"]:
            values=np.mean(temp_frame[temp_frame["Frequency"]==unique_frequency_list[index]][column].as_matrix())
            mean_value=np.mean(values)
            row.append(mean_value)
        mean_array.append(row)
    mean_frame=pandas.DataFrame(mean_array,columns=mean_options["column_names"])
    return mean_frame

def median_from_history(history_frame,**options):
    """median_from_history creates a median_frame given a full history frame (pandas.DataFrame object),
    by setting options it selects column names
    to output and input values to filter on. Returns a pandas.DataFrame object with column names = column_names,
    and filtered by any of the following: "Device_Id","System_Id","Measurement_Timestamp",
    "Connector_Type_Measurement", "Measurement_Date" or "Measurement_Time" """

    defaults={"Device_Id":None, "System_Id":None,"Measurement_Timestamp":None,
              "Connector_Type_Measurement":None,
             "Measurement_Date":None,"Measurement_Time":None,"Direction":None,
              "column_names":['Frequency','magS11','argS11'],"outlier_removal":True}
    median_options={}
    for key,value in defaults.items():
        median_options[key]=value
    for key,value in options.items():
            median_options[key]=value

    filters=["Device_Id","System_Id","Measurement_Timestamp","Connector_Type_Measurement",
             "Measurement_Date","Measurement_Time","Direction"]
    temp_frame=history_frame.copy()
    for index,filter_type in enumerate(filters):
        if median_options[filter_type] is not None:
            temp_frame=temp_frame[temp_frame[filter_type]==median_options[filter_type]]
    if median_options["outlier_removal"]:
        mean_s11=np.mean(temp_frame["magS11"])
        std_s11=np.std(temp_frame["magS11"])
        temp_frame=temp_frame[temp_frame["magS11"]<(mean_s11+3*std_s11)]
        temp_frame = temp_frame[temp_frame["magS11"] > (mean_s11 - 3 * std_s11)]
#     temp_frame=temp_frame[temp_frame["Device_Id"]==median_options["Device_Id"]]
#     temp_frame=temp_frame[temp_frame["System_Id"]==median_options["System_Id"]]
    unique_frequency_list=temp_frame["Frequency"].unique()
    median_array=[]
    for index,freq in enumerate(unique_frequency_list):
        row=[]
        for column in median_options["column_names"]:
            values=np.median(temp_frame[temp_frame["Frequency"]==unique_frequency_list[index]][column].as_matrix())
            median_value=np.median(values)
            row.append(median_value)
        median_array.append(row)
    median_frame=pandas.DataFrame(median_array,columns=median_options["column_names"])
    return median_frame

def raw_difference_frame(raw_model,mean_frame,**options):
    """Creates a difference pandas.DataFrame given a raw NIST model and a mean pandas.DataFrame"""
    defaults={"column_names":mean_frame.columns.tolist()}
    difference_options={}
    for key,value in defaults.items():
        difference_options[key]=value
    for key,value in options.items():
        difference_options[key]=value
    difference_list=[]
    for row in raw_model.data[:]:
        #print row[0]
        mean_row=mean_frame[abs(mean_frame["Frequency"]-row[0])<abs(.01)].as_matrix()
        #print mean_row
        try:
            mean_row=mean_row[0]
            difference_row=[row[i+2]-mean_row[i] for i in range(1,len(mean_row))]
            difference_row.insert(0,row[0])
            difference_list.append(difference_row)
        except:pass
    difference_data_frame=pandas.DataFrame(difference_list,columns=difference_options["column_names"])
    return difference_data_frame

def return_history_key(calrep_model):
    "Returns a key for the history dictionary given a calrep model"
    model=calrep_model.__class__.__name__
    #print model
    if re.search('Calrep|DUT',model):
        if re.search('OnePortCalrep',model):
            return '1-port calrep'
        elif re.search('TwoPortCalrep',model):
            return '2-port calrep'
        elif re.search('PowerCalrep',model):
            if calrep_model.options["column_names"]==POWER_3TERM_COLUMN_NAMES:
                return 'power 3term calrep'
            elif calrep_model.options["column_names"]==POWER_4TERM_COLUMN_NAMES:
                return 'power 4term calrep'
        elif re.search('OnePortDUT',model):
            return 'power 3term calrep'
    else:
        raise TypeError("Must be a calrep model, such as OnePortCalrepModel, etc. ")

def raw_comparison_plot_with_residuals(raw_nist,mean_frame,difference_frame,**options):
    """Creates a comparison plot given a RawModel object and a pandas.DataFrame mean frame and difference frame"""
    defaults={"display_mean":True,
              "display_difference":True,
              "display_raw":True,
              "display_legend":True,
              "save_plot":False,
              "directory":None,
              "specific_descriptor":raw_nist.metadata["Device_Id"]+"_Check_Standard",
              "general_descriptor":"Plot","file_name":None}
    comparison_plot_options={}
    for key,value in defaults.items():
        comparison_plot_options[key]=value
    for key,value in options.items():
        comparison_plot_options[key]=value
    column_names=mean_frame.columns.tolist()
    number_rows=int(len(column_names)/2)
    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col',figsize=(8,6),dpi=80)
    measurement_date=raw_nist.metadata["Measurement_Date"]
    diff_axes=[]
    for ax in compare_axes.flat:
        diff_axes.append(ax.twinx())
    #diff_axes=[diff_ax0,diff_ax1,diff_ax2,diff_ax3,diff_ax4,diff_ax5]
    if comparison_plot_options["display_difference"]:
        for index,ax in enumerate(diff_axes):
            ax.plot(difference_frame['Frequency'].tolist(),difference_frame[column_names[index+1]].tolist(),'r-x')
            ax.set_ylabel('Difference',color='red')
            if re.search('mag',column_names[index+1]):
                ax.set_ylim(-.02,.02)
            #ax.legend_.remove()
    for index, ax in enumerate(compare_axes.flat):
        if comparison_plot_options["display_raw"]:
            ax.plot(raw_nist.get_column('Frequency'),raw_nist.get_column(column_names[index+1]),
                    'k-o',label=measurement_date)
        if comparison_plot_options["display_mean"]:
            ax.plot(mean_frame['Frequency'].tolist(),mean_frame[column_names[index+1]].tolist(),'gs',label='Mean')
        ax.set_title(column_names[index+1])
        if comparison_plot_options["display_legend"]:
            ax.legend(loc=1,fontsize='8')
        #ax.xaxis.set_visible(False)
        if re.search('arg',column_names[index+1]):
            ax.set_ylabel('Phase(Degrees)',color='green')
        elif re.search('mag',column_names[index+1]):
            ax.set_ylabel(r'|${\Gamma} $|',color='green')
        #ax.sharex(diff_axes[index])
    compare_axes.flat[-2].set_xlabel('Frequency(GHz)',color='k')
    compare_axes.flat[-1].set_xlabel('Frequency(GHz)',color='k')
    fig.subplots_adjust(hspace=0)
    fig.suptitle(raw_nist.metadata["Device_Id"]+"\n",fontsize=18,fontweight='bold')
    plt.tight_layout()
    if comparison_plot_options["file_name"] is None:
        file_name=auto_name(specific_descriptor=comparison_plot_options["specific_descriptor"],
                            general_descriptor=comparison_plot_options["general_descriptor"],
                            directory=comparison_plot_options["directory"],extension='png',padding=3)
    else:
        file_name=comparison_plot_options["file_name"]
    if comparison_plot_options["save_plot"]:
        #print file_name
        plt.savefig(os.path.join(comparison_plot_options["directory"],file_name))
    else:
        plt.show()
    return fig

def calrep_history_plot(calrep_model,history_frame,**options):
    """Given a calrep_model and a history frame calrep_history_plot plots the file against any other in history
    frame  (pandas.DataFrame) with dates"""
    defaults={"display_legend":True,
              "save_plot":False,
              "directory":None,
              "specific_descriptor":calrep_model.metadata["Device_Id"]+"_Device_Measurement",
              "general_descriptor":"Plot",
              "file_name":None,
              "min_num":0,
              "max_num":None,
              "error_style":"area"}
    history_plot_options={}
    for key,value in defaults.items():
        history_plot_options[key]=value
    for key,value in options.items():
        history_plot_options[key]=value
    # The way we plot depends on the models
    model=calrep_model.__class__.__name__
    # The new method relies on metadata and not the class
    if re.search("DataTable",model,re.IGNORECASE):
        try:
            if calrep_model.metadata["Measurement_Type"] in ['1-port']:
                model="OnePort"
            elif calrep_model.metadata["Measurement_Type"] in ['2-port']:
                model="TwoPort"
            elif re.search('Dry Cal|Thermistor|power',calrep_model.metadata["Measurement_Type"]):
                model="Power"
        except:
            pass


    device_history=history_frame[history_frame["Device_Id"]==calrep_model.metadata["Device_Id"]]
    unique_analysis_dates=sorted(device_history["Analysis_Date"].unique().tolist())
    print(("{0} are {1}".format("unique_analysis_dates",unique_analysis_dates)))
    if re.search('Power',model):
        number_rows=2
        column_names=['magS11','argS11','Efficiency','Calibration_Factor']
        if calrep_model.options["column_names"]==POWER_3TERM_COLUMN_NAMES:
            error_names=['uMgS11','uAgS11','uEe','uCe']
        elif calrep_model.options["column_names"]==POWER_4TERM_COLUMN_NAMES:
            error_names=['uMgS11','uAgS11','uEg','uCg']
        table=calrep_model.joined_table

    elif re.search('OnePort',model):
        number_rows=1
        column_names=['magS11','argS11']
        error_names=['uMgS11','uAgS11']
        table=calrep_model

    elif re.search('TwoPort',model):
        number_rows=3
        column_names=['magS11','argS11','magS21','argS21','magS22','argS22']
        error_names=['uMgS11','uAgS11','uMgS21','uAgS21','uMgS22','uAgS22']
        table=calrep_model.joined_table

    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col',figsize=(8,6),dpi=80)
    for index, ax in enumerate(compare_axes.flat):

        #ax.xaxis.set_visible(False)
        if re.search('arg',column_names[index]):
            ax.set_ylabel('Phase(Degrees)',color='green')
        elif re.search('mag',column_names[index]):
            ax.set_ylabel(r'|${\Gamma} $|',color='green')
        ax.set_title(column_names[index])
        # initial plot of
        x=table.get_column('Frequency')
        y=np.array(table.get_column(column_names[index]))
        error=np.array(table.get_column(error_names[index]))
        if re.search('bar',history_plot_options["error_style"],re.IGNORECASE):
            ax.errorbar(x,y,yerr=error,fmt='k--')

            for date_index,date in enumerate(unique_analysis_dates[history_plot_options["min_num"]:history_plot_options["max_num"]]):
                number_lines=len(unique_analysis_dates[history_plot_options["min_num"]:history_plot_options["max_num"]])
                date_device_history=device_history[device_history["Analysis_Date"]==date]
                if not date_device_history.empty:
                    x_date=date_device_history['Frequency']
                    y_date=np.array(date_device_history[column_names[index]].tolist())
                    error_date=np.array(date_device_history[error_names[index]].tolist())
                    #print("{0} is {1}".format("date_device_history",date_device_history))
                    #print("{0} is {1}".format("y_date",y_date))
                    #print("{0} is {1}".format("date",date))
                    date_color=(1-float(date_index+1)/number_lines,0,float(date_index+1)/number_lines,.5)
                    ax.errorbar(x_date,y_date,
                         yerr=error_date,color=date_color,label=date)
        elif re.search('area',history_plot_options["error_style"],re.IGNORECASE):
            ax.plot(x,y,'k--')
            ax.fill_between(x,y-error,y+error,edgecolor=(0,.0,.0,.25), facecolor=(.25,.25,.25,.1),
                            linewidth=1)
            for date_index,date in enumerate(unique_analysis_dates[history_plot_options["min_num"]:history_plot_options["max_num"]]):
                number_lines=float(len(unique_analysis_dates[history_plot_options["min_num"]:history_plot_options["max_num"]]))
                #print("{0} is {1}".format("number_lines",number_lines))
                #print("{0} is {1}".format("index",index))
                #print("{0} is {1}".format("date_index",date_index))
                date_color=(1-float(date_index+1)/number_lines,0,float(date_index+1)/number_lines,.5)
                #print("{0} is {1}".format("date_color",date_color))

                date_device_history=device_history[device_history["Analysis_Date"]==date]
                x_date=date_device_history['Frequency']
                y_date=np.array(date_device_history[column_names[index]].tolist())
                error_date=np.array(date_device_history[error_names[index]].tolist())


                ax.plot(x_date,y_date,
                        color=date_color,label=date)
        #ax.sharex(diff_axes[index])
        if history_plot_options["display_legend"]:
            ax.legend(loc=1,fontsize='8')
    compare_axes.flat[-2].set_xlabel('Frequency(GHz)',color='k')
    compare_axes.flat[-1].set_xlabel('Frequency(GHz)',color='k')
    fig.subplots_adjust(hspace=0)
    fig.suptitle(calrep_model.metadata["Device_Id"]+"\n",fontsize=18,fontweight='bold')
    plt.tight_layout()

    # Dealing with the save option
    if history_plot_options["file_name"] is None:
        file_name=auto_name(specific_descriptor=history_plot_options["specific_descriptor"],
                            general_descriptor=history_plot_options["general_descriptor"],
                            directory=history_plot_options["directory"],extension='png',padding=3)
    else:
        file_name=history_plot_options["file_name"]
    if history_plot_options["save_plot"]:
        #print file_name
        plt.savefig(os.path.join(history_plot_options["directory"],file_name))
    else:
        plt.show()
    return fig

def compare_s2p_plots(list_S2PV1,**options):
    """compare_s2p_plot compares a list of s2p files plotting each on the same axis for all
    8 possible components. The format of plots can be changed by passing options as key words in a
    key word dictionary. """
    defaults={"format":"MA",
              "display_legend":True,
              "save_plot":False,
              "directory":None,
              "specific_descriptor":"comparison_Plot",
              "general_descriptor":"Plot",
              "file_name":None,
              "labels":None,
              "title":None,
              "grid":True}
    comparison_plot_options={}
    for key,value in defaults.items():
        comparison_plot_options[key]=value
    for key,value in options.items():
        comparison_plot_options[key]=value

    # create a set of 8 subplots
    #plt.hold(True)
    fig, compare_axes = plt.subplots(nrows=4, ncols=2, figsize=(8,6),dpi=80)
    if comparison_plot_options["labels"] is None:
        labels=[s2p.path for s2p in list_S2PV1]
    else:
        labels=comparison_plot_options["labels"]
    for s2p_index,s2p in enumerate(list_S2PV1):
        # start by changing the format of all the s2p
        s2p.change_data_format(comparison_plot_options["format"])
        column_names=s2p.column_names[1:]
        for index, ax in enumerate(compare_axes.flat):
            #ax.xaxis.set_visible(False)
            if re.search('arg',column_names[index]):
                ax.set_ylabel('Phase(Degrees)',color='black')
            elif re.search('mag',column_names[index]):
                ax.set_ylabel(r'|{0}|'.format(column_names[index].replace("mag","")),color='green')
            if comparison_plot_options["grid"]:
                ax.grid(True)
            ax.set_title(column_names[index])
            # initial plot of
            x=s2p.get_column('Frequency')
            y=np.array(s2p.get_column(column_names[index]))
            ax.plot(x,y,label=labels[s2p_index])
            if comparison_plot_options["display_legend"]:
                if index == 1:
                    ax.legend(loc="center left", bbox_to_anchor=(1.05, .5),
                              shadow=True,
                              fancybox=True)


    compare_axes.flat[-2].set_xlabel('Frequency(GHz)',color='k')
    compare_axes.flat[-1].set_xlabel('Frequency(GHz)',color='k')
    if comparison_plot_options["title"]:
        fig.suptitle(comparison_plot_options["title"])
    fig.subplots_adjust(hspace=0)
    plt.tight_layout()
    # Dealing with the save option
    if comparison_plot_options["file_name"] is None:
        file_name=auto_name(specific_descriptor=comparison_plot_options["specific_descriptor"],
                            general_descriptor=comparison_plot_options["general_descriptor"],
                            directory=comparison_plot_options["directory"]
                            ,extension='png',padding=3)
    else:
        file_name=comparison_plot_options["file_name"]
    if comparison_plot_options["save_plot"]:
        #print file_name
        plt.savefig(os.path.join(comparison_plot_options["directory"],file_name))
    else:
        plt.show()
    return fig

def return_calrep_value_column_names(calrep_model):
    """Returns the column names for values in a calrep model. For example if the
    calrep model is a 1-port, then it returns ["magS11","argS11"] """
    measurement_type = calrep_model.metadata["Measurement_Type"]
    if re.search('1|one', measurement_type, re.IGNORECASE):
        column_names = ['magS11', 'argS11']
    elif re.search('2|two', measurement_type, re.IGNORECASE):
        if re.search('NR', measurement_type, re.IGNORECASE):
            column_names = ['magS11', 'argS11', 'magS12', 'argS12', 'magS21', 'argS21', 'magS22', 'argS22']
        else:
            column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
    else:
        column_names = ['magS11', 'argS11', 'Efficiency']
    return column_names

def return_calrep_error_column_names(calrep_model_value_columns,error_suffix='g'):
    """Returns the column names for errors in a calrep model. For example if the
    calrep model value column names are ["magS11","argS11"], then it returns ["uMgS11","uAgS11"] """
    error_columns = []
    for column in calrep_model_value_columns[:]:
        error_column = column.replace("mag", "uM" + error_suffix)
        error_column = error_column.replace("arg", "uA" + error_suffix)
        error_column = error_column.replace("Efficiency", "uE" + error_suffix)
        error_columns.append(error_column)
    return error_columns


def plot_frequency_model(frequency_model, **options):
    """Plots any table with frequency as its x-axis and column_names as the x-axis in a
    series of subplots"""
    defaults = {"display_legend": False,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Frequency_Model",
                "general_descriptor": "Plot",
                "file_name": None,
                "plots_per_column": 2,
                "plot_format": 'b-o',
                "share_x": False,
                "subplots_title": True,
                "plot_title": None,
                "plot_size": (8, 6),
                "dpi": 80}
    plot_options = {}
    for key, value in defaults.items():
        plot_options[key] = value
    for key, value in options.items():
        plot_options[key] = value
    if type(frequency_model) in [pandas.DataFrame]:
        frequency_model = DataFrame_to_AsciiDataTable(frequency_model)
    x_data = np.array(frequency_model["Frequency"])
    y_data_columns = frequency_model.column_names[:]
    y_data_columns.remove("Frequency")
    number_plots = len(y_data_columns)
    number_columns = plot_options["plots_per_column"]
    number_rows = int(round(float(number_plots) / float(number_columns)))
    figure, axes = plt.subplots(ncols=number_columns, nrows=number_rows, sharex=plot_options["share_x"],
                                figsize=plot_options["plot_size"], dpi=plot_options["dpi"])
    for plot_index, ax in enumerate(axes.flat):
        if plot_index < number_plots:
            y_data = np.array(frequency_model[y_data_columns[plot_index]])
            ax.plot(x_data, y_data, plot_options["plot_format"], label=y_data_columns[plot_index])
            if plot_options["display_legend"]:
                ax.legend()
            if plot_options["subplots_title"]:
                ax.set_title(y_data_columns[plot_index])
        else:
            pass
    if plot_options["plot_title"]:
        plt.suptitle(plot_options["plot_title"])

    plt.tight_layout()
    # Dealing with the save option
    if plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=plot_options["specific_descriptor"],
                              general_descriptor=plot_options["general_descriptor"],
                              directory=plot_options["directory"], extension='png', padding=3)
    else:
        file_name = plot_options["file_name"]
    if plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(plot_options["directory"], file_name))
    else:
        plt.show()
    return figure


def plot_frequency_model_histogram(frequency_model, **options):
    """Plots any table with frequency as its x-axis and column_names as the x-axis in a
    series of subplots"""
    defaults = {"display_legend": False,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Frequency_Model",
                "general_descriptor": "Plot",
                "file_name": None,
                "plots_per_column": 2,
                "plot_format": 'b-o',
                "share_x": False,
                "subplots_title": True,
                "plot_title": None,
                "plot_size": (8, 6),
                "dpi": 80,
                "non_plotable_text": "Not Plotable"}
    plot_options = {}
    for key, value in defaults.items():
        plot_options[key] = value
    for key, value in options.items():
        plot_options[key] = value
    if type(frequency_model) in [pandas.DataFrame]:
        frequency_model = DataFrame_to_AsciiDataTable(frequency_model)
    x_data = np.array(frequency_model["Frequency"])
    y_data_columns = frequency_model.column_names[:]
    y_data_columns.remove("Frequency")
    number_plots = len(y_data_columns)
    number_columns = plot_options["plots_per_column"]
    number_rows = int(round(float(number_plots) / float(number_columns)))
    figure, axes = plt.subplots(ncols=number_columns, nrows=number_rows, sharex=plot_options["share_x"],
                                figsize=plot_options["plot_size"], dpi=plot_options["dpi"])
    for plot_index, ax in enumerate(axes.flat):
        if plot_index < number_plots:
            try:
                y_data = np.array(frequency_model[y_data_columns[plot_index]])
                ax.hist(y_data)
                if plot_options["display_legend"]:
                    ax.legend()
                if plot_options["subplots_title"]:
                    ax.set_title(y_data_columns[plot_index])
            except:
                text = plot_options["non_plotable_text"]
                plt.text.Annotation(text, (0, 0))
                if plot_options["subplots_title"]:
                    ax.set_title(y_data_columns[plot_index])
        else:
            pass
    if plot_options["plot_title"]:
        plt.suptitle(plot_options["plot_title"])

    plt.tight_layout()
    # Dealing with the save option
    if plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=plot_options["specific_descriptor"],
                              general_descriptor=plot_options["general_descriptor"],
                              directory=plot_options["directory"], extension='png', padding=3)
    else:
        file_name = plot_options["file_name"]
    if plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(plot_options["directory"], file_name))
    else:
        plt.show()
    return figure

def plot_calrep(calrep_model):
    """Plots a calrep model with uncertainties"""
    # todo: add options to this plot
    if type(calrep_model) in [PowerCalrepModel,TwoPortCalrepModel]:
        calrep_model.joined_table.metadata=calrep_model.metadata
        calrep_model=calrep_model.joined_table

    # Uncertainties all have u in them
    average_columns=[]
    for column_name in calrep_model.column_names[:]:
        if re.search("mag|arg|eff",column_name,re.IGNORECASE):
            average_columns.append(column_name)
    #print("{0} is {1}".format("average_columns",average_columns))
    number_plots=len(average_columns)
    number_rows=int(round(number_plots/2.))
    fig, axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col')
    for plot_index,ax in enumerate(axes.flat):
        column_name=average_columns[plot_index]
        ax.set_title(column_name)
        if re.search("mag",column_name,re.IGNORECASE):
            error_letter="M"
            error_parameter=column_name.replace("mag","")
            error_name="u"+error_letter+"g"+error_parameter
            error=calrep_model[error_name]
            x=calrep_model["Frequency"]
            y=calrep_model[column_name]
            #print("Length of x is {0}, Length of y is {1}, Length of error is {2}".format(len(x),len(y),len(error)))
            ax.errorbar(x,y,yerr=error,fmt='k-x')
            ax.set_ylabel(r'|${\Gamma} $|',color='green')
        elif re.search("arg",column_name,re.IGNORECASE):
            error_letter="A"
            error_parameter=column_name.replace("arg","")
            error_name="u"+error_letter+"g"+error_parameter
            error=calrep_model[error_name]
            x=calrep_model["Frequency"]
            y=calrep_model[column_name]
            ax.errorbar(x,y,yerr=error,fmt='k-x')
            ax.set_ylabel('Phase(Degrees)',color='green')
        elif re.search("eff",column_name,re.IGNORECASE):
            error_letter="E"
            error_parameter=""
            try:
                error_name="u"+error_letter+"g"+error_parameter
                error=calrep_model[error_name]
            except:
                error_name="u"+error_letter+"e"+error_parameter
                error=calrep_model[error_name]

            x=calrep_model["Frequency"]
            y=calrep_model[column_name]
            ax.errorbar(x,y,yerr=error,fmt='k-x')
            ax.set_ylabel('Phase(Degrees)',color='green')
            break
    fig.suptitle(calrep_model.metadata["Device_Id"])
    plt.tight_layout()
    plt.show()
    return fig
def plot_calrep_uncertainty(calrep_model,**options):
    """Plots the uncertainty values for a calrep model versus frequency"""
    defaults = {"display_legend": True,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Calrep_Uncertainty",
                "general_descriptor": "Plot",
                "file_name": None,
                "error_suffixes":['b','a','d','g'] ,
                "error_names":['Type B','SNIST','Connect','Total Uncertainty'],
                "error_plot_formats": ['r-x','b-x','g-x','k-x']}
    comparison_plot_options = {}
    for key, value in defaults.items():
        comparison_plot_options[key] = value
    for key, value in options.items():
        comparison_plot_options[key] = value
    # figure out the number of plots based on the measurement type
    measurement_type = calrep_model.metadata["Measurement_Type"]
    if re.search('1|one', measurement_type, re.IGNORECASE):
        number_plots = 2
        column_names = ['magS11', 'argS11']
    elif re.search('2|two', measurement_type, re.IGNORECASE):
        if re.search('NR', measurement_type, re.IGNORECASE):
            number_plots = 8
            column_names = ['magS11', 'argS11', 'magS12', 'argS12', 'magS21', 'argS21', 'magS22', 'argS22']
        else:
            number_plots = 6
            column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
    else:
        number_plots = 3
        column_names = ['magS11', 'argS11', 'Efficiency']
    # create the error column names
    error_columns = []
    for column in column_names[:]:
        error_columns_per_plot=[]
        for suffix in comparison_plot_options["error_suffixes"]:
            error_column = column.replace("mag", "uM" +suffix )
            error_column = error_column.replace("arg", "uA" + suffix)
            error_column = error_column.replace("Efficiency", "uE" +suffix)
            error_columns_per_plot.append(error_column)
        error_columns.append(error_columns_per_plot)

    # We want plots that have frequency as the x-axis and y that has an error
    calrep_x = calrep_model["Frequency"]
    number_rows = int(round(float(number_plots) / 2))
    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col', figsize=(8, 6), dpi=80)
    # each axis has an error column
    for plot_index, ax in enumerate(compare_axes.flat[:]):
        for error_index,error_column in enumerate(error_columns[plot_index]):

            error = np.array(calrep_model[error_column])
            ax.plot(calrep_x, error, comparison_plot_options['error_plot_formats'][error_index],
                    label='{0}'.format(comparison_plot_options['error_names'][error_index]))
            ax.set_title(column_names[plot_index])

        if comparison_plot_options["display_legend"]:
            ax.legend()

    # Dealing with the save option
    if comparison_plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=comparison_plot_options["specific_descriptor"],
                              general_descriptor=comparison_plot_options["general_descriptor"],
                              directory=comparison_plot_options["directory"]
                              , extension='png', padding=3)
    else:
        file_name = comparison_plot_options["file_name"]
    if comparison_plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(comparison_plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def plot_checkstandard_history(device_history, **options):
    """Creates a plot of all of the measurements of a device from a history frame (pandas.DataFrame).
     """
    defaults = {"display_legend": True,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Checkstandard_History",
                "general_descriptor": "Plot",
                "file_name": None,
                "min_num": 0,
                "max_num": None,
                "error_style": "area",
                "extra_plots": None,
                "extra_plot_labels": None,
                "extra_plot_formats": None}
    history_plot_options = {}
    for key, value in defaults.items():
        history_plot_options[key] = value
    for key, value in options.items():
        history_plot_options[key] = value
    device_id = device_history["Device_Id"].unique().tolist()[0]
    measurement_type = device_history["Measurement_Type"].unique().tolist()[0]
    # The new method relies on metadata and not the class

    try:
        if re.search("1", measurement_type, re.IGNORECASE):
            model = "OnePort"
        elif re.search("2", measurement_type, re.IGNORECASE):
            model = "TwoPort"
        elif re.search('Dry Cal|Thermistor|power', measurement_type):
            model = "Power"
    except:
        model = ""

    # print("{0} is {1}".format("model",model))
    unique_measurement_dates = sorted(device_history["Measurement_Timestamp"].unique().tolist())
    number_dates = len(unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]])
    extra_length = 0
    if history_plot_options['extra_plots']:
        extra_length = len(history_plot_options['extra_plots'])
    number_measurements = number_dates + extra_length
    # print("{0} are {1}".format("unique_measurement_dates",unique_measurement_dates))
    number_rows = 0
    if re.search('Power', model):
        number_rows = 2
        column_names = ['magS11', 'argS11', 'Efficiency', 'Calibration_Factor']


    elif re.search('OnePort', model):
        number_rows = 1
        column_names = ['magS11', 'argS11']


    elif re.search('TwoPort', model):
        number_rows = 3
        column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']

    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col', figsize=(8, 6), dpi=80)
    for index, ax in enumerate(compare_axes.flat):

        # ax.xaxis.set_visible(False)
        if re.search('arg', column_names[index]):
            ax.set_ylabel('Phase(Degrees)', color='green')
        elif re.search('mag', column_names[index]):
            ax.set_ylabel(r'|{0}|'.format(column_names[index]), color='green')
        # ax.set_title(column_names[index])
        # initial plot of
        if history_plot_options["extra_plots"]:
            if history_plot_options["extra_plot_formats"]:
                plot_formats = history_plot_options["extra_plot_formats"]
            else:
                plot_formats = ["r--" for plot in history_plot_options["extra_plots"]]
            if history_plot_options["extra_plot_labels"]:
                for model_index, model in enumerate(history_plot_options["extra_plots"]):
                    x = model["Frequency"]
                    y = model[column_names[index]]
                    ax.plot(x, y, plot_formats[model_index],
                            label=history_plot_options["extra_plot_labels"][model_index])
            else:
                for model_index, model in enumerate(history_plot_options["extra_plots"]):
                    x = model["Frequency"]
                    y = model[column_names[index]]
                    ax.plot(x, y, plot_formats[model_index], label="Comparison {0}".format(model_index))

        for date_index, date in enumerate(
                unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]]):
            number_lines = len(
                unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]])
            date_device_history = device_history[device_history["Measurement_Timestamp"] == date]
            if not date_device_history.empty:
                x_date = date_device_history['Frequency']
                y_date = np.array(date_device_history[column_names[index]].tolist())
                date_color = (1 - float(date_index + 1) / number_lines, 0, float(date_index + 1) / number_lines, .5)
                ax.plot(x_date, y_date,
                        color=date_color, label=date)

        # ax.sharex(diff_axes[index])
        if history_plot_options["display_legend"]:
            if index == 1:
                ax.legend(loc="center left", bbox_to_anchor=(1.05, .5),
                          ncol=int(max([round(float(number_measurements) / 28.), 1])), shadow=True,
                          title="Measurement Dates", fancybox=True)
    compare_axes.flat[-2].set_xlabel('Frequency(GHz)', color='k')
    compare_axes.flat[-1].set_xlabel('Frequency(GHz)', color='k')
    fig.subplots_adjust(hspace=0)
    plt.tight_layout()
    fig.suptitle(device_id + "\n", fontsize=18, fontweight='bold', y=1.05, )
    # Dealing with the save option
    if history_plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=history_plot_options["specific_descriptor"],
                              general_descriptor=history_plot_options["general_descriptor"],
                              directory=history_plot_options["directory"], extension='png', padding=3)
    else:
        file_name = history_plot_options["file_name"]
    if history_plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(history_plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def plot_calrep_results_comparison(calrep_model, results_model, **options):
    """Plots a calrep file and a results file on the same axis. Input is a calrep table from the sparameter
    function calrep and a
    results file, with options. """
    defaults = {"display_legend": True,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "comparison_Plot",
                "general_descriptor": "Plot",
                "file_name": None,
                "labels": None,
                "error_suffix": 'g',
                "calrep_format": 'k-x',
                "results_format": 'r-x'}
    comparison_plot_options = {}
    for key, value in defaults.items():
        comparison_plot_options[key] = value
    for key, value in options.items():
        comparison_plot_options[key] = value
    # figure out the number of plots based on the measurement type
    measurement_type = calrep_model.metadata["Measurement_Type"]
    if re.search('1|one', measurement_type, re.IGNORECASE):
        number_plots = 2
        column_names = ['magS11', 'argS11']
    elif re.search('2|two', measurement_type, re.IGNORECASE):
        if re.search('NR', measurement_type, re.IGNORECASE):
            number_plots = 8
            column_names = ['magS11', 'argS11', 'magS12', 'argS12', 'magS21', 'argS21', 'magS22', 'argS22']
        else:
            number_plots = 6
            column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
    else:
        number_plots = 3
        column_names = ['magS11', 'argS11', 'Efficiency']
    # create the error column names
    error_columns = []
    for column in column_names[:]:
        error_column = column.replace("mag", "uM" + comparison_plot_options["error_suffix"])
        error_column = error_column.replace("arg", "uA" + comparison_plot_options["error_suffix"])
        error_column = error_column.replace("Efficiency", "uE" + comparison_plot_options["error_suffix"])
        error_columns.append(error_column)

    # We want plots that have frequency as the x-axis and y that has an error
    calrep_x = calrep_model["Frequency"]
    results_x = results_model["Frequency"]
    number_rows = int(round(float(number_plots) / 2))
    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col', figsize=(8, 6), dpi=80)
    # each axis has an error column
    for plot_index, ax in enumerate(compare_axes.flat[:]):
        calrep_y = np.array(calrep_model[column_names[plot_index]])
        results_y = np.array(results_model[column_names[plot_index]])
        error = np.array(calrep_model[error_columns[plot_index]])
        ax.plot(calrep_x, calrep_y, comparison_plot_options['calrep_format'],
                label='Calrep of {0}'.format(calrep_model.metadata["Device_Id"]))
        ax.fill_between(calrep_x, calrep_y - error, calrep_y + error, edgecolor=(0, .0, .0, .25),
                        facecolor=(.25, .25, .25, .1),
                        linewidth=1)
        ax.plot(results_x, results_y, comparison_plot_options['results_format'], label="Reference File")
        if comparison_plot_options["display_legend"]:
            ax.legend()

    # Dealing with the save option
    if comparison_plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=comparison_plot_options["specific_descriptor"],
                              general_descriptor=comparison_plot_options["general_descriptor"],
                              directory=comparison_plot_options["directory"]
                              , extension='png', padding=3)
    else:
        file_name = comparison_plot_options["file_name"]
    if comparison_plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(comparison_plot_options["directory"], file_name))
    else:
        plt.show()
    return fig


def plot_calrep_results_difference_comparison(calrep_model, results_model, **options):
    """Plots a calrep file and a results file on the same axis. Input is a calrep table from the sparameter
    function calrep and a
    results file, with options. """
    defaults = {"display_legend": False,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Difference_Comparison",
                "general_descriptor": "Plot",
                "file_name": None,
                "labels": None,
                "error_suffix": 'g',
                "calrep_format": 'r-x',
                "results_format": 'r-x',
                "debug": False,
                "title": 'Calrep diference of {0}'.format(calrep_model.metadata["Device_Id"])}
    comparison_plot_options = {}
    for key, value in defaults.items():
        comparison_plot_options[key] = value
    for key, value in options.items():
        comparison_plot_options[key] = value
    # figure out the number of plots based on the measurement type
    measurement_type = calrep_model.metadata["Measurement_Type"]
    if re.search('1|one', measurement_type, re.IGNORECASE):
        number_plots = 2
        column_names = ['magS11', 'argS11']
    elif re.search('2|two', measurement_type, re.IGNORECASE):
        if re.search('NR', measurement_type, re.IGNORECASE):
            number_plots = 8
            column_names = ['magS11', 'argS11', 'magS12', 'argS12', 'magS21', 'argS21', 'magS22', 'argS22']
        else:
            number_plots = 6
            column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
    else:
        number_plots = 3
        column_names = ['magS11', 'argS11', 'Efficiency']
    # create the error column names
    error_columns = []
    for column in column_names[:]:
        error_column = column.replace("mag", "uM" + comparison_plot_options["error_suffix"])
        error_column = error_column.replace("arg", "uA" + comparison_plot_options["error_suffix"])
        error_column = error_column.replace("Efficiency", "uE" + comparison_plot_options["error_suffix"])
        error_columns.append(error_column)
    difference_model = frequency_model_difference(calrep_model, results_model)
    if comparison_plot_options["debug"]:
        print(("{0} is {1}".format("difference_model.column_names", difference_model.column_names)))
    # We want plots that have frequency as the x-axis and y that has an error
    difference_x = difference_model["Frequency"]
    calrep_x = calrep_model["Frequency"]
    number_rows = int(round(float(number_plots) / 2))
    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col', figsize=(8, 6), dpi=80)
    # each axis has an error column
    for plot_index, ax in enumerate(compare_axes.flat[:]):

        difference_y = np.array(difference_model[column_names[plot_index]])
        error = np.array(calrep_model[error_columns[plot_index]])
        ax.plot(difference_x, difference_y, comparison_plot_options['calrep_format'],
                label='Calrep diiference of {0}'.format(calrep_model.metadata["Device_Id"]))
        ax.fill_between(calrep_x, - error, error, edgecolor=(0, .0, .0, .25),
                        facecolor=(.25, .25, .25, .1),
                        linewidth=1)
        if comparison_plot_options["display_legend"]:
            ax.legend()

    if comparison_plot_options["title"]:
        fig.suptitle(comparison_plot_options["title"])

    # Dealing with the save option
    if comparison_plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=comparison_plot_options["specific_descriptor"],
                              general_descriptor=comparison_plot_options["general_descriptor"],
                              directory=comparison_plot_options["directory"]
                              , extension='png', padding=3)
    else:
        file_name = comparison_plot_options["file_name"]
    if comparison_plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(comparison_plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def plot_calrep_comparison(calrep_model_list):
    """Plots many calrep models on the same axis with uncertainties"""
    for index,calrep_model in enumerate(calrep_model_list):
        if type(calrep_model) in [PowerCalrepModel,TwoPortCalrepModel]:
            calrep_model_list[index].joined_table.metadata=calrep_model.metadata
            calrep_model_list[index]=calrep_model.joined_table

        # Uncertainties all have u in them
    average_columns=[]
    for column_name in calrep_model_list[0].column_names[:]:
            if re.search("mag|arg|eff",column_name,re.IGNORECASE):
                average_columns.append(column_name)
    #print("{0} is {1}".format("average_columns",average_columns))
    number_plots=len(average_columns)
    number_rows=int(round(number_plots/2.))
    #plt.hold(True)
    fig, axes = plt.subplots(nrows=number_rows, ncols=2, sharex='col')
    for calrep_model in calrep_model_list:
        for plot_index,ax in enumerate(axes.flat):
            column_name=average_columns[plot_index]
            ax.set_title(column_name)
            if re.search("mag",column_name,re.IGNORECASE):
                error_letter="M"
                error_parameter=column_name.replace("mag","")
                error_name="u"+error_letter+"g"+error_parameter
                error=calrep_model[error_name]
                x=calrep_model["Frequency"]
                y=calrep_model[column_name]
                ax.errorbar(x,y,yerr=error)
                ax.set_ylabel(r'|${\Gamma} $|',color='green')
            elif re.search("arg",column_name,re.IGNORECASE):
                error_letter="A"
                error_parameter=column_name.replace("arg","")
                error_name="u"+error_letter+"g"+error_parameter
                error=calrep_model[error_name]
                x=calrep_model["Frequency"]
                y=calrep_model[column_name]
                ax.errorbar(x,y,yerr=error)
                ax.set_ylabel('Phase(Degrees)',color='green')
            elif re.search("eff",column_name,re.IGNORECASE):
                error_letter="E"
                error_parameter=""
                try:
                    error_name="u"+error_letter+"g"+error_parameter
                    error=calrep_model[error_name]
                except:
                    error_name="u"+error_letter+"e"+error_parameter
                    error=calrep_model[error_name]

                x=calrep_model["Frequency"]
                y=calrep_model[column_name]
                ax.errorbar(x,y,yerr=error)
                ax.set_ylabel('Phase(Degrees)',color='green')
                break
    plt.tight_layout()
    plt.show()
    return fig


def plot_checkstandard_history(device_history, **options):
    """Creates a plot of all of the measurements of a device from a history frame (pandas.DataFrame).
     """
    defaults = {"display_legend": True,
                "save_plot": False,
                "directory": None,
                "specific_descriptor": "Checkstandard_History",
                "general_descriptor": "Plot",
                "file_name": None,
                "min_num": 0,
                "max_num": None,
                "error_style": "area",
                "extra_plots": None,
                "extra_plot_labels": None,
                "extra_plot_formats": None}
    history_plot_options = {}
    for key, value in defaults.items():
        history_plot_options[key] = value
    for key, value in options.items():
        history_plot_options[key] = value
    device_id = device_history["Device_Id"].unique().tolist()[0]
    measurement_type = device_history["Measurement_Type"].unique().tolist()[0]
    # The new method relies on metadata and not the class

    try:
        if re.search("1", measurement_type, re.IGNORECASE):
            model = "OnePort"
        elif re.search("2", measurement_type, re.IGNORECASE):
            model = "TwoPort"
        elif re.search('Dry Cal|Thermistor|power', measurement_type):
            model = "Power"
    except:
        model = ""

    # print("{0} is {1}".format("model",model))
    unique_measurement_dates = sorted(device_history["Measurement_Timestamp"].unique().tolist())
    number_dates = len(unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]])
    extra_length = 0
    if history_plot_options['extra_plots']:
        extra_length = len(history_plot_options['extra_plots'])
    number_measurements = number_dates + extra_length
    # print("{0} are {1}".format("unique_measurement_dates",unique_measurement_dates))
    number_rows = 0
    if re.search('Power', model):
        number_rows = 3
        column_names = ['magS11', 'argS11', 'Efficiency']
        number_columns=1


    elif re.search('OnePort', model):
        number_rows = 1
        column_names = ['magS11', 'argS11']
        number_columns = 2

    elif re.search('TwoPort', model):
        number_rows = 3
        column_names = ['magS11', 'argS11', 'magS21', 'argS21', 'magS22', 'argS22']
        number_columns = 2

    fig, compare_axes = plt.subplots(nrows=number_rows, ncols=number_columns, sharex='col', figsize=(8, 6), dpi=80)
    for index, ax in enumerate(compare_axes.flat):

        try:
            # ax.xaxis.set_visible(False)
            if re.search('arg', column_names[index]):
                ax.set_ylabel('Phase(Degrees)', color='green')
            elif re.search('mag', column_names[index]):
                ax.set_ylabel(r'|{0}|'.format(column_names[index]), color='green')
            elif re.search('Ef', column_names[index]):
                ax.set_ylabel(r'|{0}|'.format(column_names[index]), color='green')
            # ax.set_title(column_names[index])
            # initial plot of

            if history_plot_options["extra_plots"]:
                if history_plot_options["extra_plot_formats"]:
                    plot_formats = history_plot_options["extra_plot_formats"]
                else:
                    plot_formats = ["r--" for plot in history_plot_options["extra_plots"]]
                if history_plot_options["extra_plot_labels"]:
                    for model_index, model in enumerate(history_plot_options["extra_plots"]):
                        x = model["Frequency"]
                        y = model[column_names[index]]
                        ax.plot(x, y, plot_formats[model_index],
                                label=history_plot_options["extra_plot_labels"][model_index])
                else:
                    for model_index, model in enumerate(history_plot_options["extra_plots"]):
                        x = model["Frequency"]
                        y = model[column_names[index]]
                        ax.plot(x, y, plot_formats[model_index], label="Comparison {0}".format(model_index))
        except:
            pass
        for date_index, date in enumerate(
                unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]]):
            number_lines = len(
                unique_measurement_dates[history_plot_options["min_num"]:history_plot_options["max_num"]])
            date_device_history = device_history[device_history["Measurement_Timestamp"] == date]
            try:
                if not date_device_history.empty:
                    x_date = date_device_history['Frequency']
                    y_date = np.array(date_device_history[column_names[index]].tolist())
                    date_color = (1 - float(date_index + 1) / number_lines, 0, float(date_index + 1) / number_lines, .5)
                    ax.plot(x_date, y_date,
                            color=date_color, label=date)
            except:
                pass
        # ax.sharex(diff_axes[index])
        if history_plot_options["display_legend"]:
            if index == 1:
                ax.legend(loc="center left", bbox_to_anchor=(1.05, .5),
                          ncol=int(max([round(float(number_measurements) / 28.), 1])), shadow=True,
                          title="Measurement Dates", fancybox=True)
    compare_axes.flat[-2].set_xlabel('Frequency(GHz)', color='k')
    compare_axes.flat[-1].set_xlabel('Frequency(GHz)', color='k')
    fig.subplots_adjust(hspace=0)
    plt.tight_layout()
    fig.suptitle(device_id + "\n", fontsize=18, fontweight='bold', y=1.05, )
    # Dealing with the save option
    if history_plot_options["file_name"] is None:
        file_name = auto_name(specific_descriptor=history_plot_options["specific_descriptor"],
                              general_descriptor=history_plot_options["general_descriptor"],
                              directory=history_plot_options["directory"], extension='png', padding=3)
    else:
        file_name = history_plot_options["file_name"]
    if history_plot_options["save_plot"]:
        # print file_name
        plt.savefig(os.path.join(history_plot_options["directory"], file_name))
    else:
        plt.show()
    return fig

def plot_raw_MUF_comparison(raw_directory=r"C:\Share\35CalComp\35_ascii_results",
                            measurement_names=['N101P1.L1_030716', 'N101P2.L1_030716'],
                            nominal_path=r"C:\Share\35CalComp\MUF_results\DUTs\N101P1_Support\N101P1_0.s2p",
                            sensitivity_directory=r"C:\Share\35CalComp\MUF_results\DUTs\N101P1_Support\Covariance",
                            montecarlo_directory=r"C:\Share\35CalComp\MUF_results\DUTs\N101P1_Support\MonteCarlo",
                            **options):
    """Plots a comparison of results form the Microwave Uncertainty Framework and calrep given a raw file, nominal file,
    a sensitivity directory and a montecarlo directory.
    """

    # deal with options
    defaults = {"save_plots": False}
    comparison_options = {}
    for key, value in defaults.items():
        comparison_options[key] = value
    for key, value in comparison_options.items():
        comparison_options[key] = value
    # load files into python classes
    model_name = sparameter_power_type(os.path.join(raw_directory, measurement_names[0]))
    print(model_name)
    # raw_type(os.path.join(raw_directory,'M105P1.L1_030716'))
    model = globals()[model_name]
    measurements = [model(os.path.join(raw_directory, x)) for x in measurement_names]
    calrep_measurements = [calrep(x) for x in measurements]
    montecarlo_reference_curve = create_monte_carlo_reference_curve(monte_carlo_directory=montecarlo_directory,
                                                                    format="MA")
    sensitivity_reference_curve = create_sensitivity_reference_curve(nominal_file_path=nominal_path,
                                                                     sensitivity_directory=sensitivity_directory,
                                                                     format="MA")
    print(("-" * 80))
    print(("{0}".format(measurements[0].metadata["Device_Id"])))

    # update global preferences
    plt.rcParams.update({'font.size': 22, 'figure.figsize': (12, 6)})

    # for one-port
    if re.search("one", model_name, re.IGNORECASE):
        combined_figure, axes = plt.subplots(nrows=1, ncols=2)
        # Now plot all of these together at once mag first
        data_list = measurements + [sensitivity_reference_curve, montecarlo_reference_curve]
        labels = []
        for index, data in enumerate(data_list):
            if index == len(data_list) - 1:
                labels.append("Montecarlo")
            elif index == len(data_list) - 2:
                labels.append("Nominal")
            else:
                labels.append("Measurement {0}".format(index + 1))
        for index, data in enumerate(data_list):
            axes[0].plot(data["Frequency"], data["magS11"], label=labels[index])

        # now phase

        for index, data in enumerate(data_list):
            axes[1].plot(data["Frequency"], data["argS11"], label=labels[index])
        axes[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    else:
        combined_figure, axes = plt.subplots(nrows=3, ncols=2)
        data_list = measurements + [sensitivity_reference_curve, montecarlo_reference_curve]
        labels = []
        for index, data in enumerate(data_list):
            if index == len(data_list) - 1:
                labels.append("Montecarlo")
            elif index == len(data_list) - 2:
                labels.append("Nominal")
            else:
                labels.append("Measurement {0}".format(index + 1))
        parameters = ["S11", "S21", "S22"]
        for plot_index, plot_row in enumerate(axes):
            # Now plot all of these together at once mag first
            for index, data in enumerate(data_list):
                plot_row[0].plot(data["Frequency"], data["mag" + parameters[plot_index]], label=labels[index])
            # now phase
            for index, data in enumerate(data_list):
                plot_row[1].plot(data["Frequency"], data["arg" + parameters[plot_index]], label=labels[index])
            if plot_index == 1:
                plot_row[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))


                # plot the difference with uncertainties

    plt.tight_layout()

    if re.search("One", model_name, re.IGNORECASE):
        # now the difference of mag for measurement one
        montecarlo_mag = np.array(montecarlo_reference_curve["magS11"])
        montecarlo_uncertainty = np.array(montecarlo_reference_curve["umagS11"])
        measurement_1_mag = np.array(calrep_measurements[0]["magS11"])
        measurement_1_uncertainty = np.array(calrep_measurements[0]["uMgS11"])
        nominal_mag = np.array(sensitivity_reference_curve["magS11"])
        nominal_uncertainty = np.array(sensitivity_reference_curve["umagS11"])
        difference_figure, difference_axes = plt.subplots(nrows=1, ncols=2)
        difference_axes[0].plot(sensitivity_reference_curve["Frequency"],
                                measurement_1_mag - nominal_mag, label="Difference of Nominal and Calrep")
        difference_axes[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * nominal_uncertainty,
                                        nominal_uncertainty,
                                        color="blue",
                                        alpha=.25,
                                        edgecolor="black", label="Sensitivity Uncertainty")
        difference_axes[0].plot(montecarlo_reference_curve["Frequency"], measurement_1_mag - montecarlo_mag,
                                label="Difference of Montecarlo mean and Calrep")
        difference_axes[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * montecarlo_uncertainty,
                                        montecarlo_uncertainty,
                                        color="black",
                                        alpha=.25,
                                        edgecolor="black", label="Montecarlo Uncertainty")
        difference_axes[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * measurement_1_uncertainty,
                                        measurement_1_uncertainty,
                                        color="red",
                                        alpha=.25,
                                        edgecolor="red", label="Calrep Uncertainty")
        montecarlo_arg = np.array(montecarlo_reference_curve["argS11"])
        montecarlo_arg_uncertainty = np.array(montecarlo_reference_curve["uargS11"])
        measurement_1_arg = np.array(calrep_measurements[0]["argS11"])
        measurement_1_arg_uncertainty = np.array(calrep_measurements[0]["uAgS11"])
        nominal_arg = np.array(sensitivity_reference_curve["argS11"])
        nominal_arg_uncertainty = np.array(sensitivity_reference_curve["uargS11"])
        difference_axes[1].plot(sensitivity_reference_curve["Frequency"],
                                measurement_1_arg - nominal_arg,
                                label="Difference of Nominal ")
        difference_axes[1].fill_between(sensitivity_reference_curve["Frequency"], -1 * nominal_arg_uncertainty,
                                        nominal_arg_uncertainty,
                                        color="blue",
                                        alpha=.25,
                                        edgecolor="black", label="Sensitivity Uncertainty")
        difference_axes[1].plot(montecarlo_reference_curve["Frequency"], measurement_1_arg - montecarlo_arg,
                                label="Difference of Montecarlo ")
        difference_axes[1].fill_between(sensitivity_reference_curve["Frequency"],
                                        -1 * montecarlo_arg_uncertainty, montecarlo_arg_uncertainty,
                                        color="black",
                                        alpha=.25,
                                        edgecolor="black", label="Montecarlo Uncertainty")
        difference_axes[1].fill_between(sensitivity_reference_curve["Frequency"],
                                        -1 * measurement_1_arg_uncertainty, measurement_1_arg_uncertainty,
                                        color="red",
                                        alpha=.25,
                                        edgecolor="red", label="Calrep Uncertainty")

        difference_axes[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
        difference_axes[1].set_ylim(ymin=-5, ymax=5)
        difference_axes[0].set_ylim(ymin=-.025, ymax=.025)
    else:
        parameters = ["S11", "S21", "S22"]
        difference_figure, difference_axes = plt.subplots(nrows=3, ncols=2)
        for plot_index, plot_row in enumerate(difference_axes):
            parameter = parameters[plot_index]
            montecarlo_mag = np.array(montecarlo_reference_curve["mag" + parameter])
            montecarlo_uncertainty = np.array(montecarlo_reference_curve["umag" + parameter])
            measurement_1_mag = np.array(calrep_measurements[0]["mag" + parameter])
            measurement_1_uncertainty = np.array(calrep_measurements[0]["uMg" + parameter])
            nominal_mag = np.array(sensitivity_reference_curve["mag" + parameter])
            nominal_uncertainty = np.array(sensitivity_reference_curve["umag" + parameter])
            plot_row[0].plot(sensitivity_reference_curve["Frequency"],
                             measurement_1_mag - nominal_mag, label="Difference of Nominal and Calrep")
            plot_row[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * nominal_uncertainty,
                                     nominal_uncertainty,
                                     color="blue",
                                     alpha=.25,
                                     edgecolor="black", label="Sensitivity Uncertainty")
            plot_row[0].plot(montecarlo_reference_curve["Frequency"], measurement_1_mag - montecarlo_mag,
                             label="Difference of Montecarlo mean and Calrep")
            plot_row[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * montecarlo_uncertainty,
                                     montecarlo_uncertainty,
                                     color="black",
                                     alpha=.25,
                                     edgecolor="black", label="Montecarlo Uncertainty")
            plot_row[0].fill_between(sensitivity_reference_curve["Frequency"], -1 * measurement_1_uncertainty,
                                     measurement_1_uncertainty,
                                     color="red",
                                     alpha=.25,
                                     edgecolor="red", label="Calrep Uncertainty")
            montecarlo_arg = np.array(montecarlo_reference_curve["arg" + parameter])
            montecarlo_arg_uncertainty = np.array(montecarlo_reference_curve["uarg" + parameter])
            measurement_1_arg = np.array(calrep_measurements[0]["arg" + parameter])
            measurement_1_arg_uncertainty = np.array(calrep_measurements[0]["uAg" + parameter])
            nominal_arg = np.array(sensitivity_reference_curve["arg" + parameter])
            nominal_arg_uncertainty = np.array(sensitivity_reference_curve["uarg" + parameter])
            plot_row[1].plot(sensitivity_reference_curve["Frequency"],
                             measurement_1_arg - nominal_arg,
                             label="Difference of Nominal ")
            plot_row[1].fill_between(sensitivity_reference_curve["Frequency"], -1 * nominal_arg_uncertainty,
                                     nominal_arg_uncertainty,
                                     color="blue",
                                     alpha=.25,
                                     edgecolor="black", label="Sensitivity Uncertainty")
            plot_row[1].plot(montecarlo_reference_curve["Frequency"], measurement_1_arg - montecarlo_arg,
                             label="Difference of Montecarlo ")
            plot_row[1].fill_between(sensitivity_reference_curve["Frequency"],
                                     -1 * montecarlo_arg_uncertainty, montecarlo_arg_uncertainty,
                                     color="black",
                                     alpha=.25,
                                     edgecolor="black", label="Montecarlo Uncertainty")
            plot_row[1].fill_between(sensitivity_reference_curve["Frequency"],
                                     -1 * measurement_1_arg_uncertainty, measurement_1_arg_uncertainty,
                                     color="red",
                                     alpha=.25,
                                     edgecolor="red", label="Calrep Uncertainty")
            if plot_index == 1:
                plot_row[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
                plot_row[0].set_ylim(ymin=-.0001, ymax=.0001)
                plot_row[1].set_ylim(ymin=-1.8, ymax=1.8)
            else:
                plot_row[1].set_ylim(ymin=-10, ymax=10)
                plot_row[0].set_ylim(ymin=-.025, ymax=.025)
    plt.tight_layout()
    plt.show()
    print(("-" * 80))
    # Return files if you need them later
    return [measurements, calrep_measurements, montecarlo_reference_curve, sensitivity_reference_curve]
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_average_one_port_sparameters():
    os.chdir(TESTS_DIRECTORY)
    table_list=[OnePortRawModel('OnePortRawTestFileAsConverted.txt') for i in range(3)]
    out_data=average_one_port_sparameters(table_list)
    out_table=OnePortRawModel(None,**{"data":out_data})
    #table_list[0].show()
    #out_table.show()
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
    ax0.plot(out_table.get_column('Frequency'),out_table.get_column('magS11'),'k--')
    ax0.plot(table_list[0].get_column('Frequency'),table_list[0].get_column('magS11'),'bx')
    ax0.set_title('Magnitude S11')
    ax1.plot(out_table.get_column('Frequency'),out_table.get_column('argS11'),'ro')
    ax1.plot(table_list[0].get_column('Frequency'),table_list[0].get_column('argS11'),'bx')
    ax1.set_title('Phase S11')
    plt.show()
    print(out_table)

def test_comparison(input_file=None):
    """test_comparison tests the raw_mean,difference and comparison plot functionality"""
    # Data sources, to be replaced as project_files in Django
    # Todo: These are not robust tests fix them?
    TWO_PORT_NR_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Two_Port_NR_Check_Standard.csv"
    COMBINED_ONE_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_One_Port_Check_Standard.csv"
    COMBINED_TWO_PORT_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Two_Port_Check_Standard.csv"
    COMBINED_POWER_CHKSTD_CSV=r"C:\Share\Converted_Check_Standard\Combined_Power_Check_Standard.csv"
    ONE_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\One_Port_DUT.csv"
    TWO_PORT_CALREP_CSV=r"C:\Share\Converted_DUT\Two_Port_DUT.csv"
    POWER_3TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_3Term_DUT.csv"
    POWER_4TERM_CALREP_CSV=r"C:\Share\Converted_DUT\Power_4Term_DUT.csv"
    history_dict={'1-port':pandas.read_csv(COMBINED_ONE_PORT_CHKSTD_CSV),
         '2-port':pandas.read_csv(COMBINED_TWO_PORT_CHKSTD_CSV),
         '2-portNR':pandas.read_csv(TWO_PORT_NR_CHKSTD_CSV),'power':pandas.read_csv(COMBINED_POWER_CHKSTD_CSV)}
    if input_file is None:
        #input_file=r"C:\Share\Ck_Std_raw_ascii\C07207.D1_030298"
        input_file=r"C:\Share\Ck_Std_raw_ascii\C07207.D9_042500"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\C07208.A10_081507"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\CTNP20.R1_032310"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\CN49.K2_050608"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\C22P13.H4_043015"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\C24N07.L1_070998"
        #input_file=r"C:\Share\Ck_Std_raw_ascii\CTN208.A1_011613"
    start_time=datetime.datetime.now()
    file_model=sparameter_power_type(input_file)
    model=globals()[file_model]
    table=model(input_file)
    #print table
    #table.metadata["System_Id"]
    options={"Device_Id":table.metadata["Device_Id"], "System_Id":table.metadata["System_Id"],"Measurement_Timestamp":None,
                  "Connector_Type_Measurement":table.metadata["Connector_Type_Measurement"],
                 "Measurement_Date":None,"Measurement_Time":None}
    if re.search('2-port',table.metadata["Measurement_Type"],re.IGNORECASE) and not re.search('2-portNR',table.metadata["Measurement_Type"],re.IGNORECASE):
        history_key='2-port'
        options["column_names"]=['Frequency','magS11','argS11','magS21','argS21','magS22','argS22']
    elif re.search('2-portNR',table.metadata["Measurement_Type"],re.IGNORECASE):
        history_key='2-portNR'
        options["column_names"]=['Frequency','magS11','argS11','magS12','argS12','magS21','argS21','magS22','argS22']
    elif re.search('1-port',table.metadata["Measurement_Type"],re.IGNORECASE):
        history_key='1-port'
        if COMBINE_S11_S22:
             options["column_names"]=['Frequency','magS11','argS11']
        else:
            options["column_names"]=['Frequency','magS11','argS11','magS22','argS22']
    elif re.search('Dry Cal|Thermistor|power',table.metadata["Measurement_Type"],re.IGNORECASE):
        history_key='power'
        options["column_names"]=['Frequency','magS11','argS11','Efficiency','Calibration_Factor']
    #print history[history_key][:5]
    print(history_key)
    mean_frame=mean_from_history(history_dict[history_key].copy(),**options)
    #print mean_frame
    difference_frame=raw_difference_frame(table,mean_frame)
    #print difference_frame
    stop_time=datetime.datetime.now()
    plot_options={"display_difference":False,"display_mean":True,"display_raw":True,"display_legend":False}
    raw_comparison_plot_with_residuals(table,mean_frame,difference_frame,**plot_options)
    #stop_time=datetime.datetime.now()
    diff=stop_time-start_time
    print(("It took {0} seconds to process".format(diff.total_seconds())))

def test_compare_s2p_plots(file_list=["thru.s2p",'20160301_30ft_cable_0.s2p','TwoPortTouchstoneTestFile.s2p']):
    """Tests the compare_s2p_plots function"""
    os.chdir(TESTS_DIRECTORY)
    tables=[S2PV1(file_name) for file_name in file_list]
    format="MA"
    compare_s2p_plots(tables,format=format)
    format="DB"
    compare_s2p_plots(tables,format=format,display_legend=False)
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_average_one_port_sparameters()
    #test_comparison()
    test_compare_s2p_plots()