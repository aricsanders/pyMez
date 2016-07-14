#-----------------------------------------------------------------------------
# Name:        SParameter.py
# Purpose:    Tools to analyze SParameter Data
# Author:      Aric Sanders
# Created:     4/13/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Sparameter is a module with tools for analyzing Sparameter data """
#-----------------------------------------------------------------------------
# Standard Imports
import os
import re
import datetime
import sys
print sys.path
#-----------------------------------------------------------------------------
# Third Party Imports
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
    #import pyMeasure.Code.DataHandlers.NISTModels
    #from pyMeasure.Code.DataHandlers.NISTModels import *
    from pyMeasure import *
except:
    print("The module pyMeasure.Code.DataHandlers.NISTModels was not found,"
          "please put it on the python path")
    raise ImportError
try:
    import matplotlib.pyplot as plt
except:
    print("The module matplotlib was not found,"
          "please put it on the python path")
#-----------------------------------------------------------------------------
# Module Constants

# Does this belong in tests or a Data folder
ONE_PORT_DUT=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')
#-----------------------------------------------------------------------------
# Module Functions
def one_port_robin_comparision_plot(input_asc_file,input_res_file,**options):
    """one_port_robin_comparision_plot plots a one port.asc file against a given .res file,
    use device_history=True in options to show device history"""
    defaults={"device_history":False,"mag_res":False}
    plot_options={}
    for key,value in defaults.iteritems():
        plot_options[key]=value
    for key,value in options.iteritems():
        plot_options[key]=value
    history=np.loadtxt(input_res_file,skiprows=1)
    column_names=["Frequency",'mag','arg','magS11N','argS11N','UmagS11N','UargS11N']
    options={"data":history.tolist(),"column_names":column_names,"column_types":['float' for column in column_names]}
    history_table=AsciiDataTable(None,**options)
    table=OnePortCalrepModel(input_asc_file)
    if plot_options["device_history"]:
        history_frame=pandas.read_csv(ONE_PORT_DUT)
        device_history=history_frame[history_frame["Device_Id"]==table.header[0].rstrip().lstrip()]
    fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)

    ax0.errorbar(history_table.get_column('Frequency'),history_table.get_column('magS11N'),fmt='k--',
                yerr=history_table.get_column('UmagS11N'),label="History")
    ax0.errorbar(table.get_column('Frequency'),table.get_column('mag'),
        yerr=table.get_column('uMg'),fmt='ro',label="Current Measurement",alpha=.3)
    if plot_options["device_history"]:
        ax0.errorbar(device_history['Frequency'].tolist(),device_history['mag'].tolist(),fmt='bs',
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

def average_one_port_sparameters(table_list,**options):
    """Returns a table that is the average of the Sparameters in table list. The new table will have all the unique
    frequency values contained in all of the tables. Tables must be in Real-Imaginary format or magnitude-angle format
    do not try to average db-angle format. """
    #This will work on any table that the data is stored in data, need to add a sparameter version
    defaults={"frequency_selector":0,"frequency_column_name":"Frequency"}
    average_options={}
    for key,value in defaults.iteritems():
        average_options[key]=value
    for key,value in options.iteritems():
        average_options[key]=value
    frequency_list=[]
    average_data=[]
    for table in table_list:
        frequency_list=frequency_list+table.get_column("Frequency")
    unique_frequency_list=sorted(list(set(frequency_list)))
    for frequency in unique_frequency_list:
        new_row=[]
        for table in table_list:
            data_list=filter(lambda x: x[average_options["frequency_selector"]]==frequency,table.data)
            table_average=np.mean(np.array(data_list),axis=0)
            new_row.append(table_average)
            #print new_row
        average_data.append(np.mean(new_row,axis=0).tolist())
    return average_data

def two_port_comparision_plot_with_residuals(two_port_raw,mean_frame,difference_frame):
    """Creates a comparision plot given a TwoPortRawModel object and a pandas.DataFrame mean frame"""
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
             "Measurement_Date":None,"Measurement_Time":None,
              "column_names":['Frequency','magS11','argS11']}
    mean_options={}
    for key,value in defaults.iteritems():
        mean_options[key]=value
    for key,value in options.iteritems():
            mean_options[key]=value

    filters=["Device_Id","System_Id","Measurement_Timestamp","Connector_Type_Measurement",
             "Measurement_Date","Measurement_Time"]
    temp_frame=history_frame.copy()
    for index,filter_type in enumerate(filters):
        if mean_options[filter_type] is not None:
            temp_frame=temp_frame[temp_frame[filter_type]==mean_options[filter_type]]
#     temp_frame=temp_frame[temp_frame["Device_Id"]==mean_options["Device_Id"]]
#     temp_frame=temp_frame[temp_frame["System_Id"]==mean_options["System_Id"]]
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

def raw_difference_frame(raw_model,mean_frame,**options):
    """Creates a difference pandas.DataFrame given a raw NIST model and a mean pandas.DataFrame"""
    defaults={"column_names":mean_frame.columns.tolist()}
    difference_options={}
    for key,value in defaults.iteritems():
        difference_options[key]=value
    for key,value in options.iteritems():
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

def raw_comparision_plot_with_residuals(raw_nist,mean_frame,difference_frame,**options):
    """Creates a comparision plot given a RawModel object and a pandas.DataFrame mean frame and difference frame"""
    defaults={"display_mean":True,
              "display_difference":True,
              "display_raw":True,
              "display_legend":True,
              "save_plot":False,
              "directory":None,
              "specific_descriptor":raw_nist.metadata["Device_Id"]+"_Check_Standard",
              "general_descriptor":"Plot","file_name":None}
    comparison_plot_options={}
    for key,value in defaults.iteritems():
        comparison_plot_options[key]=value
    for key,value in options.iteritems():
        comparison_plot_options[key]=value
    column_names=mean_frame.columns.tolist()
    number_rows=len(column_names)/2
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
    print out_table
def test_comparison(input_file=None):
    """test_comparision tests the raw_mean,difference and comparison plot functionality"""
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
             options["column_names"]=['Frequency','mag','arg']
        else:
            options["column_names"]=['Frequency','magS11','argS11','magS22','argS22']
    elif re.search('Dry Cal|Thermistor|power',table.metadata["Measurement_Type"],re.IGNORECASE):
        history_key='power'
        options["column_names"]=['Frequency','magS11','argS11','Efficiency','Calibration_Factor']
    #print history[history_key][:5]
    print history_key
    mean_frame=mean_from_history(history_dict[history_key].copy(),**options)
    #print mean_frame
    difference_frame=raw_difference_frame(table,mean_frame)
    #print difference_frame
    stop_time=datetime.datetime.now()
    plot_options={"display_difference":False,"display_mean":True,"display_raw":True,"display_legend":False}
    raw_comparision_plot_with_residuals(table,mean_frame,difference_frame,**plot_options)
    #stop_time=datetime.datetime.now()
    diff=stop_time-start_time
    print("It took {0} seconds to process".format(diff.total_seconds()))

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_average_one_port_sparameters()
    test_comparison()