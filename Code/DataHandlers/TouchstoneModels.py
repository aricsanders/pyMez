#-----------------------------------------------------------------------------
# Name:        TouchstoneModels
# Purpose:     To store and manipulate touchstone files
# Author:      Aric Sanders
# Created:     3/7/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A module dedicated to the manipulation and storage of touchstone files, such as
 .s2p or .ts files. Touchstone files are normally s-parameter data for multiport VNA's
 This module handles all SNP's and different formats such as MA, DB, RI. It currently does
 not support T, Y, and Z transformations. On 11/15/2016 the sparameter_data attribute was
 changed to data to align better with other class models.

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
import cmath
import math
import sys
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Utils.Alias import *
    METHOD_ALIASES=1
    "Constant that is set to True if Method Alias is available."
except:
    print("The module pyMez.Code.Utils.Alias was not found")
    METHOD_ALIASES=0
    pass
try:
    from Code.DataHandlers.GeneralModels import *
except:
    print("The module pyMez.Code.DataHandlers.GeneralModels was not found,"
          "please put it on the python path")
    raise ImportError
try:
    import numpy as np
except:
    print("The module numpy was not found,"
          "please put it on the python path")
    raise ImportError
import matplotlib.pyplot as plt
# try:
#     import smithplot
#     SMITHPLOT=1
#     "Constant assigned as true if the module smithplot is present, this module is currently broken"
#
# except:
#     print("The module smithplot was not found,"
#           "please put it on the python path")
#     SMITHPLOT=0
#-----------------------------------------------------------------------------
# Module Constants
TOUCHSTONE_KEYWORDS=["Version","Number of Ports","Two-Port Order","Number of Frequencies",
                     "Number of Noise Frequencies","Reference","Matrix Format","Mixed-Mode Order",
                     "Network Data","Noise Data","End"]
"""Keywords for version 2 touchstone files, not currently implemented """
OPTION_LINE_PATTERN="#[\s]+(?P<Frequency_Units>\w+)[\s]+(?P<Parameter>\w+)[\s]+(?P<Format>\w+)[\s]+R[\s]+(?P<Reference_Resistance>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"
"Regular expression string for the option line in touchstone files (# GHz S RI R 50)"
COMMENT_PATTERN="![\s]*(?P<Comment>.+)\n"
"Regular expression for comments in touchstone files."
EXTENSION_PATTERN="s(?P<Number_Ports>\d+)p"
"Regular expresion for snp extensions."
FREQUENCY_UNITS=["Hz","kHz","MHz","GHz"]
"Common frequency units .in touchstone files"
PARAMETERS=["S","Y","Z","G","H"]
"Network parameters found in touchstone files"
FORMATS=["RI","DB","MA"]
"Format codes found in touchstone files."
S1P_MA_COLUMN_NAMES=["Frequency","magS11","argS11"]
S1P_DB_COLUMN_NAMES=["Frequency","dbS11","argS11"]
S1P_RI_COLUMN_NAMES=["Frequency","reS11","imS11"]
S2P_MA_COLUMN_NAMES=["Frequency","magS11","argS11","magS21","argS21","magS12","argS12","magS22","argS22"]
S2P_DB_COLUMN_NAMES=["Frequency","dbS11","argS11","dbS21","argS21","dbS12","argS12","dbS22","argS22"]
S2P_RI_COLUMN_NAMES=["Frequency","reS11","imS11","reS21","imS21","reS12","imS12","reS22","imS22"]
# Todo: Make the descriptions dictionaries and cycle through them in the model
S2P_MA_COLUMN_DESCRIPTION=["Frequency","magS11","argS11","magS21","argS21","magS12","argS12","magS22","argS22"]
S2P_DB_COLUMN_DESCRIPTION=["Frequency","dbS11","argS11","dbS21","argS21","dbS12","argS12","dbS22","argS22"]
S2P_RI_COLUMN_DESCRIPTION=["Frequency","reS11","imS11","reS21","imS21","reS12","imS12","reS22","imS22"]
S2P_COMPLEX_COLUMN_NAMES=["Frequency","S11","S21","S12","S22"]
S2P_NOISE_PARAMETER_COLUMN_NAMES=["Frequency","NFMin","mag","arg","Rn"]
# value to assign to any thing that is 0
MINIMUM_DB_VALUE=-200
"Decibel value assigned to any linear value that is zero in a touchstone file"
MINIMUM_DB_ARG_VALUE=0
"Value assigned to the phase of a zero linear value in a touchstone file"

