#-----------------------------------------------------------------------------
# Name:        TouchstoneModels
# Purpose:     To store and manipulate touchstone files
# Author:      Aric Sanders
# Created:     3/7/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A module dedicated to the manipulation and storage of touchstone files, such as
 .s2p or .ts files. Touchstone files are normally s-parameter data for multiport VNA's"""

#-----------------------------------------------------------------------------
# Standard Imports
import os
import cmath
import math
#-----------------------------------------------------------------------------
# Third Party Imports
try:
    from pyMeasure.Code.Utils.Alias import *
    METHOD_ALIASES=1
except:
    print("The module pyMeasure.Code.Utils.Alias was not found")
    METHOD_ALIASES=0
    pass
try:
    from pyMeasure.Code.DataHandlers.GeneralModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.GeneralModels was not found,"
          "please put it on the python path")
    raise ImportError
try:
    import numpy as np
except:
    print("The module numpy was not found,"
          "please put it on the python path")
    raise ImportError
import matplotlib.pyplot as plt
try:
    import smithplot
    SMITHPLOT=1

except:
    print("The module smithplot was not found,"
          "please put it on the python path")
    SMITHPLOT=0
#-----------------------------------------------------------------------------
# Module Constants
TOUCHSTONE_KEYWORDS=["Version","Number of Ports","Two-Port Order","Number of Frequencies",
                     "Number of Noise Frequencies","Reference","Matrix Format","Mixed-Mode Order",
                     "Network Data","Noise Data","End"]
OPTION_LINE_PATTERN="#[\s]+(?P<Frequency_Units>\w+)[\s]+(?P<Parameter>\w+)[\s]+(?P<Format>\w+)[\s]+R[\s]+(?P<Reference_Resistance>[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"
COMMENT_PATTERN="!(?P<Comment>.+)\n"
FREQUENCY_UNITS=["Hz","kHz","MHz","GHz"]
PARAMETERS=["S","Y","Z","G","H"]
FORMATS=["RI","DB","MA"]
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