#-----------------------------------------------------------------------------
# Module Functions
def print_s1p_attributes(new_table):
    """prints some important attributes of s1p table"""
    print("The attributes for the table as read in are")
    print(("-"*80))
    print(("The attribute {0} is {1}".format('data',str(new_table.data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('comments',str(new_table.comments))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('option_line',str(new_table.option_line))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('format',str(new_table.format))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('column_names',str(new_table.column_names))))
    print(("-"*80))

def print_s2p_attributes(new_table):
    """prints some important attributes of s2p table"""
    print("The attributes for the table as read in are")
    print(("-"*80))
    print(("The attribute {0} is {1}".format('data',str(new_table.data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('noiseparameter_data',str(new_table.noiseparameter_data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('comments',str(new_table.comments))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('option_line',str(new_table.option_line))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('format',str(new_table.format))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('column_names',str(new_table.column_names))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('noiseparameter_column_names',str(new_table.noiseparameter_column_names))))
def print_snp_attributes(new_table):
    """prints some important attributes of snp table"""
    print("The attributes for the table as read in are")
    print(("-"*80))
    print(("The attribute {0} is {1}".format('data',str(new_table.data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('noiseparameter_data',str(new_table.noiseparameter_data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('comments',str(new_table.comments))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('option_line',str(new_table.option_line))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('format',str(new_table.format))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('column_names',str(new_table.column_names))))
    print(("-"*80))
    print(("-"*80))
    print(("-"*80))

def make_row_match_string(column_names,delimiter_pattern='[\s,]+'):
    """Returns a regex string for matching a row given a set of column names assuming the row delimiter
    is a set of white spaces (default) or a specified delimiter pattern.
    Designed to create a regex for the input of numbers"""
    row_regex_string="(?:^|[\s]+)"
    for index,name in enumerate(column_names):
        if index == len(column_names)-1:
            row_regex_string=row_regex_string+'(?P<%s>{0})'%name
        else:
            row_regex_string=row_regex_string+'(?P<%s>{0})'%name+delimiter_pattern
    row_regex_string=row_regex_string.format(NUMBER_MATCH_STRING)
    return row_regex_string

def build_row_formatter(precision=None,number_columns=None):
    """Builds a uniform row_formatter_string given a precision and a number of columns"""
    row_formatter=""
    if precision is None:
        precision=4
    for i in range(number_columns):
        if i==number_columns-1:
            row_formatter=row_formatter+"{"+str(i)+":.%sg}"%precision
        else:
            row_formatter=row_formatter+"{"+str(i)+":.%sg}{delimiter}"%precision
    return row_formatter

def build_snp_row_formatter(number_ports=2,precision=None,number_columns=None):
    """Builds a uniform row_formatter_string given a precision and a number of columns
    for a snp file. If number_ports is 1,2 all sparameters are assumed to be on a single line
     if it is 3,4 it is assumed to be in a matrix format, if >4 it is assumed to be 4 sparameters
     on a line with the first line containing frequency"""
    number_rows_per_frequency=number_ports**2/4
    row_formatter=""
    if precision is None:
        precision=10
    for i in range(number_columns):
        if i==number_columns-1:
            row_formatter=row_formatter+"{"+str(i)+":.%sg}"%precision
        else:
            row_formatter=row_formatter+"{"+str(i)+":.%sg}{delimiter}"%precision
    return row_formatter

def number_ports_from_file_name(file_name):
    "Returns the number of ports as an integer from a file_name."
    match=re.search(EXTENSION_PATTERN,file_name.split(".")[-1],re.IGNORECASE)
    number_ports=match.groupdict()["Number_Ports"]
    return int(number_ports)

def build_snp_column_names(number_of_ports=2,format="RI"):
    """Return a list of column names based on the format and number of ports. Enter
    number_or_ports as a integer and format as text string such as 'RI','MA' or 'DB'"""
    column_names=["Frequency"]
    prefix_1=""
    prefix_2=""
    if re.search('ri',format,re.IGNORECASE):
        prefix_1="re"
        prefix_2="im"
    elif re.search('ma',format,re.IGNORECASE):
        prefix_1="mag"
        prefix_2="arg"
    elif re.search('db',format,re.IGNORECASE):
        prefix_1="db"
        prefix_2="arg"
    else:
        raise TypeError("format must be RI, DB or MA")
    for i in range(number_of_ports):
        for j in range(number_of_ports):
            column_names.append(prefix_1+"S"+str(i+1)+str(j+1))
            column_names.append(prefix_2+"S"+str(i+1)+str(j+1))
    if number_of_ports==2:
        #switch S21 and S12
        [S12_1,S12_2,S21_1,S21_2]=column_names[3:7]
        column_names[3:7]=[S21_1,S21_2,S12_1,S12_2]
    return column_names

def build_parameter_column_names(number_of_ports=2,format="RI",parameter="S"):
    """Return a list of column names based on the format and number of ports. Enter
    number_or_ports as a integer and format as text string such as 'RI','MA' or 'DB'"""
    column_names=["Frequency"]
    prefix_1=""
    prefix_2=""
    if re.search('ri',format,re.IGNORECASE):
        prefix_1="re"
        prefix_2="im"
    elif re.search('ma',format,re.IGNORECASE):
        prefix_1="mag"
        prefix_2="arg"
    elif re.search('db',format,re.IGNORECASE):
        prefix_1="db"
        prefix_2="arg"
    else:
        raise TypeError("format must be RI, DB or MA")
    for i in range(number_of_ports):
        for j in range(number_of_ports):
            column_names.append(prefix_1+parameter+str(i+1)+str(j+1))
            column_names.append(prefix_2+parameter+str(i+1)+str(j+1))
    if number_of_ports==2:
        #switch S21 and S12
        [S12_1,S12_2,S21_1,S21_2]=column_names[3:7]
        column_names[3:7]=[S21_1,S21_2,S12_1,S12_2]
    return column_names


def combine_segments(segment_list):
    """Combines a list of lists that are segments (each segment is list of strings)
    and returns a single list of strings, segments are assumed to be the same length"""
    combined_list=[]
    for index,row in enumerate(segment_list[0]):
        new_row=""
        for segment in segment_list:
            new_row=new_row+segment[index]
        combined_list.append(new_row)
    return combined_list

def parse_combined_float_list(float_string_list):
    """Parses a list of strings, where each element of the list is a single string which is a list of floats
    to be parsed.
    Assumes the data delimiter is whitespace or comma,
    and removes any white space at the beginning and end of the string
    all values data types are assumed to be floats returned as floats"""
    parsed_data=[]
    for row in float_string_list:
        new_row=[float(x) for x in re.split("[\s|,]+",row.rstrip().lstrip().replace("\n","\t"))]
        parsed_data.append(new_row)
    return parsed_data

def s2p_mean(list_s2p_models,**options):
    """Calculates the mean of the data of a list of
    s2p model and returns a new s2p model. The formats should be the same. Note this is very slow for large number
   of s2ps"""
    #This will work on any table that the data is stored in data, need to add a sparameter version
    defaults={"frequency_selector":0,"frequency_column_name":"Frequency"}
    average_options={}
    for key,value in defaults.items():
        average_options[key]=value
    for key,value in options.items():
        average_options[key]=value
    frequency_list=[]
    average_data=[]
    for table in list_s2p_models:
        frequency_list=frequency_list+table.get_column("Frequency")
    unique_frequency_list=sorted(list(set(frequency_list)))
    for frequency in unique_frequency_list:
        new_row=[]
        for table in list_s2p_models:
            data_list=[x for x in table.data if x[average_options["frequency_selector"]]==frequency]
            table_average=np.mean(np.array(data_list),axis=0)
            new_row.append(table_average)
            #print new_row
        average_data.append(np.mean(new_row,axis=0).tolist())
    average_options["data"]=average_data
    average_options["option_line"]=list_s2p_models[0].option_line
    new_s2p=S2PV1(None,**average_options)
    return new_s2p

def s2p_difference(s2p_one,s2p_two,**options):
    """Calculates the difference of two
    s2p models and returns a new s2p model. The Frequency values must all be the same,
    formats should all be the same"""
    list_s2p_models=[s2p_one,s2p_two]
    frequency_check=list_s2p_models[0].get_column("Frequency")
    for model in list_s2p_models:
        if model.get_column("Frequency")==frequency_check:
            pass
        else:
            raise TypeError("Frequencies must be of the same length")
    defaults={"frequency_selector":0,"frequency_column_name":"Frequency"}
    difference_options={}
    for key,value in defaults.items():
        difference_options[key]=value
    for key,value in options.items():
        difference_options[key]=value
    difference_data=[]
    for index,row in enumerate(s2p_one.data[:]):
        a=np.array(row)
        b=np.array(s2p_two.data[index])
        new_row=np.subtract(a,b)
        new_row=new_row.tolist()
        new_row[0]=row[0]
        difference_data.append(new_row)
    difference_options["data"]=difference_data
    difference_options["option_line"]=s2p_one.option_line
    new_s2p=S2PV1(None,**difference_options)
    return new_s2p

#-----------------------------------------------------------------------------
# Module Classes

# TODO: make a SNPBase class that has save, change_frequency_units,get_column, __str__, methods
# TODO: This doesnt work because .__init__ is so different for each class
class SNPBase():
    """SNPBase is a class with methods that are common across all the Touchstone models.
    It is only meant as a base class to inherit, not to instantiate by itself"""
    def __init__(self):
        pass

    def __str__(self):
        "Controls how the model displays when print and str are called"
        self.string=self.build_string()
        return self.string
    def add_comment(self,comment):
        """Adds a comment to the SNP file"""
        if self.comments is None:
            self.comments=[]
        if isinstance(comment, StringType):
            for old_comment in self.comments:
                if old_comment[2] == 0:
                    old_comment[1] += 1
            self.comments.append([comment,0,0])
            self.options["option_line_line"]+=1
            self.options["sparameter_begin_line"]+=1

        if isinstance(comment, ListType):
            if comment[1]==0:
                for old_comment in self.comments:
                    if old_comment[2]==0:
                        old_comment[1]+=1
                self.comments.append(comment)
                self.options["option_line_line"] += 1
                self.options["sparameter_begin_line"] += 1
            else:
                self.comments.append(comment)

    def save(self,file_path=None,**temp_options):
        """Saves the snp file to file_path with options, defaults to snp.path"""
        if file_path is None:
            file_path=self.path
        out_file=open(file_path,'w')
        out_file.write(self.build_string(**temp_options))
        out_file.close()

    def get_data_dictionary_list(self,use_row_formatter_string=True):
        """Returns a python list with a row dictionary of form {column_name:data_column} for sparameters only"""
        try:
            if self.options["sparameter_row_formatter_string"] is None:
                use_row_formatter_string=False
            if use_row_formatter_string:
                list_formatter=[item.replace("{"+str(index),"{0")
                                for index,item in enumerate(self.options["sparameter_row_formatter_string"].split("{delimiter}"))]
            else:
                list_formatter=["{0}" for i in self.column_names]
            out_list=[{self.column_names[i]:list_formatter[i].format(value) for i,value in enumerate(line)}
                      for line in self.data]
            return out_list
        except:raise

    def change_frequency_units(self,new_frequency_units=None):
        """Changes the frequency units from the current to new_frequency_units. Frequency units must be one
        an accepted scientific prefix, function is case sensitive (mHz=milli Hertz, MHz=Mega Hertz) """
        multipliers={"yotta":10.**24,"Y":10.**24,"zetta":10.**21,"Z":10.**21,"exa":10.**18,"E":10.**18,"peta":10.**15,
                     "P":10.**15,"tera":10.**12,"T":10.**12,"giga":10.**9,"G":10.**9,"mega":10.**6,"M":10.**6,
                     "kilo":10.**3,"k":10.**3,"hecto":10.**2,"h":10.**2,"deka":10.,"da":10.,None:1.,"":1.,
                     "deci":10.**-1,"d":10.**-1,"centi":10.**-2,"c":10.**-2,"milli":10.**-3,"m":10.**-3,
                     "micro":10.**-6,"mu":10.**-6,"\u00B5":10.**-6,"nano":10.**-9,
                     "n":10.**-9,"pico":10.**-12,"p":10.**-12,"femto":10.**-15,
                     "f":10.**-15,"atto":10.**-18,"a":10.**-18,"zepto":10.**-21,"z":10.**-21,
                     "yocto":10.**-24,"y":10.**-24}
        # change column name into column index
        old_prefix=re.sub('Hz','',self.frequency_units,flags=re.IGNORECASE)
        new_prefix=re.sub('Hz','',new_frequency_units,flags=re.IGNORECASE)
        unit='Hz'
        column_selector=0
        try:
            if old_prefix is None:
                old_prefix=""
            if new_prefix is None:
                new_prefix=""
            old_unit=old_prefix+unit
            new_unit=new_prefix+unit
            if column_selector in self.column_names:
                column_selector=self.column_names.index(column_selector)
            for index,row in enumerate(self.data[:]):
                if type(self.data[index][column_selector]) in [FloatType,LongType]:
                    #print "{0:e}".format(multipliers[old_prefix]/multipliers[new_prefix])
                    self.data[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.data[index][column_selector]
                    self.sparameter_complex[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.sparameter_complex[index][column_selector]
                elif type(self.data[index][column_selector]) in [StringType,IntType]:
                    self.data[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.data[index][column_selector]))
                    self.sparameter_complex[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.sparameter_complex[index][column_selector]))
                else:
                    print(type(self.data[index][column_selector]))
                    raise
            for index,row in enumerate(self.noiseparameter_data[:]):
                if type(self.noiseparameter_data[index][column_selector]) in [FloatType,LongType]:
                    #print "{0:e}".format(multipliers[old_prefix]/multipliers[new_prefix])
                    self.noiseparameter_data[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.noiseparameter_data[index][column_selector]
                elif type(self.noiseparameter_data[index][column_selector]) in [StringType,IntType]:
                    self.noiseparameter_data[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.noiseparameter_data[index][column_selector]))
                else:
                    print(type(self.noiseparameter_data[index][column_selector]))
                    raise
            old_unit_pattern=re.compile(old_unit,re.IGNORECASE)
            self.frequency_units=new_frequency_units
            self.option_line=re.sub(old_unit_pattern,new_unit,self.option_line)
            self.options["option_line"]=re.sub(old_unit_pattern,new_unit,self.option_line)
            if self.options["column_descriptions"] is not None:
                old=self.options["column_descriptions"][column_selector]
                self.options["column_descriptions"][column_selector]=old.replace(old_unit,new_unit)
            if self.options["column_units"] is not None:
                old=self.options["column_units"][column_selector]
                self.options["column_units"][column_selector]=old.replace(old_unit,new_unit)
            if re.search(old_unit,self.column_names[column_selector]):
                old=self.column_names[column_selector]
                self.column_names[column_selector]=old.replace(old_unit,new_unit)
        except:
            print(("Could not change the unit prefix of column {0}".format(column_selector)))
            raise


    def get_column(self,column_name=None,column_index=None):
        """Returns a column as a list given a column name or column index"""
        if column_name is None:
            if column_index is None:
                return
            else:
                column_selector=column_index
        else:
            column_selector=self.column_names.index(column_name)
        out_list=[self.data[i][column_selector] for i in range(len(self.data))]
        return out_list
    def __getitem__(self, items):
        """Controls how the model responds to self["Item"]"""
        out_data=[]
        column_selectors=[]
        #print items[0]
        if type(items) in [StringType,IntType]:
            if items in self.column_names:
                return self.get_column(column_name=items)
            elif items in ["data","data"]:
                return self.data
            elif items in ["sparameter_complex","complex_data"]:
                return self.sparameter_complex
            elif items in ["noiseparameter_data","noise"]:
                return self.noiseparameter_data
        else:
            for item in items:
                if isinstance(item, IntType):
                    column_selectors.append(item)
                else:
                    #print self.column_names
                    column_selectors.append(self.column_names.index(item))
            for row in self.data[:]:
                new_row=[]
                for selector in column_selectors:
                    new_row.append(row[selector])
                out_data.append(new_row)
            return out_data

    def show(self, **options):
        """Plots any table with frequency as its x-axis and column_names as the x-axis in a
        series of subplots"""
        defaults = {"display_legend": False,
                    "save_plot": False,
                    "directory": None,
                    "specific_descriptor": "Touchstone",
                    "general_descriptor": "Plot",
                    "file_name": None,
                    "plots_per_column": 2,
                    "plot_format": 'b-',
                    "share_x": False,
                    "subplots_title": True,
                    "plot_title": None,
                    "plot_size": (8, 6),
                    "dpi": 80,
                    "format": "MA",
                    "x_label": True,
                    "grid": True,
                    "silent":False}
        plot_options = {}
        for key, value in defaults.items():
            plot_options[key] = value
        for key, value in options.items():
            plot_options[key] = value

        current_format = self.format[:]
        if plot_options["format"]:
            if plot_options["format"] is current_format:
                pass
            elif re.search("R", plot_options["format"], re.IGNORECASE):
                self.change_data_format("RI")
            elif re.search("M", plot_options["format"], re.IGNORECASE):
                self.change_data_format("MA")
            elif re.search("D", plot_options["format"], re.IGNORECASE):
                self.change_data_format("DB")
        x_data = np.array(self["Frequency"])
        y_data_columns = self.column_names[:]
        y_data_columns.remove("Frequency")
        number_plots = len(y_data_columns)
        number_columns = plot_options["plots_per_column"]
        number_rows = int(round(float(number_plots) / float(number_columns)))
        figure, axes = plt.subplots(ncols=number_columns, nrows=number_rows, sharex=plot_options["share_x"],
                                    figsize=plot_options["plot_size"], dpi=plot_options["dpi"])
        for plot_index, ax in enumerate(axes.flat):
            if plot_index < number_plots:
                y_data = np.array(self[y_data_columns[plot_index]])
                ax.plot(x_data, y_data, plot_options["plot_format"], label=y_data_columns[plot_index])
                if plot_options["display_legend"]:
                    ax.legend()
                if plot_options["subplots_title"]:
                    ax.set_title(y_data_columns[plot_index])
                if plot_options["x_label"]:
                    ax.set_xlabel("Frequency ({0})".format(self.frequency_units))
                if plot_options["grid"]:
                    ax.grid()
            else:
                pass

        if plot_options["plot_title"]:
            plt.suptitle(plot_options["plot_title"])
        self.change_data_format(current_format)
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
        elif plot_options["silent"]:
            pass
        else:
            plt.show()
        return figure


class S1PV1(SNPBase):
    """A container for touchstone S1P. S1P are one port s-parameter files, with comments on any line
    began with ! and an option line in the format # GHz S RI R 50.0 that specifies the frequency units,
    stored parameter (default is S), data format (RI,MA or DB) and reference resistance data is 3 columns"""
    def __init__(self,file_path=None,**options):
        """Initialization of the s2p class for version 1 files,
        if a file path is specified, it opens and parses the file. If the file path is not
        specified then data can be added through the s2pv1.data. A reference to the version 1 touchstone
        format may be found at
        http://cp.literature.agilent.com/litweb/pdf/genesys200801/sim/linear_sim/sparams/touchstone_file_format.htm
        """
        defaults={"data_delimiter":"  ",
                  "column_names_delimiter":None,
                  "specific_descriptor":'One_Port',
                  "general_descriptor":'Sparameter',
                  "option_line_line":0,
                  "option_line":'# GHz S RI R 50',
                  "directory":None,
                  "extension":'s1p',
                  "metadata":None,
                  "column_descriptions":None,
                  "sparameter_row_formatter_string":build_row_formatter(10,3),
                  "data":[],
                  "sparameter_complex":[],
                  "noiseparameter_data":[],
                  "comments":[],
                  "path":None,
                  "column_units":None,
                  "sparameter_begin_line":1,
                  "sparameter_end_line":None

                  }
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        self.noiseparameter_data=[]
        SNPBase.__init__(self)
        self.elements=['data','comments','option_line']
        self.metadata=self.options["metadata"]
        if file_path is not None:
            self.path=file_path
            self.__read_and_fix__()
        else:
            for element in self.elements:
                self.__dict__[element]=self.options[element]
            self.sparameter_complex=self.options["sparameter_complex"]
            match=re.match(OPTION_LINE_PATTERN,self.option_line)
            # set the values associated with the option line
            for key,value in match.groupdict().items():
                self.__dict__[key.lower()]=value
            if re.match('db',self.format,re.IGNORECASE):
                self.column_names=S2P_DB_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_DB_COLUMN_NAMES)
            elif re.match('ma',self.format,re.IGNORECASE):
                self.column_names=S2P_MA_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_MA_COLUMN_NAMES)
            elif re.match('ri',self.format,re.IGNORECASE):
                self.column_names=S2P_RI_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_RI_COLUMN_NAMES)
            # now we handle the cases if data or sparameter_complex is specified
            if self.data is [] and self.sparameter_complex is[]:
                pass
            elif self.sparameter_complex in [[],None]:
                for row in self.data:
                    self.add_sparameter_complex_row(row)
                    #print("{0} is {1}".format("row",row))
            elif self.data in [[],None]:
                self.data=[[0,0,0] for row in self.sparameter_complex]
                #print self.data
                self.change_data_format(new_format=self.format)
            if self.comments is None:
                number_line_comments=0
            else:
                number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
            self.options["sparameter_begin_line"]=number_line_comments+1
            self.options["sparameter_end_line"]= self.options["sparameter_begin_line"]\
                                                 +len(self.data)+1

            if self.options["path"] is None:
                self.path=auto_name(self.options["specific_descriptor"],self.options["general_descriptor"],
                                    self.options['directory'],self.options["extension"])
            else:
                self.path=self.options["path"]

    def __read_and_fix__(self):
        """Reads a s2pv1 file and fixes any problems with delimiters. Since s2p files may use
        any white space or combination of white space as data delimiters it reads the data and creates
        a uniform delimter. This means a file saved with save() will not be the same as the original if the
        whitespace is not uniform. """
        default_option_line=self.options["option_line"]
        in_file=open(self.path,'r')
        # to keep the logic clean we will repeatedly cycle through self.lines
        # but in theory we could do it all on the line input stage
        self.lines=[]
        for line in in_file:
            self.lines.append(line)
        # now we need to collect and extract all the inline comments
        # There should be two types ones that have char position EOL, -1 or 0
        self.comments=collect_inline_comments(self.lines,begin_token="!",end_token="\n")
        # change all of them to be 0 or -1
        if self.comments is None:
            pass
        else:
            for index,comment in enumerate(self.comments):
                if comment[2]>1:
                    self.comments[index][2]=-1
                else:
                    self.comments[index][2]=0
        # Match the option line and set the attribute associated with them
        match=re.match(OPTION_LINE_PATTERN,default_option_line)
        self.option_line=default_option_line
        add_option_line=1
        for index,line in enumerate(self.lines):
            if re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE):
                #print line
                self.option_line=line.replace("\n","")
                self.options["option_line_line"]=index
                match=re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE)
                add_option_line=0


        for key,value in match.groupdict().items():
                    self.__dict__[key.lower()]=value
        if re.match('db',self.format,re.IGNORECASE):
            self.column_names=S1P_DB_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_DB_COLUMN_NAMES)
        elif re.match('ma',self.format,re.IGNORECASE):
            self.column_names=S1P_MA_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_MA_COLUMN_NAMES)
        elif re.match('ri',self.format,re.IGNORECASE):
            self.column_names=S1P_RI_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_RI_COLUMN_NAMES)
        # remove the comments
        stripped_lines=strip_inline_comments(self.lines,begin_token="!",end_token="\n")
        #print stripped_lines
        self.data=[]
        self.sparameter_complex=[]
        self.options["sparameter_begin_line"]=self.options["sparameter_end_line"]=0
        data_lines=[]
        for index,line in enumerate(stripped_lines):
            if re.search(self.row_pattern,line):
                data_lines.append(index)
                #print re.search(self.row_pattern,line).groupdict()
                row_data=re.search(self.row_pattern,line).groupdict()
                self.add_sparameter_row(row_data=row_data)
                self.add_sparameter_complex_row(row_data=row_data)
        if data_lines != []:
            self.options["sparameter_begin_line"]=min(data_lines)+add_option_line
            self.options["sparameter_end_line"]=max(data_lines)+add_option_line
        #print self.data

    def build_string(self,**temp_options):
        """Creates the output string"""
        #number of lines = option line + comments that start at zero + rows in sparameter data + rows in noise data
        original_options=self.options
        for key,value in temp_options.items():
            self.options[key]=value
        if self.comments is None:
            number_line_comments=0
        else:
            number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
        #print number_line_comments
        number_lines=1+number_line_comments+len(self.data)
        #print number_lines
        out_lines=["" for i in range(number_lines)]
        out_lines[self.options["option_line_line"]]=self.option_line
        # populate the line comments
        comment_lines=[]
        inline_comments=[]
        if self.comments != None:
            for comment in self.comments:
                if comment[2] == 0:
                    out_lines[comment[1]]="!"+comment[0]
                    comment_lines.append(comment[1])
                else:
                    inline_comments.append(comment)
        # now start writting data at first empty line after the option line
        for index,line in enumerate(out_lines):
            if index==self.options["option_line_line"]:
                pass
            elif index in comment_lines:
                pass
            elif self.data not in [[],None] and index>=self.options["sparameter_begin_line"] and index <=self.options["sparameter_end_line"]:
                # print out_lines
                #print index
                out_lines[index]=self.options["sparameter_row_formatter_string"].format(
                    delimiter=self.options["data_delimiter"],
                    *self.data[index-self.options["sparameter_begin_line"]])
        if inline_comments:
            for comment in inline_comments:
                out_lines=insert_inline_comment(out_lines,comment=comment[0],
                                                line_number=comment[1],
                                                string_position=comment[2],
                                                begin_token=self.options["inline_comment_begin"],
                                                end_token="")
        self.options=original_options
        return string_list_collapse(out_lines)

    def add_sparameter_row(self,row_data):
        """Adds data to the sparameter attribute, which is a list of s-parameters. The
        data can be a list of 5 real numbers
         or dictionary with appropriate column names, note column names are not case sensitive"""
        if isinstance(row_data, ListType):
            if len(row_data) == 3:
                    self.data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if isinstance(row_data, DictionaryType):
            new_row=[]
            for column_name in self.column_names:
                #print row_data
                new_row.append(float(row_data[column_name]))
            self.data.append(new_row)
        self.options["sparameter_end_line"]+=1

    def add_sparameter_complex_row(self,row_data):
        """Adds a row to the sparameter_complex attribute. This attribute stores the values of the sparameter table in
        complex form for easy conversion and manipulation. Row_data is assumed to be of the same form that would be
        given to add_sparameter_row"""

        if isinstance(row_data, ListType) and len(row_data)==3 and isinstance(row_data[1], ComplexType):
            self.sparameter_complex.append(row_data)
        else:
            row_data=self.sparameter_row_to_complex(row_data=row_data)
            self.sparameter_complex.append(row_data)

    def sparameter_row_to_complex(self,row_data=None,row_index=None):
        """Given a row_data string, row_data list, or row_data dictionary it converts the values of the sparameter to
         complex notation (complex types) and returns a single list with 5 elements [Frequency,S11,S21,S12,S22]"""
        if row_index is not None:
            row_data=self.data[row_index]
        if row_data is None:
            print("Could not convert row to complex, need a valid row_data string, list or dictionary or a row_index in "
                  "data")
        out_row=[]
        try:
            if isinstance(row_data, StringType):
                row_data=re.search(self.row_pattern,row_data).groupdict()
            elif isinstance(row_data, ListType):
                row_data={self.column_names[index]:row_data[index] for index in range(3)}
            if not isinstance(row_data, DictionaryType):
                raise
            row_data={key:float(value) for key,value in row_data.items()}
            # now row data is in dictionary form with known keys, the tranformation is only based on self.format
            if re.match('db',self.format,re.IGNORECASE):
                S11=cmath.rect(10.**(row_data["dbS11"]/20.),(math.pi/180.)*row_data["argS11"])
                out_row=[row_data["Frequency"],S11]
            elif re.match('ma',self.format,re.IGNORECASE):
                S11=cmath.rect(row_data["magS11"],(math.pi/180.)*row_data["argS11"])
                out_row=[row_data["Frequency"],S11]
            elif re.match('ri',self.format,re.IGNORECASE):
                S11=complex(row_data["reS11"],row_data["imS11"])
                out_row=[row_data["Frequency"],S11]
            return out_row
        except:
            print("Could not convert row to a complex row")
            raise



    def change_data_format(self,new_format=None):
        """Changes the data format to new_format. Format must be one of the following: 'DB','MA','RI'
        standing for Decibel-Angle, Magnitude-Angle or Real-Imaginary as per the touchstone specification
        all angles are in degrees."""
        old_format=self.format

        if re.match('db',new_format,re.IGNORECASE):
            self.format="DB"
            self.option_line=self.option_line.replace(old_format,"DB")
            self.column_names=S1P_DB_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_DB_COLUMN_NAMES)
            for row_index,row in enumerate(self.data):
                frequency=self.sparameter_complex[row_index][0]
                dbS11=20.*math.log(abs(self.sparameter_complex[row_index][1]),10.)
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                self.data[row_index]=[frequency,dbS11,argS11]

        elif re.match('ma',new_format,re.IGNORECASE):
            self.format="MA"
            self.option_line=self.option_line.replace(old_format,"MA")
            self.column_names=S1P_MA_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_MA_COLUMN_NAMES)
            for row_index,row in enumerate(self.data):
                frequency=self.sparameter_complex[row_index][0]
                magS11=abs(self.sparameter_complex[row_index][1])
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                self.data[row_index]=[frequency,magS11,argS11]

        elif re.match('ri',new_format,re.IGNORECASE):
            self.format="RI"
            self.option_line=self.option_line.replace(old_format,"RI")
            self.column_names=S1P_RI_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_RI_COLUMN_NAMES)
            for row_index,row in enumerate(self.data):
                frequency=self.sparameter_complex[row_index][0]
                reS11=self.sparameter_complex[row_index][1].real
                imS11=self.sparameter_complex[row_index][1].imag
                self.data[row_index]=[frequency,reS11,imS11]
        else:
            print("Could not change data format the specified format was not DB, MA, or RI")
            return