#-----------------------------------------------------------------------------
# Module Functions
def print_s1p_attributes(new_table):
    """prints some important attributes of s1p table"""
    print("The attributes for the table as read in are")
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_data',str(new_table.sparameter_data)))
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex)))
    print("-"*80)
    print("The attribute {0} is {1}".format('comments',str(new_table.comments)))
    print("-"*80)
    print("The attribute {0} is {1}".format('option_line',str(new_table.option_line)))
    print("-"*80)
    print("The attribute {0} is {1}".format('format',str(new_table.format)))
    print("-"*80)
    print("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units)))
    print("-"*80)
    print("The attribute {0} is {1}".format('column_names',str(new_table.column_names)))
    print("-"*80)

def print_s2p_attributes(new_table):
    """prints some important attributes of s2p table"""
    print("The attributes for the table as read in are")
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_data',str(new_table.sparameter_data)))
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex)))
    print("-"*80)
    print("The attribute {0} is {1}".format('noiseparameter_data',str(new_table.noiseparameter_data)))
    print("-"*80)
    print("The attribute {0} is {1}".format('comments',str(new_table.comments)))
    print("-"*80)
    print("The attribute {0} is {1}".format('option_line',str(new_table.option_line)))
    print("-"*80)
    print("The attribute {0} is {1}".format('format',str(new_table.format)))
    print("-"*80)
    print("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units)))
    print("-"*80)
    print("The attribute {0} is {1}".format('column_names',str(new_table.column_names)))
    print("-"*80)
    print("The attribute {0} is {1}".format('noiseparameter_column_names',str(new_table.noiseparameter_column_names)))

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
#-----------------------------------------------------------------------------
# Module Classes
class S1PV1():
    """A container for touchstone S1P. S1P are one port s-parameter files, with comments on any line
    began with ! and an option line in the format # GHz S RI R 50.0 that specifies the frequency units,
    stored parameter (default is S), data format (RI,MA or DB) and reference resistance data is 3 columns"""
    def __init__(self,file_path=None,**options):
        """Initialization of the s2p class for version 1 files,
        if a file path is specified, it opens and parses the file. If the file path is not
        specified then data can be added through the s2pv1.sparameter_data. A reference to the version 1 touchstone
        format may be found at
        http://cp.literature.agilent.com/litweb/pdf/genesys200801/sim/linear_sim/sparams/touchstone_file_format.htm
        """
        defaults={"data_delimiter":"\t",
                  "column_names_delimiter":None,
                  "specific_descriptor":'One_Port',
                  "general_descriptor":'Sparameter',
                  "option_line_line":0,
                  "option_line":'# GHz S RI R 50',
                  "directory":None,
                  "extension":'s1p',
                  "metadata":None,
                  "column_descriptions":None,
                  "sparameter_row_formatter_string":build_row_formatter(None,3),
                  "sparameter_data":[],
                  "sparameter_complex":[],
                  "comments":[],
                  "path":None,
                  "column_units":None,
                  "sparameter_begin_line":1,
                  "sparameter_end_line":None

                  }
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        self.elements=['sparameter_data','comments','option_line']
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
            for key,value in match.groupdict().iteritems():
                self.__dict__[key.lower()]=value
            # now we handle the cases if sparameter_data or sparameter_complex is specified
            if self.sparameter_data is [] and self.sparameter_complex is[]:
                pass
            elif self.sparameter_complex is []:
                for row in self.sparameter_data:
                    self.add_sparameter_complex_row(row)
                    #print("{0} is {1}".format("row",row))
            elif self.sparameter_data is []:
                self.sparameter_data=[[0,0,0,0,0,0,0,0,0] for row in self.sparameter_complex]
                #print self.sparameter_data
                self.change_data_format(new_format=self.format)

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


        for key,value in match.groupdict().iteritems():
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
        self.sparameter_data=[]
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
        #print self.sparameter_data

    def build_string(self,**temp_options):
        """Creates the output string"""
        #number of lines = option line + comments that start at zero + rows in sparameter data + rows in noise data
        original_options=self.options
        for key,value in temp_options.iteritems():
            self.options[key]=value
        if self.comments is None:
            number_line_comments=0
        else:
            number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
        #print number_line_comments
        number_lines=1+number_line_comments+len(self.sparameter_data)
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
            elif self.sparameter_data not in [[],None] and index>=self.options["sparameter_begin_line"] and index <=self.options["sparameter_end_line"]:
                # print out_lines
                #print index
                out_lines[index]=self.options["sparameter_row_formatter_string"].format(
                    delimiter=self.options["data_delimiter"],
                    *self.sparameter_data[index-self.options["sparameter_begin_line"]])
        if inline_comments:
            for comment in inline_comments:
                out_lines=insert_inline_comment(out_lines,comment=comment[0],
                                                line_number=comment[1],
                                                string_position=comment[2],
                                                begin_token=self.options["inline_comment_begin"],
                                                end_token="")
        self.options=original_options
        return string_list_collapse(out_lines)

    def __str__(self):
        self.string=self.build_string()
        return self.string

    def save(self,file_path=None,**temp_options):
        """Saves the s2p file to file_path with options, defaults to s2p.path"""
        if file_path is None:
            file_path=self.path
        out_file=open(file_path,'w')
        out_file.write(self.build_string(**temp_options))
        out_file.close()

    def add_sparameter_row(self,row_data):
        """Adds data to the sparameter attribute, which is a list of s-parameters. The
        data can be a list of 9 real numbers
         or dictionary with appropriate column names, note column names are not case sensitive"""
        if type(row_data) is ListType:
            if len(row_data) == 3:
                    self.sparameter_data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if type(row_data) is DictionaryType:
            new_row=[]
            for column_name in self.column_names:
                #print row_data
                new_row.append(float(row_data[column_name]))
            self.sparameter_data.append(new_row)
        self.options["sparameter_end_line"]+=1

    def add_sparameter_complex_row(self,row_data):
        """Adds a row to the sparameter_complex attribute. This attribute stores the values of the sparameter table in
        complex form for easy conversion and manipulation. Row_data is assumed to be of the same form that would be
        given to add_sparameter_row"""

        if type(row_data) is ListType and len(row_data)==3 and type(row_data[1]) is ComplexType:
            self.sparameter_complex.append(row_data)
        else:
            row_data=self.sparameter_row_to_complex(row_data=row_data)
            self.sparameter_complex.append(row_data)

    def sparameter_row_to_complex(self,row_data=None,row_index=None):
        """Given a row_data string, row_data list, or row_data dictionary it converts the values of the sparameter to
         complex notation (complex types) and returns a single list with 5 elements [Frequency,S11,S21,S12,S22]"""
        if row_index is not None:
            row_data=self.sparameter_data[row_index]
        if row_data is None:
            print("Could not convert row to complex, need a valid row_data string, list or dictionary or a row_index in "
                  "sparameter_data")
        out_row=[]
        try:
            if type(row_data) is StringType:
                row_data=re.search(self.row_pattern,row_data).groupdict()
            elif type(row_data) is ListType:
                row_data={self.column_names[index]:row_data[index] for index in range(3)}
            if type(row_data) is not DictionaryType:
                raise
            row_data={key:float(value) for key,value in row_data.iteritems()}
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

    def change_frequency_units(self,new_frequency_units=None):
        """Changes the frequency units from the current to new_frequency_units. Frequency Units must be one
        of the following: 'Hz','kHz','MHz', or 'GHz'. """
        multipliers={"yotta":10.**24,"Y":10.**24,"zetta":10.**21,"Z":10.**21,"exa":10.**18,"E":10.**18,"peta":10.**15,
                     "P":10.**15,"tera":10.**12,"T":10.**12,"giga":10.**9,"G":10.**9,"mega":10.**6,"M":10.**6,
                     "kilo":10.**3,"k":10.**3,"hecto":10.**2,"h":10.**2,"deka":10.,"da":10.,None:1.,"":1.,
                     "deci":10.**-1,"d":10.**-1,"centi":10.**-2,"c":10.**-2,"milli":10.**-3,"m":10.**-3,
                     "micro":10.**-6,"mu":10.**-6,u"\u00B5":10.**-6,"nano":10.**-9,
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
            for index,row in enumerate(self.sparameter_data):
                if type(self.sparameter_data[index][column_selector]) in [FloatType,LongType]:
                    #print "{0:e}".format(multipliers[old_prefix]/multipliers[new_prefix])
                    self.sparameter_data[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.sparameter_data[index][column_selector]
                elif type(self.sparameter_data[index][column_selector]) in [StringType,IntType]:
                    self.sparameter_data[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.sparameter_data[index][column_selector]))
                else:
                    print type(self.sparameter_data[index][column_selector])
                    raise

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
            print("Could not change the unit prefix of column {0}".format(column_selector))
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
            for row_index,row in enumerate(self.sparameter_data):
                frequency=self.sparameter_complex[row_index][0]
                dbS11=20.*math.log(abs(self.sparameter_complex[row_index][1]),10.)
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                self.sparameter_data[row_index]=[frequency,dbS11,argS11]

        elif re.match('ma',new_format,re.IGNORECASE):
            self.format="MA"
            self.option_line=self.option_line.replace(old_format,"MA")
            self.column_names=S1P_MA_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_MA_COLUMN_NAMES)
            for row_index,row in enumerate(self.sparameter_data):
                frequency=self.sparameter_complex[row_index][0]
                magS11=abs(self.sparameter_complex[row_index][1])
                argS11=(180./math.pi)*cmath.phase(self.sparameter_complex[row_index][1])
                self.sparameter_data[row_index]=[frequency,magS11,argS11]

        elif re.match('ri',new_format,re.IGNORECASE):
            self.format="RI"
            self.option_line=self.option_line.replace(old_format,"RI")
            self.column_names=S1P_RI_COLUMN_NAMES
            self.row_pattern=make_row_match_string(S1P_RI_COLUMN_NAMES)
            for row_index,row in enumerate(self.sparameter_data):
                frequency=self.sparameter_complex[row_index][0]
                reS11=self.sparameter_complex[row_index][1].real
                imS11=self.sparameter_complex[row_index][1].imag
                self.sparameter_data[row_index]=[frequency,reS11,imS11]
        else:
            print("Could not change data format the specified format was not DB, MA, or RI")
            return

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
                      for line in self.sparameter_data]
            return out_list
        except:raise

    def get_column(self,column_name=None,column_index=None):
        """Returns a column as a list given a column name or column index"""
        if column_name is None:
            if column_index is None:
                return
            else:
                column_selector=column_index
        else:
            column_selector=self.column_names.index(column_name)
        out_list=[self.sparameter_data[i][column_selector] for i in range(len(self.sparameter_data))]
        return out_list

    def show(self,type='matplotlib'):
        """Shows the touchstone file"""
        # plot data
        if re.search('smith',type,re.IGNORECASE):
            plt.figure(figsize=(8, 8))
            val1=[row[1] for row in self.sparameter_complex]
            ax = plt.subplot(1, 1, 1, projection='smith', axes_norm=50)
            plt.plot(val1, markevery=1, label="S11")
           #ax.plot_vswr_circle(0.3 - 0.7j, real=1, solution2=True, label="Re(Z)->1")
            plt.legend(loc="lower right")
            plt.title("Matplotlib Smith Chart Projection")
            plt.show()
        else:
            current_format=self.format
            self.change_data_format('MA')
            fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
            ax0.plot(self.get_column('Frequency'),self.get_column('magS11'),'k--')
            ax1.plot(self.get_column('Frequency'),self.get_column('argS11'),'ro')
            ax0.set_title('Magnitude S11')
            ax1.set_title('Phase S11')
            self.change_data_format(current_format)
            plt.show()