class S2PV1(SNPBase):
    """A container for s2p version 1 files. Files consist of comments, option line, S parameter data
     and noise parameter data"""
    def __init__(self,file_path=None,**options):
        """Initialization of the s2p class for version 1 files,
        if a file path is specified, it opens and parses the file. If the file path is not
        specified then data can be added through the s2pv1.data. A reference to the version 1 touchstone
        format may be found at
        http://cp.literature.agilent.com/litweb/pdf/genesys200801/sim/linear_sim/sparams/touchstone_file_format.htm
        """
        defaults={"data_delimiter":"  ",
                  "column_names_delimiter":None,
                  "specific_descriptor":'Two_Port',
                  "general_descriptor":'Sparameter',
                  "option_line_line":0,
                  "option_line":'# GHz S RI R 50',
                  "directory":None,
                  "extension":'s2p',
                  "metadata":None,
                  "column_descriptions":None,
                  "sparameter_row_formatter_string":build_row_formatter(None,9),
                  "nosieparameter_row_formatter_string":build_row_formatter(None,5),
                  "noiseparameter_data":[],
                  "data":[],
                  "sparameter_complex":[],
                  "comments":[],
                  "path":None,
                  "column_units":None,
                  "inline_comment_begin":"!",
                  "inline_comment_end":"",
                  "sparameter_begin_line":1,
                  "sparameter_end_line":None,
                  }
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        SNPBase.__init__(self)
        self.elements=['data','noiseparameter_data','comments','option_line']
        self.metadata=self.options["metadata"]
        self.noiseparameter_row_pattern=make_row_match_string(S2P_NOISE_PARAMETER_COLUMN_NAMES)+"\n"
        self.noiseparameter_column_names=S2P_NOISE_PARAMETER_COLUMN_NAMES
        if file_path is not None:
            self.path=file_path
            self.__read_and_fix__()
        else:
            for element in self.elements:
                self.__dict__[element]=self.options[element]
            self.sparameter_complex=self.options["sparameter_complex"]
            match=re.match(OPTION_LINE_PATTERN,self.option_line)
            # set the values associated with the option line
            for key,value in match.groupdict().items():
                self.__dict__[key.lower()]=value
            if re.match('db',self.format,re.IGNORECASE):
                self.column_names=S2P_DB_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_DB_COLUMN_NAMES)
            elif re.match('ma',self.format,re.IGNORECASE):
                self.column_names=S2P_MA_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_MA_COLUMN_NAMES)
            elif re.match('ri',self.format,re.IGNORECASE):
                self.column_names=S2P_RI_COLUMN_NAMES
                self.row_pattern=make_row_match_string(S2P_RI_COLUMN_NAMES)
            # now we handle the cases if data or sparameter_complex is specified
            if self.data is [] and self.sparameter_complex is[]:
                pass
            elif self.sparameter_complex in [[],None]:
                for row in self.data:
                    self.add_sparameter_complex_row(row)
                    #print("{0} is {1}".format("row",row))
            elif self.data in [[],None]:
                self.data=[[0,0,0,0,0,0,0,0,0] for row in self.sparameter_complex]
                #print self.data
                self.change_data_format(new_format=self.format)
            if self.comments is None:
                number_line_comments=0
            else:
                number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
            self.options["sparameter_begin_line"]=number_line_comments+1
            self.options["sparameter_end_line"]= self.options["sparameter_begin_line"]\
                                                 +len(self.data)+1

            if self.options["path"] is None:
                self.path=auto_name(self.options["specific_descriptor"],self.options["general_descriptor"],
                                    self.options['directory'],self.options["extension"])
            else:
                self.path=self.options["path"]

    def __read_and_fix__(self):
        """Reads a s2pv1 file and fixes any problems with delimiters. Since s2p files may use
        any white space or combination of white space as data delimiters it reads the data and creates
        a uniform delimter. This means a file saved with save() will not be the same as the original if the
        whitespace is not uniform. It will also remove blank lines. """
        default_option_line=self.options["option_line"]
        in_file=open(self.path,'r')
        # to keep the logic clean we will repeatedly cycle through self.lines
        # but in theory we could do it all on the line input stage
        self.lines=[]
        for line in in_file:
            self.lines.append(line)
        # now we need to collect and extract all the inline comments
        # There should be two types ones that have char position EOL, -1 or 0
        self.comments=collect_inline_comments(self.lines,begin_token="!",end_token="\n")
        # change all of them to be 0 or -1
        if self.comments is None:
            pass
        else:
            for index,comment in enumerate(self.comments):
                if comment[2]>1:
                    self.comments[index][2]=-1
                else:
                    self.comments[index][2]=0
        # Match the option line and set the attribute associated with them
        match=re.match(OPTION_LINE_PATTERN,default_option_line)
        self.option_line=default_option_line
        add_option_line=1
        for index,line in enumerate(self.lines):
            if re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE):
                #print line
                self.option_line=line.replace("\n","")
                self.options["option_line_line"]=index
                match=re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE)
                add_option_line=0
        # set the attributes associated with the option line
        for key,value in match.groupdict().items():
                    self.__dict__[key.lower()]=value
        # now the option line attributes are set deduce column properties from them
        if re.match('db',self.format,re.IGNORECASE):
            self.column_names=S2P_DB_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_DB_COLUMN_NAMES)
        elif re.match('ma',self.format,re.IGNORECASE):
            self.column_names=S2P_MA_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_MA_COLUMN_NAMES)
        elif re.match('ri',self.format,re.IGNORECASE):
            self.column_names=S2P_RI_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_RI_COLUMN_NAMES)
        # remove the comments
        stripped_lines=strip_inline_comments(self.lines,begin_token="!",end_token="\n")
        #print stripped_lines
        self.data=[]
        self.sparameter_complex=[]
        self.noiseparameter_data=[]
        self.options["sparameter_begin_line"]=self.options["sparameter_end_line"]=0
        self.options["noiseparameter_begin_line"]=self.options["noiseparameter_end_line"]=0
        data_lines=[]
        noise_lines=[]
        for index,line in enumerate(stripped_lines):
            if re.search(self.row_pattern,line):
                data_lines.append(index)
                #print re.search(self.row_pattern,line).groupdict()
                row_data=re.search(self.row_pattern,line).groupdict()
                self.add_sparameter_row(row_data=row_data)
                self.add_sparameter_complex_row(row_data=row_data)
            elif re.match(self.noiseparameter_row_pattern,line):
                noise_lines.append(index)
                row_data=re.match(self.noiseparameter_row_pattern,line).groupdict()
                self.add_noiseparameter_row(row_data=row_data)
        if data_lines != []:
            self.options["sparameter_begin_line"]=min(data_lines)+add_option_line
            self.options["sparameter_end_line"]=max(data_lines)+add_option_line
        if noise_lines != []:
            self.options["noiseparameter_begin_line"]=min(noise_lines)+add_option_line
            self.options["noiseparameter_end_line"]=max(noise_lines)+add_option_line
        #print self.data
        #print self.noiseparameter_data
        #print self.options["noiseparameter_begin_line"]

    def build_string(self,**temp_options):
        """Creates the output string"""
        #number of lines = option line + comments that start at zero + rows in sparameter data + rows in noise data
        # Is this different for snp? The only difference is noiseparameter_data.
        original_options=self.options
        for key,value in temp_options.items():
            self.options[key]=value
        if self.comments is None:
            number_line_comments=0
        else:
            number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
        #print number_line_comments
        number_lines=1+number_line_comments+len(self.data)+len(self.noiseparameter_data)
        #print("{0} is {1}".format('number_lines',number_lines))
        out_lines=["" for i in range(number_lines)]
        out_lines[self.options["option_line_line"]]=self.option_line
        #print("{0} is {1}".format('out_lines',out_lines))
        # populate the line comments
        comment_lines=[]
        inline_comments=[]
        if self.comments != None:
            for comment in self.comments:
                if comment[2] == 0:
                    out_lines[comment[1]]="!"+comment[0]
                    comment_lines.append(comment[1])
                else:
                    inline_comments.append(comment)
        #print("{0} is {1}".format('out_lines',out_lines))
        # now start writting data at first empty line after the option line
        for index,line in enumerate(out_lines):
            if index==self.options["option_line_line"]:
                pass
            elif index in comment_lines:
                pass
            elif self.data not in [[],None] and index>=self.options["sparameter_begin_line"] and index <=self.options["sparameter_end_line"]:
                # print out_lines
                #print index
                out_lines[index]=self.options["sparameter_row_formatter_string"].format(
                    delimiter=self.options["data_delimiter"],
                    *self.data[index-self.options["sparameter_begin_line"]])

            elif self.noiseparameter_data not in [[],None] and index>=self.options["noiseparameter_begin_line"] and index <=self.options["noiseparameter_end_line"]:
                #print out_lines
                #print (index-self.options["noiseparameter_begin_line"])
                out_lines[index]=self.options["nosieparameter_row_formatter_string"].format(
                    delimiter=self.options["data_delimiter"],*self.noiseparameter_data[index-self.options["noiseparameter_begin_line"]])
        #print("{0} is {1}".format('out_lines',out_lines))
        #print("{0} is {1}".format('inline_comments',inline_comments))
        if inline_comments:
            for comment in inline_comments:
                out_lines=insert_inline_comment(out_lines,comment=comment[0],
                                                line_number=comment[1],
                                                string_position=comment[2],
                                                begin_token=self.options["inline_comment_begin"],
                                                end_token="")
        #print("{0} is {1}".format('out_lines', out_lines))
        self.options=original_options
        return string_list_collapse(out_lines)


    def add_sparameter_row(self,row_data):
        """Adds data to the sparameter attribute, which is a list of s-parameters. The
        data can be a list of 9 real numbers
         or dictionary with appropriate column names, note column names are not case sensitive"""
        if isinstance(row_data, ListType):
            if len(row_data) == 9:
                    self.data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if isinstance(row_data, DictionaryType):
            new_row=[]
            for column_name in self.column_names:
                #print row_data
                new_row.append(float(row_data[column_name]))
            self.data.append(new_row)
        self.options["sparameter_end_line"]+=1
        self.options["noiseparameter_begin_line"]+=1
        self.options["noiseparameter_end_line"]+=1

    def add_sparameter_complex_row(self,row_data):
        """Adds a row to the sparameter_complex attribute. This attribute stores the values of the sparameter table in
        complex form for easy conversion and manipulation. Row_data is assumed to be of the same form that would be
        given to add_sparameter_row"""

        if isinstance(row_data, ListType) and len(row_data)==5 and isinstance(row_data[1], ComplexType):
            self.sparameter_complex.append(row_data)
        else:
            row_data=self.sparameter_row_to_complex(row_data=row_data)
            self.sparameter_complex.append(row_data)

    def sparameter_row_to_complex(self,row_data=None,row_index=None):
        """Given a row_data string, row_data list, or row_data dictionary it converts the values of the sparameter to
         complex notation (complex types) and returns a single list with 5 elements [Frequency,S11,S21,S12,S22]"""
        if row_index is not None:
            row_data=self.data[row_index]
        if row_data is None:
            print("Could not convert row to complex, need a valid row_data string, list or dictionary or a row_index in "
                  "data")
        out_row=[]
        try:
            if isinstance(row_data, StringType):
                row_data=re.search(self.row_pattern,row_data).groupdict()
            elif isinstance(row_data, ListType):
                row_data={self.column_names[index]:row_data[index] for index in range(9)}
            if not isinstance(row_data, DictionaryType):
                raise
            row_data={key:float(value) for key,value in row_data.items()}
            # now row data is in dictionary form with known keys, the tranformation is only based on self.format
            if re.match('db',self.format,re.IGNORECASE):
                S11=cmath.rect(10.**(row_data["dbS11"]/20.),(math.pi/180.)*row_data["argS11"])
                S21=cmath.rect(10.**(row_data["dbS21"]/20.),(math.pi/180.)*row_data["argS21"])
                S12=cmath.rect(10.**(row_data["dbS12"]/20.),(math.pi/180.)*row_data["argS12"])
                S22=cmath.rect(10.**(row_data["dbS22"]/20.),(math.pi/180.)*row_data["argS22"])
                out_row=[row_data["Frequency"],S11,S21,S12,S22]
            elif re.match('ma',self.format,re.IGNORECASE):
                S11=cmath.rect(row_data["magS11"],(math.pi/180.)*row_data["argS11"])
                S21=cmath.rect(row_data["magS21"],(math.pi/180.)*row_data["argS21"])
                S12=cmath.rect(row_data["magS12"],(math.pi/180.)*row_data["argS12"])
                S22=cmath.rect(row_data["magS22"],(math.pi/180.)*row_data["argS22"])
                out_row=[row_data["Frequency"],S11,S21,S12,S22]
            elif re.match('ri',self.format,re.IGNORECASE):
                S11=complex(row_data["reS11"],row_data["imS11"])
                S21=complex(row_data["reS21"],row_data["imS21"])
                S12=complex(row_data["reS12"],row_data["imS12"])
                S22=complex(row_data["reS22"],row_data["imS22"])
                out_row=[row_data["Frequency"],S11,S21,S12,S22]
            return out_row
        except:
            print("Could not convert row to a complex row")
            raise

    def add_noiseparameter_row(self,row_data):
        """Adds data to the noiseparameter_data attribute, which is a list of noise parameters. The
        data can be a list of 5 real numbers dictionary with appropriate column names,
        note column names are not case sensitive"""
        if isinstance(row_data, ListType):
            if len(row_data) == 5:
                    self.noiseparameter_data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if isinstance(row_data, DictionaryType):
            new_row=[]
            for column_name in self.noiseparameter_column_names:
                new_row.append(float(row_data[column_name]))
            self.noiseparameter_data.append(new_row)
        self.options["noiseparameter_end_line"]+=1


    def change_data_format(self,new_format=None):
        """Changes the data format to new_format. Format must be one of the following: 'DB','MA','RI'
        standing for Decibel-Angle, Magnitude-Angle or Real-Imaginary as per the touchstone specification
        all angles are in degrees."""
        old_format=self.format

        if re.match('db',new_format,re.IGNORECASE):
            self.format="DB"
            self.option_line=self.option_line.replace(old_format,"DB")
            self.column_names=S2P_DB_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_DB_COLUMN_NAMES)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                dbS11=20.*math.log(abs(self.sparameter_complex[row_index][1]),10.)
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                dbS21=20.*math.log(abs(self.sparameter_complex[row_index][2]),10.)
                argS21=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][2])
                dbS12=20.*math.log(abs(self.sparameter_complex[row_index][3]),10.)
                argS12=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][3])
                dbS22=20.*math.log(abs(self.sparameter_complex[row_index][4]),10.)
                argS22=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][4])
                self.data[row_index]=[frequency,dbS11,argS11,dbS21,argS21,dbS12,argS12,dbS22,argS22]

        elif re.match('ma',new_format,re.IGNORECASE):
            self.format="MA"
            self.option_line=self.option_line.replace(old_format,"MA")
            self.column_names=S2P_MA_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_MA_COLUMN_NAMES)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                magS11=abs(self.sparameter_complex[row_index][1])
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                magS21=abs(self.sparameter_complex[row_index][2])
                argS21=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][2])
                magS12=abs(self.sparameter_complex[row_index][3])
                argS12=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][3])
                magS22=abs(self.sparameter_complex[row_index][4])
                argS22=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][4])
                self.data[row_index]=[frequency,magS11,argS11,magS21,argS21,magS12,argS12,magS22,argS22]

        elif re.match('ri',new_format,re.IGNORECASE):
            self.format="RI"
            self.option_line=self.option_line.replace(old_format,"RI")
            self.column_names=S2P_RI_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S2P_RI_COLUMN_NAMES)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                reS11=self.sparameter_complex[row_index][1].real
                imS11=self.sparameter_complex[row_index][1].imag
                reS21=self.sparameter_complex[row_index][2].real
                imS21=self.sparameter_complex[row_index][2].imag
                reS12=self.sparameter_complex[row_index][3].real
                imS12=self.sparameter_complex[row_index][3].imag
                reS22=self.sparameter_complex[row_index][4].real
                imS22=self.sparameter_complex[row_index][4].imag
                self.data[row_index]=[frequency,reS11,imS11,reS21,imS21,reS12,imS12,reS22,imS22]
        else:
            print("Could not change data format the specified format was not DB, MA, or RI")
            return


    def correct_switch_terms(self,switch_terms=None,switch_terms_format='port'):
        """Corrects sparameter data for switch terms. Switch terms must be a list with a row of format
        [Frequency,SWF,SWR] where SWF is the complex foward switch term (SWport2),
        SWR is the complex reverse switch term (SWport1)"""
        if re.search('port',switch_terms_format,re.IGNORECASE):
            foward_index=2
            reverse_index=1
        elif re.search('F',switch_terms_format,re.IGNORECASE):
            foward_index=1
            reverse_index=2

        self.corrected_data=[]
        for index,row in enumerate(self.sparameter_complex[:]):
            SWF=switch_terms[index][foward_index]
            SWR=switch_terms[index][reverse_index]
            [S11,S21,S12,S22]=row[1:]
            D=1-S21*S12*SWR*SWF
            S11_corrected=(S11-S12*S21*SWF)/D
            S21_corrected=(S21-S22*S21*SWF)/D
            S12_corrected=(S12-S11*S12*SWR)/D
            S22_corrected=(S22-S12*S21*SWR)/D
            self.corrected_data.append([row[0],S11_corrected,S21_corrected,S12_corrected,S22_corrected])




class SNP(SNPBase):
    """SNP is a class that holds touchstone files of more than 2 ports. Use S1PV1 and S2PV2
    for one and two ports, they have special methods"""
    def __init__(self,file_path=None,**options):
        """Initialization of the snp class for version 1 files,
        if a file path is specified, it opens and parses the file. If the file path is not
        specified then data can be added through the snp.data. A reference to the version 1 touchstone
        format may be found at
        http://cp.literature.agilent.com/litweb/pdf/genesys200801/sim/linear_sim/sparams/touchstone_file_format.htm
        For S2P files use the S2PV1 class. This class does not handle noise parameters.
        """
        defaults={"number_ports":None,
                  "data_delimiter":"  ",
                  "column_names_delimiter":None,
                  "specific_descriptor":'Multiport',
                  "general_descriptor":'Sparameter',
                  "option_line_line":0,
                  "option_line":'# GHz S RI R 50',
                  "directory":None,
                  "extension":None,
                  "metadata":None,
                  "column_descriptions":None,
                  "sparameter_row_formatter_string":None,
                  "data":[],
                  "sparameter_complex":[],
                  "noiseparameter_data":[],
                  "comments":[],
                  "path":None,
                  "column_units":None,
                  "inline_comment_begin":"!",
                  "inline_comment_end":"",
                  "sparameter_begin_line":1,
                  "sparameter_end_line":None,
                  }
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        # adds common functions from base class
        SNPBase.__init__(self)
        # determine the number of ports
        if self.options["number_ports"] is None:
            if self.options["path"] is None and file_path is None:
                # if number of ports cannot be figured out exit with error
                raise TypeError("Cannot determine number of ports, please pass as number_ports=int")
            else:
                # determine number of ports

                if self.options["path"] is not None:
                    self.number_ports=number_ports_from_file_name(self.options["path"])
                elif file_path is not None:
                    self.number_ports=number_ports_from_file_name(file_path)
        else:
            self.number_ports = self.options["number_ports"]

        #self.number_ports = self.options["number_ports"]
        self.elements=['data','noiseparameter_data','comments','option_line']
        self.noiseparameter_data=[]
        self.metadata=self.options["metadata"]
        # Determine the number of lines per sparameter
        if self.number_ports in [1,2]:
            self.number_lines_per_sparameter=1
            self.wrap_value=8
        elif self.number_ports in [3]:
            self.number_lines_per_sparameter=3
            self.wrap_value=6
        else:
            self.number_lines_per_sparameter=int(self.number_ports**2/4)
            self.wrap_value=8
        if file_path is not None:
            self.path=file_path
            self.__read_and_fix__()
        else:
            # promote options to attributes
            for element in self.elements:
                self.__dict__[element]=self.options[element]
            self.sparameter_complex=self.options["sparameter_complex"]
            match=re.match(OPTION_LINE_PATTERN,self.option_line)
            # set the values associated with the option line
            for key,value in match.groupdict().items():
                self.__dict__[key.lower()]=value
            if re.match('db',self.format,re.IGNORECASE):
                self.column_names=build_snp_column_names(self.number_ports,"db")
            elif re.match('ma',self.format,re.IGNORECASE):
                self.column_names=build_snp_column_names(self.number_ports,"ma")
            elif re.match('ri',self.format,re.IGNORECASE):
                self.column_names=build_snp_column_names(self.number_ports,"db")

            # now we handle the cases if data or sparameter_complex is specified
            if self.data is [] and self.sparameter_complex is[]:
                pass
            elif self.sparameter_complex in [[],None]:
                for row in self.data:
                    self.add_sparameter_complex_row(row)
                    #print("{0} is {1}".format("row",row))
            elif self.data in [[],None]:
                self.data=[[0 for i in self.column_names] for row in self.sparameter_complex]
                #print self.data
                self.change_data_format(new_format=self.format)
            if self.comments is None:
                number_line_comments=0
            else:
                number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
            self.options["sparameter_begin_line"]=number_line_comments+1
            self.options["sparameter_end_line"]= self.options["sparameter_begin_line"]\
                                                 +len(self.data)+1

            if self.options["path"] is None:
                self.path=auto_name(self.options["specific_descriptor"],self.options["general_descriptor"],
                                    self.options['directory'],self.options["extension"])
            else:
                self.path=self.options["path"]
        # Need to be careful here, sparameters can have many lines
        self.sparameter_lines=[]
        for row in self.data[:]:
            for line_number in range(self.number_lines_per_sparameter):
                if line_number is 0:
                    row_formatter=build_row_formatter(precision=9,number_columns=self.wrap_value+1)
                    self.sparameter_lines.append(row_formatter.format(delimiter=self.options["data_delimiter"],
                                                                      *row[:self.wrap_value+1]))
                elif line_number>0 and line_number<self.number_lines_per_sparameter:
                    row_formatter=build_row_formatter(precision=9,number_columns=self.wrap_value)
                    offset=1+self.wrap_value*(line_number)
                    span=self.wrap_value
                    self.sparameter_lines.append(row_formatter.format(delimiter=self.options["data_delimiter"],
                                                                      *row[offset:offset+span]))
                elif line_number<self.number_lines_per_sparameter-1:
                    offset=1+self.wrap_value*(line_number)
                    span=len(row)-offset
                    row_formatter=build_row_formatter(precision=9,number_columns=span)
                    self.sparameter_lines.append(row_formatter.format(delimiter=self.options["data_delimiter"],
                                                                      *row[offset:offset+span]))
        #print("{0} is {1}".format("len(self.sparameter_lines)",len(self.sparameter_lines)))
        self.options["column_types"]=["float" for column in self.column_names[:]]
    def __read_and_fix__(self):
        """Reads a snp v1 file and fixes any problems with delimiters. Since snp files may use
        any white space or combination of white space as data delimiters it reads the data and creates
        a uniform delimter. This means a file saved with save() will not be the same as the original if the
        whitespace is not uniform. This function removes empty lines """
        self.noiseparameter_data=self.options["noiseparameter_data"]
        default_option_line=self.options["option_line"]


        in_file=open(self.path,'r')
        # to keep the logic clean we will repeatedly cycle through self.lines
        # but in theory we could do it all on the line input stage
        self.lines=[]
        self.data_lines=[]
        removed_lines=[]
        for index,line in enumerate(in_file):
            self.lines.append(line)
            # if the line is just '\n' ignore it
            if line in ["","\n"]:
                removed_lines.append(index)
                continue
            #if the line is an option line collect it
            elif re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE):
                continue
            elif re.match(COMMENT_PATTERN,line,re.IGNORECASE):
                continue
            else:
                self.data_lines.append(line)
        # now we need to collect and extract all the inline comments
        # There should be two types ones that have char position EOL, -1 or 0
        self.comments=collect_inline_comments(self.lines,begin_token="!",end_token="\n")
        # make sure there are no comments in the data
        self.data_lines=strip_inline_comments(self.data_lines,begin_token="!",end_token="\n")
        # change all of them to be 0 or -1
        if self.comments is None:
            pass
        else:
            for index,comment in enumerate(self.comments):
                skipped=removed_lines
                shift=list(map(lambda x: x<comment[1],skipped)).count(True)
                self.comments[index][1]=self.comments[index][1]-shift
                if comment[2]>1:
                    self.comments[index][2]=-1
                else:
                    self.comments[index][2]=0
        # Match the option line and set the attribute associated with them
        match=re.match(OPTION_LINE_PATTERN,default_option_line)
        self.option_line=default_option_line
        add_option_line=1
        for index,line in enumerate(self.lines):
            if re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE):
                #print line
                self.option_line=line.replace("\n","")
                self.options["option_line_line"]=index
                match=re.search(OPTION_LINE_PATTERN,line,re.IGNORECASE)
                add_option_line=0
        # set the attributes associated with the option line
        for key,value in match.groupdict().items():
                    self.__dict__[key.lower()]=value
        # now the option line attributes are set deduce column properties from them
        self.column_names=build_snp_column_names(self.number_ports,self.format)
        #print stripped_lines
        segments=[self.data_lines[i::self.number_lines_per_sparameter] for i in range(self.number_lines_per_sparameter)]
        combined_list=combine_segments(segments)
        self.data=parse_combined_float_list(combined_list)
        self.sparameter_complex=[]
        for row in self.data[:]:
            self.add_sparameter_complex_row(row)
        self.options["sparameter_begin_line"]=self.options["sparameter_end_line"]=0

    def build_string(self,**temp_options):
        """Creates the output string"""
        #number of lines = option line + comments that start at
        # zero + rows in sparameter data*number_lines_per_sparameter + rows in noise data
        # Is this different for snp? The only difference is noiseparameter_data.
        original_options=self.options
        for key,value in temp_options.items():
            self.options[key]=value
        if self.comments is None:
            number_line_comments=0
        else:
            number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
        #print number_line_comments
        number_lines=1+number_line_comments+len(self.sparameter_lines)
        #print("{0} is {1}".format('number_lines',number_lines))
        out_lines=["" for i in range(number_lines)]
        sparameter_lines=["" for i in range(len(self.data)*self.number_lines_per_sparameter)]
        out_lines[self.options["option_line_line"]]=self.option_line
        #print("{0} is {1}".format('out_lines',out_lines))
        # populate the line comments
        comment_lines=[]
        inline_comments=[]
        if self.comments != None:
            for comment in self.comments:
                if comment[2] == 0:
                    out_lines[comment[1]]="!"+comment[0]
                    comment_lines.append(comment[1])
                else:
                    inline_comments.append(comment)
        #print("{0} is {1}".format('out_lines',out_lines))
        # now start writting data at first empty line after the option line
        #print("{0} is {1}".format('len(self.sparameter_lines)',len(self.sparameter_lines)))
        out_line_number=0
        for index,line in enumerate(self.sparameter_lines[:]):
                value_written=False
                while(not value_written):
                    if out_line_number==self.options["option_line_line"]:
                        out_line_number+=1
                        continue
                    elif out_line_number in comment_lines:
                        out_line_number+=1
                        continue
                    else:
                        #print out_lines
                        #print index
                        out_lines[out_line_number]=line
                        out_line_number+=1
                        #print("{0} is {1}".format('out_line_number',out_line_number))
                        value_written=True

        #print("{0} is {1}".format('out_lines',out_lines))
        #print("{0} is {1}".format('inline_comments',inline_comments))
        if inline_comments:
            for comment in inline_comments:
                out_lines=insert_inline_comment(out_lines,comment=comment[0],
                                                line_number=comment[1],
                                                string_position=comment[2],
                                                begin_token=self.options["inline_comment_begin"],
                                                end_token="")
        #print("{0} is {1}".format('out_lines', out_lines))
        self.options=original_options
        return string_list_collapse(out_lines)

    def add_sparameter_row(self,row_data):
        """Adds data to the sparameter attribute, which is a list of s-parameters. The
        data can be a list of nports**2 +1 numbers
         or dictionary with appropriate column names, note column names are not case sensitive
         it is assumed that the row_data is in the format that the model is currently in. Check
         SNP.format if in doubt"""
        if isinstance(row_data, ListType):
            if len(row_data) == self.number_ports**2+1:
                    self.data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if isinstance(row_data, DictionaryType):
            new_row=[]
            for column_name in self.column_names:
                #print row_data
                new_row.append(float(row_data[column_name]))
            self.data.append(new_row)
        self.options["sparameter_end_line"]+=1

    def add_sparameter_complex_row(self,row_data):
        """Adds a row to the sparameter_complex attribute. This attribute stores the values of the sparameter table in
        complex form for easy conversion and manipulation. Row_data is assumed to be of the same form that would be
        given to add_sparameter_row"""

        if isinstance(row_data, ListType) and len(row_data)==(self.number_ports**2+1) and isinstance(row_data[1], ComplexType):
            self.sparameter_complex.append(row_data)
        else:
            row_data=self.sparameter_row_to_complex(row_data=row_data)
            self.sparameter_complex.append(row_data)
    def sparameter_row_to_complex(self,row_data=None,row_index=None):
        """Given a row_data string, row_data list, or row_data dictionary it converts the values of the sparameter to
         complex notation (complex types) and returns a single list with number_ports**2 +1 elements [Frequency,S11,..,SNN]"""
        if row_index is not None:
            row_data=self.data[row_index]
        if row_data is None:
            print("Could not convert row to complex, need a valid row_data string, list or dictionary or a row_index in "
                  "data")
        out_row=[]
        try:
            if isinstance(row_data, StringType):
                row_data=parse_combined_float_list([row_data])[0]
                row_data={self.column_names[index]:row_data[index] for index in range(len(self.column_names))}
            elif isinstance(row_data, ListType):
                row_data={self.column_names[index]:row_data[index] for index in range(len(self.column_names))}
            if not isinstance(row_data, DictionaryType):
                raise
            row_data={key:float(value) for key,value in row_data.items()}
            # now row data is in dictionary form with known keys, the tranformation is only based on self.format
            if self.number_ports==2:
                if re.match('db',self.format,re.IGNORECASE):
                    S11=cmath.rect(10.**(row_data["dbS11"]/20.),(math.pi/180.)*row_data["argS11"])
                    S21=cmath.rect(10.**(row_data["dbS21"]/20.),(math.pi/180.)*row_data["argS21"])
                    S12=cmath.rect(10.**(row_data["dbS12"]/20.),(math.pi/180.)*row_data["argS12"])
                    S22=cmath.rect(10.**(row_data["dbS22"]/20.),(math.pi/180.)*row_data["argS22"])
                    out_row=[row_data["Frequency"],S11,S21,S12,S22]
                elif re.match('ma',self.format,re.IGNORECASE):
                    S11=cmath.rect(row_data["magS11"],(math.pi/180.)*row_data["argS11"])
                    S21=cmath.rect(row_data["magS21"],(math.pi/180.)*row_data["argS21"])
                    S12=cmath.rect(row_data["magS12"],(math.pi/180.)*row_data["argS12"])
                    S22=cmath.rect(row_data["magS22"],(math.pi/180.)*row_data["argS22"])
                    out_row=[row_data["Frequency"],S11,S21,S12,S22]
                elif re.match('ri',self.format,re.IGNORECASE):
                    S11=complex(row_data["reS11"],row_data["imS11"])
                    S21=complex(row_data["reS21"],row_data["imS21"])
                    S12=complex(row_data["reS12"],row_data["imS12"])
                    S22=complex(row_data["reS22"],row_data["imS22"])
                    out_row=[row_data["Frequency"],S11,S21,S12,S22]
                return out_row
            elif self.number_ports!=2:
                if re.match('ri',self.format,re.IGNORECASE):
                    re_values=self.column_names[1::2]
                    im_values=self.column_names[2::2]
                    complex_values=[]
                    for index,value in enumerate(re_values):
                        complex_s=complex(row_data[value],row_data[im_values[index]])
                        complex_values.append(complex_s)
                    out_row=[row_data["Frequency"]]+complex_values
                elif re.match('ma',self.format,re.IGNORECASE):
                    mag_values=self.column_names[1::2]
                    arg_values=self.column_names[2::2]
                    complex_values=[]
                    for index,value in enumerate(mag_values):
                        complex_s=cmath.rect(row_data[value],(math.pi/180.)*row_data[arg_values[index]])
                        complex_values.append(complex_s)
                    out_row=[row_data["Frequency"]]+complex_values
                elif re.match('db',self.format,re.IGNORECASE):
                    db_values=self.column_names[1::2]
                    arg_values=self.column_names[2::2]
                    complex_values=[]
                    for index,value in enumerate(db_values):
                        complex_s=cmath.rect(10.**(row_data[value]/20.),(math.pi/180.)*row_data[arg_values[index]])
                        complex_values.append(complex_s)
                    out_row=[row_data["Frequency"]]+complex_values
                return out_row
        except:
            print("Could not convert row to a complex row")
            raise
    def change_data_format(self,new_format=None):
        """Changes the data format to new_format. Format must be one of the following: 'DB','MA','RI'
        standing for Decibel-Angle, Magnitude-Angle or Real-Imaginary as per the touchstone specification
        all angles are in degrees."""
        old_format=self.format

        if re.match('db',new_format,re.IGNORECASE):
            self.format="DB"
            self.option_line=self.option_line.replace(old_format,"DB")
            self.column_names=build_snp_column_names(self.number_ports,new_format)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                complex_values=self.sparameter_complex[row_index][1:]
                values=[]
                for index,value in enumerate(complex_values):
                    if value == complex(0,0):
                        db=MINIMUM_DB_VALUE
                        arg=MINIMUM_DB_ARG_VALUE
                    else:
                        db=20.*math.log(abs(value),10.)
                        arg=(180./math.pi)*cmath.phase(value)
                    values.append(db)
                    values.append(arg)
                new_row=[frequency]+values
                self.data[row_index]=new_row

        elif re.match('ma',new_format,re.IGNORECASE):
            self.format="MA"
            self.option_line=self.option_line.replace(old_format,"MA")
            self.column_names=build_snp_column_names(self.number_ports,new_format)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                complex_values=self.sparameter_complex[row_index][1:]
                values=[]
                for index,value in enumerate(complex_values):
                    mag=abs(value)
                    arg=(180./math.pi)*cmath.phase(value)
                    values.append(mag)
                    values.append(arg)
                new_row=[frequency]+values
                self.data[row_index]=new_row

        elif re.match('ri',new_format,re.IGNORECASE):
            self.format="RI"
            self.option_line=self.option_line.replace(old_format,"RI")
            self.column_names=build_snp_column_names(self.number_ports,new_format)
            for row_index,row in enumerate(self.sparameter_complex):
                frequency=self.sparameter_complex[row_index][0]
                complex_values=self.sparameter_complex[row_index][1:]
                values=[]
                for index,value in enumerate(complex_values):
                    re_part=value.real
                    im_part=value.imag
                    values.append(re_part)
                    values.append(im_part)
                new_row=[frequency]+values
                self.data[row_index]=new_row
        else:
            print("Could not change data format the specified format was not DB, MA, or RI")
            return
    def show(self,**options):
        """Shows the touchstone file"""
        defaults={"display_legend":True,
                  "save_plot":False,
                  "directory":None,
                  "specific_descriptor":self.options["specific_descriptor"],
                  "general_descriptor":self.options["general_descriptor"]+"Plot",
                  "file_name":None,
                  "type":"matplotlib"}
        plot_options={}
        for key,value in defaults.items():
            plot_options[key]=value
        for key,value in options.items():
            plot_options[key]=value
        # plot data

        if re.search("matplot",plot_options["type"],re.IGNORECASE):
            current_format=self.format
            self.change_data_format('MA')
            number_rows=self.number_ports
            fig, axes = plt.subplots(nrows=number_rows, ncols=2)
            mag_axes=axes.flat[0::2]
            arg_axes=axes.flat[1::2]
            mag_names=self.column_names[1::2]
            arg_names=self.column_names[2::2]
            frequency_data=self.get_column('Frequency')

            for index,ax in enumerate(mag_axes):
                ax_names=mag_names[index::number_rows]
                for row_index in range(number_rows):
                    column_color=(1-float(row_index)/number_rows,0,float(row_index)/number_rows,.5)
                    ax.plot(frequency_data,
                            self.get_column(ax_names[row_index]),
                            label=ax_names[row_index],color=column_color)
                    if plot_options["display_legend"]:
                        ax.legend(loc=1,fontsize='8')
            for index,ax in enumerate(arg_axes):
                ax_names=arg_names[index::number_rows]

                for row_index in range(number_rows):
                    column_color=(1-float(row_index)/number_rows,0,float(row_index)/number_rows,.5)
                    ax.plot(frequency_data,
                            self.get_column(ax_names[row_index]),
                            label=ax_names[row_index],color=column_color)
                    if plot_options["display_legend"]:
                        ax.legend(loc=1,fontsize='8')


            plt.tight_layout()
            self.change_data_format(current_format)
            plt.show()
            return fig