class S2PV1():
    """A container for s2p version 1 files. Files consist of comments, option line, S parameter data
     and noise parameter data"""
    def __init__(self,file_path=None,**options):
        """Initialization of the s2p class for version 1 files,
        if a file path is specified, it opens and parses the file. If the file path is not
        specified then data can be added through the s2pv1.sparameter_data. A reference to the version 1 touchstone
        format may be found at
        http://cp.literature.agilent.com/litweb/pdf/genesys200801/sim/linear_sim/sparams/touchstone_file_format.htm
        """
        defaults={"data_delimiter":"\t",
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
                  "sparameter_data":[],
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
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        self.elements=['sparameter_data','noiseparameter_data','comments','option_line']
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
            for key,value in match.groupdict().iteritems():
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
            # now we handle the cases if sparameter_data or sparameter_complex is specified
            if self.sparameter_data is [] and self.sparameter_complex is[]:
                pass
            elif self.sparameter_complex in [[],None]:
                for row in self.sparameter_data:
                    self.add_sparameter_complex_row(row)
                    #print("{0} is {1}".format("row",row))
            elif self.sparameter_data in [[],None]:
                self.sparameter_data=[[0,0,0,0,0,0,0,0,0] for row in self.sparameter_complex]
                #print self.sparameter_data
                self.change_data_format(new_format=self.format)
            if self.comments is None:
                number_line_comments=0
            else:
                number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
            self.options["sparameter_begin_line"]=number_line_comments+1
            self.options["sparameter_end_line"]= self.options["sparameter_begin_line"]\
                                                 +len(self.sparameter_data)+1

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


        for key,value in match.groupdict().iteritems():
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
        # remove the comments
        stripped_lines=strip_inline_comments(self.lines,begin_token="!",end_token="\n")
        #print stripped_lines
        self.sparameter_data=[]
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
        #print self.sparameter_data
        #print self.noiseparameter_data
        #print self.options["noiseparameter_begin_line"]

    def build_string(self,**temp_options):
        """Creates the output string"""
        #number of lines = option line + comments that start at zero + rows in sparameter data + rows in noise data
        original_options=self.options
        for key,value in temp_options.iteritems():
            self.options[key]=value
        if self.comments is None:
            number_line_comments=0
        else:
            number_line_comments=[str(comment[2]) for comment in self.comments].count('0')
        #print number_line_comments
        number_lines=1+number_line_comments+len(self.sparameter_data)+len(self.noiseparameter_data)
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
            elif self.sparameter_data not in [[],None] and index>=self.options["sparameter_begin_line"] and index <=self.options["sparameter_end_line"]:
                # print out_lines
                #print index
                out_lines[index]=self.options["sparameter_row_formatter_string"].format(
                    delimiter=self.options["data_delimiter"],
                    *self.sparameter_data[index-self.options["sparameter_begin_line"]])

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

    def __str__(self):
        self.string=self.build_string()
        return self.string

    def save(self,file_path=None,**temp_options):
        """Saves the s2p file to file_path with options, defaults to s2p.path"""
        if file_path is None:
            file_path=self.path
        out_file=open(file_path,'w')
        out_file.write(self.build_string(**temp_options))
        out_file.close()

    def add_sparameter_row(self,row_data):
        """Adds data to the sparameter attribute, which is a list of s-parameters. The
        data can be a list of 9 real numbers
         or dictionary with appropriate column names, note column names are not case sensitive"""
        if type(row_data) is ListType:
            if len(row_data) == 9:
                    self.sparameter_data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if type(row_data) is DictionaryType:
            new_row=[]
            for column_name in self.column_names:
                #print row_data
                new_row.append(float(row_data[column_name]))
            self.sparameter_data.append(new_row)
        self.options["sparameter_end_line"]+=1
        self.options["noiseparameter_begin_line"]+=1
        self.options["noiseparameter_end_line"]+=1

    def add_sparameter_complex_row(self,row_data):
        """Adds a row to the sparameter_complex attribute. This attribute stores the values of the sparameter table in
        complex form for easy conversion and manipulation. Row_data is assumed to be of the same form that would be
        given to add_sparameter_row"""

        if type(row_data) is ListType and len(row_data)==5 and type(row_data[1]) is ComplexType:
            self.sparameter_complex.append(row_data)
        else:
            row_data=self.sparameter_row_to_complex(row_data=row_data)
            self.sparameter_complex.append(row_data)

    def sparameter_row_to_complex(self,row_data=None,row_index=None):
        """Given a row_data string, row_data list, or row_data dictionary it converts the values of the sparameter to
         complex notation (complex types) and returns a single list with 5 elements [Frequency,S11,S21,S12,S22]"""
        if row_index is not None:
            row_data=self.sparameter_data[row_index]
        if row_data is None:
            print("Could not convert row to complex, need a valid row_data string, list or dictionary or a row_index in "
                  "sparameter_data")
        out_row=[]
        try:
            if type(row_data) is StringType:
                row_data=re.search(self.row_pattern,row_data).groupdict()
            elif type(row_data) is ListType:
                row_data={self.column_names[index]:row_data[index] for index in range(9)}
            if type(row_data) is not DictionaryType:
                raise
            row_data={key:float(value) for key,value in row_data.iteritems()}
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
        if type(row_data) is ListType:
            if len(row_data) == 5:
                    self.noiseparameter_data.append(row_data)
            else:
                print("Could not add row, the data was a list of the wrong dimension, if you desire to add multiple"
                      "rows use add_sparameter_rows")
                return
        if type(row_data) is DictionaryType:
            new_row=[]
            for column_name in self.noiseparameter_column_names:
                new_row.append(float(row_data[column_name]))
            self.noiseparameter_data.append(new_row)
        self.options["noiseparameter_end_line"]+=1
    #TODO:Add this to unit tests and fix it
    def change_frequency_units(self,new_frequency_units=None):
        """Changes the frequency units from the current to new_frequency_units. Frequency Units must be one
        of the following: 'Hz','kHz','MHz', or 'GHz'. """
        multipliers={"yotta":10.**24,"Y":10.**24,"zetta":10.**21,"Z":10.**21,"exa":10.**18,"E":10.**18,"peta":10.**15,
                     "P":10.**15,"tera":10.**12,"T":10.**12,"giga":10.**9,"G":10.**9,"mega":10.**6,"M":10.**6,
                     "kilo":10.**3,"k":10.**3,"hecto":10.**2,"h":10.**2,"deka":10.,"da":10.,None:1.,"":1.,
                     "deci":10.**-1,"d":10.**-1,"centi":10.**-2,"c":10.**-2,"milli":10.**-3,"m":10.**-3,
                     "micro":10.**-6,"mu":10.**-6,u"\u00B5":10.**-6,"nano":10.**-9,
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
            for index,row in enumerate(self.sparameter_data[:]):
                if type(self.sparameter_data[index][column_selector]) in [FloatType,LongType]:
                    #print "{0:e}".format(multipliers[old_prefix]/multipliers[new_prefix])
                    self.sparameter_data[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.sparameter_data[index][column_selector]
                elif type(self.sparameter_data[index][column_selector]) in [StringType,IntType]:
                    self.sparameter_data[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.sparameter_data[index][column_selector]))
                else:
                    print type(self.sparameter_data[index][column_selector])
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
                    print type(self.noiseparameter_data[index][column_selector])
                    raise
            self.frequency_units=new_frequency_units
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
            print("Could not change the unit prefix of column {0}".format(column_selector))
            raise

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
                self.sparameter_data[row_index]=[frequency,dbS11,argS11,dbS21,argS21,dbS12,argS12,dbS22,argS22]

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
                self.sparameter_data[row_index]=[frequency,magS11,argS11,magS21,argS21,magS12,argS12,magS22,argS22]

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
                self.sparameter_data[row_index]=[frequency,reS11,imS11,reS21,imS21,reS12,imS12,reS22,imS22]
        else:
            print("Could not change data format the specified format was not DB, MA, or RI")
            return

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
                      for line in self.sparameter_data]
            return out_list
        except:raise

    def correct_switch_terms(self,switch_terms=None,switch_terms_format=None):
        """Corrects sparameter data for switch terms. Switch terms must be a list with a row of format
        [Frequency,SWF,SWR] where SWF is the complex foward switch term (SWport2),
        SWR is the complex reverse switch term (SWport1)"""
        self.corrected_sparameter_data=[]
        for index,row in enumerate(self.sparameter_complex):
            SWF=switch_terms[index][1]
            SWR=switch_terms[index][2]
            [S11,S21,S12,S22]=row[1:]
            D=1-S21*S12*SWR*SWF
            S11_corrected=(S11-S12*S21*SWF)/D
            S21_corrected=(S21-S22*S21*SWF)/D
            S12_corrected=(S12-S11*S12*SWR)/D
            S22_corrected=(S22-S12*S21*SWR)/D
            self.corrected_sparameter_data.append([row[0],S11_corrected,S21_corrected,S12_corrected,S22_corrected])
    def get_column(self,column_name=None,column_index=None):
        """Returns a column as a list given a column name or column index"""
        if column_name is None:
            if column_index is None:
                return
            else:
                column_selector=column_index
        else:
            column_selector=self.column_names.index(column_name)
        out_list=[self.sparameter_data[i][column_selector] for i in range(len(self.sparameter_data))]
        return out_list

    def show(self,type='matplotlib'):
        """Shows the touchstone file"""
        # plot data
        if re.search('smith',type,re.IGNORECASE):
            plt.figure(figsize=(8, 8))
            val1=[row[1] for row in self.sparameter_complex]
            val2=[row[4] for row in self.sparameter_complex]
            ax = plt.subplot(1, 1, 1, projection='smith', axes_norm=50)
            plt.plot(val1, markevery=1, label="S11")
            plt.plot(val2, markevery=1, label="S22")
           #ax.plot_vswr_circle(0.3 - 0.7j, real=1, solution2=True, label="Re(Z)->1")
            plt.legend(loc="lower right")
            plt.title("Matplotlib Smith Chart Projection")
            plt.show()
        else:
            current_format=self.format
            self.change_data_format('MA')
            fig, axes = plt.subplots(nrows=3, ncols=2)
            ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat
            ax0.plot(self.get_column('Frequency'),self.get_column('magS11'),'k-o')
            ax0.set_title('Magnitude S11')
            ax1.plot(self.get_column('Frequency'),self.get_column('argS11'),'ro')
            ax1.set_title('Phase S11')
            ax2.plot(self.get_column('Frequency'),self.get_column('magS21'),'k-o')
            ax2.plot(self.get_column('Frequency'),self.get_column('magS12'),'b-o')
            ax2.set_title('Magnitude S21 and S12')
            ax3.plot(self.get_column('Frequency'),self.get_column('argS21'),'ro')
            ax3.plot(self.get_column('Frequency'),self.get_column('argS12'),'bo')
            ax3.set_title('Phase S21 and S12')
            ax4.plot(self.get_column('Frequency'),self.get_column('magS22'),'k-o')
            ax4.set_title('Magnitude S22')
            ax5.plot(self.get_column('Frequency'),self.get_column('argS22'),'ro')
            ax5.set_title('Phase S22')
            plt.tight_layout()
            self.change_data_format(current_format)
            plt.show()


#-----------------------------------------------------------------------------
# Module Scripts
def test_option_string():
    """Tests the regex for extracting option string values"""
    match=re.search(OPTION_LINE_PATTERN,"# GHz S RI R 50")
    print match.groupdict()
    print match.groupdict()["Format"] in FORMATS

def test_S1PV1(file_path="OnePortTouchstoneTestFile.s1p"):
    """Tests the s2pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S1PV1(file_path)
    print new_table
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='DB')
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='MA')
    print_s1p_attributes(new_table=new_table)
    new_table.change_data_format(new_format='RI')
    print_s1p_attributes(new_table=new_table)
    print new_table
    new_table.show()

def test_s2pv1(file_path="thru.s2p"):
    """Tests the s2pv1 class"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S2PV1(file_path)
    print new_table
    print("The Table as read in with line numbers is")
    for index,line in enumerate(new_table.lines):
        print("{0} {1}".format(index,line))
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_data',str(new_table.sparameter_data)))
    print("-"*80)
    print("The attribute {0} is {1}".format('sparameter_complex',str(new_table.sparameter_complex)))
    print("-"*80)
    print("The attribute {0} is {1}".format('noiseparameter_data',str(new_table.noiseparameter_data)))
    print("-"*80)
    print("The attribute {0} is {1}".format('comments',str(new_table.comments)))
    print("-"*80)
    print("The attribute {0} is {1}".format('option_line',str(new_table.option_line)))
    print("-"*80)
    print("The attribute {0} is {1}".format('format',str(new_table.format)))
    print("-"*80)
    print("The attribute {0} is {1}".format('frequncy_units',str(new_table.frequency_units)))
    print("-"*80)
    print("The attribute {0} is {1}".format('column_names',str(new_table.column_names)))
    print("-"*80)
    print("The attribute {0} is {1}".format('noiseparameter_column_names',str(new_table.noiseparameter_column_names)))

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
    print new_table
    new_table.show()
def test_change_frequency_units(file_path="thru.s2p"):
    """Tests the models change_frequnecy_units method"""
    os.chdir(TESTS_DIRECTORY)
    new_table=S2PV1(file_path)
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    new_table.change_frequency_units("Hz")
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    new_table.change_frequency_units("MHz")
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    new_table.change_frequency_units("kHz")
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    new_table.change_frequency_units("THz")
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    new_table.change_frequency_units("Hz")
    print("The frequency units are {0},"
          "and the frequency values are {1}".format(new_table.frequency_units,
                                             new_table.get_column("Frequency")))
    print new_table
    new_table.show()
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_S1PV1()
    #test_option_string()
    #test_s2pv1()
    #test_s2pv1('TwoPortTouchstoneTestFile.s2p')
    #test_change_format()
    #test_change_format('TwoPortTouchstoneTestFile.s2p')
    #test_change_format('20160301_30ft_cable_0.s2p')
    #test_change_frequency_units()
    #test_s2pv1('704b.S2P')
    test_change_format('704b.S2P')