#-----------------------------------------------------------------------------
# Module Scripts
def test_option_string():
    """Tests the regex for extracting option string values"""
    match=re.search(OPTION_LINE_PATTERN,"# GHz S RI R 50")
    print(match.groupdict())
    print(match.groupdict()["Format"] in FORMATS)

def test_S1PV1(file_path="OnePortTouchstoneTestFile.s1p"):
    """Tests the s1pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S1PV1(file_path)
    print(new_table)
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='DB')
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='MA')
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='RI')
    print_s1p_attributes(new_table=new_table)
    print(new_table)
    new_table.show()

def test_s2pv1(file_path="thru.s2p"):
    """Tests the s2pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S2PV1(file_path)
    print(new_table)
    print("The Table as read in with line numbers is")
    for index,line in enumerate(new_table.lines):
        print(("{0} {1}".format(index,line)))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('data',str(new_table.data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('noiseparameter_data',str(new_table.noiseparameter_data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('comments',str(new_table.comments))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('option_line',str(new_table.option_line))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('format',str(new_table.format))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('column_names',str(new_table.column_names))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('noiseparameter_column_names',str(new_table.noiseparameter_column_names))))
def test_SNP(file_path="thru.s2p"):
    """Tests the SNP class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=SNP(file_path)
    #print new_table
    print("The Table as read in with line numbers is")
    for index,line in enumerate(new_table.lines):
        print(("{0} {1}".format(index,line)))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('data',str(new_table.data))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('comments',str(new_table.comments))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('option_line',str(new_table.option_line))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('format',str(new_table.format))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('column_names',str(new_table.column_names))))
    print(("-"*80))
    print(("The attribute {0} is {1}".format('sparameter_lines',str(new_table.sparameter_lines))))
    print(("-"*80))
    print(str(new_table))

def test_change_format(file_path="thru.s2p"):
    """Tests the s2pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S2PV1(file_path)
    print_s2p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='DB')
    print_s2p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='MA')
    print_s2p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='RI')
    print_s2p_attributes(new_table=new_table)
    print(new_table)
    new_table.show()
def test_change_format_SNP(file_path="thru.s2p"):
    """Tests the s2pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=SNP(file_path)
    print_snp_attributes(new_table=new_table)
    new_table.change_data_format(new_format='DB')
    print_snp_attributes(new_table=new_table)
    new_table.change_data_format(new_format='MA')
    print_snp_attributes(new_table=new_table)
    new_table.change_data_format(new_format='RI')
    print_snp_attributes(new_table=new_table)

def test_change_frequency_units(file_path="thru.s2p"):
    """Tests the models change_frequency_units method"""
    os.chdir(TESTS_DIRECTORY)
    new_table=SNP(file_path)
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    new_table.change_frequency_units("Hz")
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    new_table.change_frequency_units("MHz")
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    new_table.change_frequency_units("kHz")
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    new_table.change_frequency_units("THz")
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    new_table.change_frequency_units("Hz")
    print(("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency"))))
    print(new_table)
    new_table.show()
def test_build_snp_column_names():
    """Tests the function build_snp_column_names"""
    for n_port in range(1,10):
        for format in ["RI","DB","MA"]:
            print(("The column names for a {0}-port device in {1} format are ".format(n_port,format)))
            print(("{0}".format(build_snp_column_names(number_of_ports=n_port,format=format))))
def test_s2p_mean(s2p_list=["thru.s2p","thru.s2p"]):
    """Tests the s2p_mean function by applying it the files in TESTS_DIRECTORY"""
    os.chdir(TESTS_DIRECTORY)
    s2p_models=[]
    for file_name in s2p_list:
        s2p_models.append(S2PV1(file_name))
    mean=s2p_mean(s2p_models)
    mean.show()
def test_s2p_difference(s2p_one="thru.s2p",s2p_two="thru.s2p"):
    """Tests the s2p_difference function by applying it the files in TESTS_DIRECTORY"""
    os.chdir(TESTS_DIRECTORY)
    difference=s2p_difference(s2p_one=S2PV1(s2p_one),s2p_two=S2PV1(s2p_two))
    difference.show()
def test_s2p_mean_and_difference(s2p_one="thru.s2p",s2p_two="thru.s2p"):
    "Tests taking a difference and then a mean"
    os.chdir(TESTS_DIRECTORY)
    s2p=S2PV1(s2p_one)
    s2p.show()
    difference=s2p_difference(s2p_one=s2p,s2p_two=S2PV1(s2p_two))
    difference.show()
    mean=s2p_mean([s2p,difference])
    mean.show()

def test_add_comment(file_path="thru.s2p"):
    """Tests the add_comment method of the SNPBase superclass"""
    os.chdir(TESTS_DIRECTORY)
    s2p=SNP(file_path)
    print("Before adding a comment")
    print(("-"*80))
    print(s2p)
    print("After adding a comment")
    print(("-"*80))
    s2p.add_comment("A new comment")
    print(s2p)

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_S1PV1()
    test_option_string()
    test_s2pv1()
    test_s2pv1('TwoPortTouchstoneTestFile.s2p')
    test_change_format()
    test_change_format('TwoPortTouchstoneTestFile.s2p')
    test_change_format('20160301_30ft_cable_0.s2p')
    test_change_format_SNP('setup20101028.s4p')
    test_change_frequency_units('setup20101028.s4p')
    test_change_frequency_units("B7_baseline_50ohm_OR2_10n0_4p0_REV2_EVB1_01new.s3p")
    test_s2pv1('704b.S2P')
    test_change_format('704b.S2P')
    test_build_snp_column_names()
    test_SNP()
    test_SNP("B7_baseline_50ohm_OR2_10n0_4p0_REV2_EVB1_01new.s3p")
    test_SNP('setup20101028.s4p')
    test_s2p_mean()
    test_s2p_difference()
    test_s2p_mean(["thru.s2p","thru.s2p","thru.s2p"])
    test_s2p_mean_and_difference()
    test_SNP('Solution_0.s4p')
    test_change_format_SNP('Solution_0.s4p')
    test_add_comment()
