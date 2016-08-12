#-----------------------------------------------------------------------------
# Name:        NISTModels
# Purpose:    To handle data generated at NIST Boulder
# Author:      Aric Sanders
# Created:     2/22/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" NISTModels is a module to handle data types found at NIST in Boulder, CO """

#-----------------------------------------------------------------------------
# Standard Imports
import os
import fnmatch
import datetime
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
    from pyMeasure.Code.DataHandlers.TouchstoneModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.TouchstoneModels was not found,"
          "please put it on the python path")
    raise ImportError

try:
    import numpy as np
except:
    print("The module numpy was not found,"
          "please put it on the python path")
    raise ImportError
try:
    import matplotlib.pyplot as plt
except:
    print("The module matplotlib was not found,"
          "please put it on the python path")
#-----------------------------------------------------------------------------
# Module Constants
ONE_PORT_COLUMN_NAMES=["Frequency", "mag", "uMb", "uMa", "uMd", "uMg", "arg",
                                    "uAb", "uAa", "uAd", "uAg"]
#Note there are 2 power models!!! one with 4 error terms and one with 3
POWER_4TERM_COLUMN_NAMES=['Frequency','Efficiency','uEb', 'uEa','uEd','uEg',
                    'Calibration_Factor','uCb','uCa','uCd','uCg']
#todo: change this description to reflect the column names
POWER_4TERM_COLUMN_DESCRIPTIONS={"Frequency": "Frequency in GHz",
                                           "Efficiency":"Effective Efficiency",
                                           "uEs": "Uncertainty in efficiency due to standards",
                                           "uEc": "Uncertainty in efficiency for repeated connects",
                                           "uEe": "Total uncertainty in Efficiency",
                                           "Calibration_Factor": "Effective efficiency modified by reflection coefficient",
                                           "uCs": "Uncertainty in calibration factor due to standards",
                                           "uCc": "Uncertainty in calibration factor for repeated connects",
                                           "uCe": "Total uncertainty in calibration factor"}
POWER_3TERM_COLUMN_NAMES=['Frequency','Efficiency','uEs', 'uEc','uEe',
                    'Calibration_Factor','uCs','uCc','uCe']
POWER_3TERM_COLUMN_DESCRIPTIONS={"Frequency": "Frequency in GHz",
                                           "Efficiency":"Effective Efficiency",
                                           "uEs": "Uncertainty in efficiency due to standards",
                                           "uEc": "Uncertainty in efficiency for repeated connects",
                                           "uEe": "Total uncertainty in Efficiency",
                                           "Calibration_Factor": "Effective efficiency modified by reflection coefficient",
                                           "uCs": "Uncertainty in calibration factor due to standards",
                                           "uCc": "Uncertainty in calibration factor for repeated connects",
                                           "uCe": "Total uncertainty in calibration factor"}
#POWER_COLUMN_NAMES=POWER_3TERM_COLUMN_NAMES
TWELVE_TERM_ERROR_COLUMN_NAMES=["Frequency","reEdf","imEdf","reEsf","imEsf",
                                "reErf","imErf","reExf","imExf","reElf","imElf","reEtf","imEtf"
                                "reEdr","imEdr","reEsr","imEsr","reErr","imErr","reExr","imExr"
                                "reElr","imElr","reEtr","imEtr"]
# Constant that determines if S21 is in db-angle or mag-angle format true is in mag-angle
CONVERT_S21=True
# Constant that determines if 1-port raw files have S11 and S22 or just S11
COMBINE_S11_S22=True
#-----------------------------------------------------------------------------
# Module Functions
def asc_type(file_contents):
    """asc_type determines the type of asc file given it's contents, returns the class name of the appropriate model"""
    if type(file_contents) is StringType:
        contents=file_contents
    elif type(file_contents) is ListType:
        contents=string_list_collapse(file_contents)
    else:
        return None
    if re.search('table 1',contents,re.IGNORECASE) and re.search('table 2',contents,re.IGNORECASE) and re.search('table 3',contents,re.IGNORECASE):
        return 'TwoPortCalrepModel'
    elif re.search('table 1',contents,re.IGNORECASE) and re.search('table 2',contents,re.IGNORECASE):
        return 'PowerCalrepModel'
    elif re.search('table 1',contents,re.IGNORECASE):
        return 'OnePortCalrepModel'
    else:
        return None

def raw_type(file_contents):
    """Given the contents of a file in a list of lines or a single string returns the raw class name. It is assumed
    that the type of file is the 5th line of the header"""
    if type(file_contents) is StringType:
        lines=file_contents.splitlines()
    elif type(file_contents) is ListType:
        lines=file_contents
    #print("The value of {0} is {1}".format('lines[4]',lines[4]))
    out=None
    if re.search('1-port',lines[4],re.IGNORECASE):
        out='OnePortRawModel'
    elif re.search('2-port',lines[4],re.IGNORECASE) and not re.search('2-portNR',lines[4],re.IGNORECASE):
        out='TwoPortRawModel'
    elif re.search('2-portNR',lines[4],re.IGNORECASE):
        out='TwoPortNRRawModel'
    elif re.search('Thermistor|Dry Cal',lines[4],re.IGNORECASE):
        out='PowerRawModel'
    return out

def sparameter_power_type(file_path):
    """sparameter_power_type returns the class name of file given a file path"""
    extension=file_path.split('.')[-1]
    #print extension
    in_file=open(file_path,'r')
    lines=[]
    for line in in_file:
        lines.append(line)
    in_file.close()
    if re.match('asc',extension,re.IGNORECASE):
        #print("The value of {0} is {1}".format('extension',extension))
        # handle asc files
        out=asc_type(lines)
    elif re.match('[\w][\d]+_[\d]+',extension,re.IGNORECASE):
        #print("The value of {0} is {1}".format('extension',extension))
        out=raw_type(lines)
    return out

def calrep_to_benchmark(file_path):
    """Creates a benchmark list given a path to a calrep file, assumes column names are 2 lines after
    the occurrence of the last /"""
    in_file=open(file_path,'r')
    lines=[]
    for line in in_file:
        lines.append(line)
    block_end=re.compile('/')
    for index,line in enumerate(lines):
        if re.match(block_end,line):
            last_block_comment_line=index
    header=lines[0:last_block_comment_line+1]
    columns_line=last_block_comment_line+2
    column_names=lines[columns_line].split(' ')
    data=lines[columns_line+1:None]
    return [header,column_names,data]

def build_csv_from_raw(input_file_names_list,output_file_name,model_name):
    """Build csv from raw  takes a list of file names conforming to model and builds a single csv.
    It is intentioned to accept raw files from the sparameter power project that have been converted from bdat
    using Ron Ginely's converter (modified calrep program). The output is a single csv file with metadata added
    as extra columns (ie a denormalized table)"""
    try:
        # our current definition of metadata keys for all of the raw models
        metadata_keys=["System_Id","System_Letter","Connector_Type_Calibration","Connector_Type_Measurement",
              "Measurement_Type","Measurement_Date","Measurement_Time","Program_Used","Program_Revision","Operator",
              "Calibration_Name","Calibration_Date","Port_Used","Number_Connects","Number_Repeats","Nbs",
              "Number_Frequencies","Start_Frequency",
              "Device_Description","Device_Id"]
        # import the first file
        model=globals()[model_name]
        initial_file=model(input_file_names_list[0])
        # Add the metadata columns and replace any commas with -
        for column_name in metadata_keys:
            initial_file.add_column(column_name=column_name,column_type='str',
                            column_data=[initial_file.metadata[column_name].replace(',','-')
                                         for row in initial_file.data])
        # We also add a column at the end that is Measurement_Timestamp, that is
        # Measurement_Time+Measurement_Date in isoformat
        timestamp=initial_file.metadata["Measurement_Date"]+" "+initial_file.metadata["Measurement_Time"]
        datetime_timestamp=datetime.datetime.strptime(timestamp,'%d %b %Y %H:%M:%S')
        measurement_timestamp=datetime_timestamp.isoformat(' ')
        initial_file.add_column(column_name="Measurement_Timestamp",column_type='str',
                            column_data=[measurement_timestamp
                                         for row in initial_file.data])
        # now we save the intial file with its column names but not its header
        initial_file.header=None
        initial_file.save(output_file_name)

        # Now we re-open this file in the append mode and read-in each new file and append it. This seems to work
        # for very large data sets, where as keeping a single object in memory fails
        out_file=open(output_file_name,'a')
        # now we do the same thing over and over and add it to the out file
        for file_name in input_file_names_list[1:]:

            model=globals()[model_name]
            parsed_file=model(file_name)
            for column_name in metadata_keys:
                parsed_file.add_column(column_name=column_name,column_type='str',
                            column_data=[parsed_file.metadata[column_name].replace(',','-')
                                         for row in parsed_file.data])
            timestamp=parsed_file.metadata["Measurement_Date"]+" "+parsed_file.metadata["Measurement_Time"]
            datetime_timestamp=datetime.datetime.strptime(timestamp,'%d %b %Y %H:%M:%S')
            measurement_timestamp=datetime_timestamp.isoformat(' ')
            parsed_file.add_column(column_name="Measurement_Timestamp",column_type='str',
                            column_data=[measurement_timestamp
                                         for row in parsed_file.data])
            # add an endline before appending
            out_file.write('\n')
            # now we only want the data string
            data=parsed_file.get_data_string()
            out_file.write(data)
        # close the file after  loop
        out_file.close()
    # Catch any errors
    except:
            raise

#-----------------------------------------------------------------------------
# Module Classes
class OnePortCalrepModel(AsciiDataTable):
    def __init__(self,file_path,**options):
        "Intializes the OnePortCalrepModel Class, it is assumed that the file is of the .asc or table type"
        # This is a general pattern for adding a lot of options
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'One_Port',
                   "general_descriptor": 'Sparameter', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "column_types": ['float' for i in range(11)],
                   "column_descriptions": {"Frequency": "Frequency in GHz", "Magnitude": "Linear magnitude",
                                           "uMb": "Uncertainty in magnitude due to standards",
                                           "uMa": "Uncertainty in magnitude due to electronics",
                                           "uMd": "Uncertainty in magnitude for repeated connects",
                                           "uMg": "Total uncertainty in magnitude",
                                           "Phase": "Phase in degrees",
                                           "uPhb": "Uncertainty in phase due to standards",
                                           "uPha": "Uncertainty in phase due to electronics",
                                           "uPhd": "Uncertainty in phase for repeated connects",
                                           "uPhg": "Total uncertainty in phase"}, "header": None,
                   "column_names": ONE_PORT_COLUMN_NAMES, "column_names_end_token": "\n", "data": None,
                   "row_formatter_string": None, "data_table_element_separator": None,"row_begin_token":None,
                   "row_end_token":None,"escape_character":None,
                   "data_begin_token":None,"data_end_token":None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        self.metadata={}
        if file_path is not None:
            self.path=file_path
            self.__read_and_fix__()

        #build the row_formatting string, the original files have 4 decimals of precision for freq/gamma and 2 for Phase
        row_formatter=""
        for i in range(11):
            if i<6:
                row_formatter=row_formatter+"{"+str(i)+":.4f}{delimiter}"
            elif i==10:
                row_formatter=row_formatter+"{"+str(i)+":.2f}"
            else:
                row_formatter=row_formatter+"{"+str(i)+":.2f}{delimiter}"
        self.options["row_formatter_string"]=row_formatter
        AsciiDataTable.__init__(self,None,**self.options)
        if file_path is not None:
            self.path=file_path

    def __read_and_fix__(self):
        """Reads in a 1 port ascii file and fixes any issues with inconsistent delimiters, etc"""
        lines=[]
        table_type=self.path.split(".")[-1]
        in_file=open(self.path,'r')
        for line in in_file:
            #if not re.match('[\s]+(?!\w+)',line):
                #print line
            lines.append(line)
        in_file.close()
        # Handle the cases in which it is the comma delimited table
        if re.match('txt',table_type,re.IGNORECASE):
            lines=strip_tokens(lines,*[self.options['data_begin_token'],
                                                    self.options['data_end_token']])
            self.options["data"]=strip_all_line_tokens(lines,begin_token=self.options["row_begin_token"],
                                            end_token=self.options["row_end_token"])
            self.options["data"]=split_all_rows(self.options["data"],delimiter=self.options["data_delimiter"],
                                     escape_character=self.options["escape_character"])
            self.options["data"]=convert_all_rows(self.options["data"],self.options["column_types"])
            #print self.options["data"]
            root_name_pattern=re.compile('(?P<root_name>\w+)[abc].txt',re.IGNORECASE)
            root_name_match=re.search(root_name_pattern,self.path)
            if root_name_match:
                root_name=root_name_match.groupdict()["root_name"]
            else:
                root_name=self.path.split('.')[0]
            self.options["header"]=["Device_Id = {0}".format(root_name)]

        elif re.match("asc",table_type,re.IGNORECASE):
            self.lines=lines
            data_begin_line=self.find_line("TABLE")+2
            # TODO: Replace with parse lines, it ignores blank lines
            data=np.loadtxt(self.path,skiprows=data_begin_line)
            self.options["data"]=data.tolist()
            self.options["header"]=lines[:self.find_line("TABLE")]
            self.metadata["Device_Id"]=lines[0].rstrip().lstrip()
            self.metadata["Analysis_Date"]=lines[1].rstrip().lstrip()
            self.options["metadata"]={"Device_Id":lines[0].rstrip().lstrip(),
                                      "Analysis_Date":lines[1].rstrip().lstrip()}
            print("The {0} variable is {1}".format('self.metadata["Device_Id"]',self.metadata["Device_Id"]))
            #print("The {0} variable is {1}".format('data.tolist()',data.tolist()))

    def show(self):
        fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
        ax0.errorbar(self.get_column('Frequency'),self.get_column('mag'),
             yerr=self.get_column('uMg'),fmt='k--')
        ax0.set_title('Magnitude S11')
        ax1.errorbar(self.get_column('Frequency'),self.get_column('arg'),
             yerr=self.get_column('uAg'),fmt='ro')
        ax1.set_title('Phase S11')
        plt.show()

class PowerModel(AsciiDataTable):
    def __init__(self,file_path,**options):
        "Intializes the PowerModel Class, it is assumed that the file is of  table type"
        # This is a general pattern for adding a lot of options
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'One_Port',
                   "general_descriptor": 'Power', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "header": None,
                   "column_names":None, "column_names_end_token": "\n", "data": None,
                   "row_formatter_string": None, "data_table_element_separator": None,"row_begin_token":None,
                   "row_end_token":None,"escape_character":None,
                   "data_begin_token":None,"data_end_token":None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is not None:
            self.power_4term_row_pattern=make_row_match_string(POWER_4TERM_COLUMN_NAMES)
            self.power_3term_row_pattern=make_row_match_string(POWER_3TERM_COLUMN_NAMES)
            self.path=file_path
            self.__read_and_fix__()
        #build the row_formatting string, the original files have 4 decimals of precision for freq/gamma and 2 for Phase
        row_formatter=""
        for i in range(len(self.options["column_names"])):
            if i<len(self.options["column_names"])-1:
                row_formatter=row_formatter+"{"+str(i)+":.4f}{delimiter}"
            elif i==len(self.options["column_names"])-1:
                row_formatter=row_formatter+"{"+str(i)+":.4f}"
        self.options["row_formatter_string"]=row_formatter
        AsciiDataTable.__init__(self,None,**self.options)
        if file_path is not None:
            self.path=file_path

    def __read_and_fix__(self):
        """Reads in a power ascii file and fixes any issues with inconsistent delimiters, etc"""
        lines=[]
        table_type=self.path.split(".")[-1]
        in_file=open(self.path,'r')
        for line in in_file:
            if not re.match('[\s]+(?!\w+)',line):
                #print line
                lines.append(line)
        # Handle the cases in which it is the comma delimited table
        # Does this need to be parse lines or numpy.loadtxt?
        if re.match('txt',table_type,re.IGNORECASE):
            lines=strip_tokens(lines,*[self.options['data_begin_token'],
                                                    self.options['data_end_token']])
            self.options["data"]=strip_all_line_tokens(lines,begin_token=self.options["row_begin_token"],
                                            end_token=self.options["row_end_token"])
            self.options["data"]=split_all_rows(self.options["data"],delimiter=self.options["data_delimiter"],
                                     escape_character=self.options["escape_character"])
            print("{0} is {1}".format("len(self.options['data'][0])",len(self.options['data'][0])))
            if len(self.options['data'][0])==9:
                self.power_pattern=self.power_3term_row_pattern
                self.options["column_names"]=POWER_3TERM_COLUMN_NAMES
                self.options["column_descriptions"]=POWER_3TERM_COLUMN_DESCRIPTIONS
            elif len(self.options['data'][0])==11:
                self.power_pattern=self.power_4term_row_pattern
                self.options["column_names"]=POWER_4TERM_COLUMN_NAMES
                self.options["column_descriptions"]=POWER_4TERM_COLUMN_DESCRIPTIONS
            self.options["column_types"]= ['float' for i in range(len(self.options["column_names"]))]
            self.options["data"]=convert_all_rows(self.options["data"],self.options["column_types"])
            #print self.options["data"]
            root_name_pattern=re.compile('(?P<root_name>\w+)[abc].txt',re.IGNORECASE)
            root_name_match=re.search(root_name_pattern,self.path)
            root_name=root_name_match.groupdict()["root_name"]
            self.options["header"]=["Device_Id = {0}".format(root_name)]



class OnePortRawModel(AsciiDataTable):
    """ Class that deals with the OnePort Raw Files after conversion to Ascii using Ron Ginley's converter.
    These files typically have header information seperated from data by !!
    Header format is:
    Line 1:		Spid$ - identification of type of system used
    Line 2:		Systemletter$ - letter name indicating which system was used
    Line 3:		Conncal$ - connector type from the system calibration
    Line 4:		Connectors$ - connector type used for the measurement
    Line 5:		Meastype$ - type of measurement (basically 1-port, 2-port or power)
    Line 6:		Datea$ - date of measurement
    Line 7:		Timea$ - time of measurement
    Line 8:		Programm$ - name of program used
    Line 9:		Rev$ - program revision
    Line 10:	Opr$ - operator
    Line 11:	Cfile$ - calibration name
    Line 12:	Cdate$ - calibration date
    Line 13:	Sport - identification of which port or direction was used for measurement
    Line 14:	Numconnects ? number of disconnect/reconnect cycles
    Line 15:	Numrepeats ? number of repeat measurements for each connect (usually 1)
    Line 16:	Nbs ? not sure
    Line 17:	Nfreq ? number of frequencies
    Line 18:	Startfreq ? data row pointer for bdat files
    Line 19:	Devicedescript$ - description of device being measured or of test being done
    Line 20:	Devicenum$ - Identifying number for device ? used for file names
    """
    def __init__(self,file_path=None,**options):
        """Initializes the OnePortRaw class, if a file_path is specified opens an existing file, else creates an
        empty container"""
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'One_Port_Raw',
                   "general_descriptor": 'Sparameter', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "column_types": ['float','int','int','float','float','float','float'],
                   "column_descriptions": {"Frequency":"Frequency in GHz",
                                           "Direction":"Direction of connects, may be unused",
                                           "Connect":"Connect number", "magS11":"Linear magnitude for port 1",
                                           "argS11":"Phase in degrees for port 1",
                                           "magS22":"Linear magnitude for port 2",
                                           "argS22":"Phase in degrees for port 2"}, "header": None,
                   "column_names": ["Frequency","Direction","Connect", "magS11",
                                    "argS11","magS22",  "argS22"],
                   "column_names_end_token": "\n", "data": None,
                   'row_formatter_string': "{0:.5f}{delimiter}{1}{delimiter}{2}{delimiter}"
                                           "{3:.4f}{delimiter}{4:.2f}{delimiter}{5:.4f}{delimiter}{6:.2f}",
                   "data_table_element_separator": None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value

        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is not None:
            self.__read_and_fix__(file_path)
        if COMBINE_S11_S22:
            self.options['row_formatter_string']= "{0:.5f}{delimiter}{1}{delimiter}{2}{delimiter}{3:.4f}{delimiter}{4:.2f}"
            self.options["column_types"]= ['float','int','int','float','float']
            self.options["column_names"]=["Frequency","Direction","Connect", "mag","arg"]
            self.options["column_descriptions"]= {"Frequency":"Frequency in GHz",
                                           "Direction":"Direction of connects, may be unused",
                                           "Connect":"Connect number", "mag":"Linear magnitude",
                                           "arg":"Phase in degrees"}
        AsciiDataTable.__init__(self,None,**self.options)
        self.path=file_path
        self.structure_metadata()


    def __read_and_fix__(self,file_path=None):
        """Inputs in the raw OnePortRaw file and fixes any problems with delimiters,etc."""
        lines=[]
        in_file=open(file_path,'r')
        for index,line in enumerate(in_file):
            lines.append(line)
            if re.match("!!",line):
                data_begin_line=index+1
        self.lines=lines
        in_file.close()
        parse_options={"row_end_token":'\n',
                       "row_pattern":make_row_match_string(self.options["column_names"]),
                       "column_names":self.options["column_names"],"column_types":self.options["column_types"]}
        data=parse_lines(lines[data_begin_line:],**parse_options)
        self.options["data"]=data
        self.options["header"]=lines[:data_begin_line-1]
        if COMBINE_S11_S22:
            new_data=[]
            for index,row in enumerate(self.options["data"][:]):
                new_row=[row[0],row[1],row[2],row[3]+row[5],row[4]+row[6]]
                new_data.append(new_row)
            self.options["data"]=new_data



    def structure_metadata(self):
        """Returns a dictionary of key,value pairs extracted from the header"""
        keys=["System_Id","System_Letter","Connector_Type_Calibration","Connector_Type_Measurement",
              "Measurement_Type","Measurement_Date","Measurement_Time","Program_Used","Program_Revision","Operator",
              "Calibration_Name","Calibration_Date","Port_Used","Number_Connects","Number_Repeats","Nbs",
              "Number_Frequencies","Start_Frequency",
              "Device_Description","Device_Id"]
        self.metadata={}
        if self.header is None:
            pass
        else:
            for index,key in enumerate(keys):
                self.metadata[key]=self.header[index].rstrip().lstrip()
    def show(self):
        fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
        if COMBINE_S11_S22:
            ax0.plot(self.get_column('Frequency'),self.get_column('mag'),'k--')
            ax1.plot(self.get_column('Frequency'),self.get_column('arg'),'ro')
        else:
            ax0.plot(self.get_column('Frequency'),self.get_column('magS11'),'k--')
            ax0.plot(self.get_column('Frequency'),self.get_column('magS22'),'k--')
            ax1.plot(self.get_column('Frequency'),self.get_column('argS11'),'ro')
            ax1.plot(self.get_column('Frequency'),self.get_column('argS22'),'ro')
        ax0.set_title('Magnitude S11')
        ax1.set_title('Phase S11')
        plt.show()

class TwoPortRawModel(AsciiDataTable):
    """ Class that deals with the TwoPort Raw Files after conversion to Ascii using Ron Ginley's converter.
    These files typically have header information seperated from data by !!
    Header format is:
    Line 1:		Spid$ - identification of type of system used
    Line 2:		Systemletter$ - letter name indicating which system was used
    Line 3:		Conncal$ - connector type from the system calibration
    Line 4:		Connectors$ - connector type used for the measurement
    Line 5:		Meastype$ - type of measurement (basically 1-port, 2-port or power)
    Line 6:		Datea$ - date of measurement
    Line 7:		Timea$ - time of measurement
    Line 8:		Programm$ - name of program used
    Line 9:		Rev$ - program revision
    Line 10:	Opr$ - operator
    Line 11:	Cfile$ - calibration name
    Line 12:	Cdate$ - calibration date
    Line 13:	Sport - identification of which port or direction was used for measurement
    Line 14:	Numconnects ? number of disconnect/reconnect cycles
    Line 15:	Numrepeats ? number of repeat measurements for each connect (usually 1)
    Line 16:	Nbs ? not sure
    Line 17:	Nfreq ? number of frequencies
    Line 18:	Startfreq ? data row pointer for bdat files
    Line 19:	Devicedescript$ - description of device being measured or of test being done
    Line 20:	Devicenum$ - Identifying number for device ? used for file names
    """
    def __init__(self,file_path=None,**options):
        """Initializes the TwoPortRaw class, if a file_path is specified opens an existing file, else creates an
        empty container"""
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'Two_Port_Raw',
                   "general_descriptor": 'Sparameter', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "column_types": ['float','int','int','float','float','float','float','float','float'],
                   "column_descriptions": {"Frequency":"Frequency in GHz",
                                           "Direction":"Direction of connects, may be unused",
                                           "Connect":"Connect number", "magS11":"Linear magnitude for S11",
                                           "argS11":"Phase in degrees for S11",
                                           "magS21":"Linear magnitude for S21",
                                           "argS21":"Phase in degrees for S21",
                                           "magS22":"Linear magnitude for S22",
                                           "argS22":"Phase in degrees for S22"},
                   "header": None,
                   "column_names": ["Frequency","Direction","Connect", "magS11",
                                    "argS11","magS21","argS21","magS22","argS22"],
                   "column_names_end_token": "\n", "data": None,
                   'row_formatter_string': "{0:.5f}{delimiter}{1}{delimiter}{2}"
                                           "{delimiter}{3:.4f}{delimiter}{4:.2f}{delimiter}"
                                           "{5:.4f}{delimiter}{6:.2f}{delimiter}"
                                           "{7:.4f}{delimiter}{8:.2f}",
                   "data_table_element_separator": None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is not None:
            self.__read_and_fix__(file_path)

        AsciiDataTable.__init__(self,None,**self.options)
        self.path=file_path
        self.structure_metadata()

    def __read_and_fix__(self,file_path=None):
        """Inputs in the raw OnePortRaw file and fixes any problems with delimiters,etc."""
        lines=[]
        data_begin_line=0
        in_file=open(file_path,'r')
        for index,line in enumerate(in_file):
            lines.append(line)
            if re.search("!!",line):
                data_begin_line=index+1
        self.lines=lines
        in_file.close()
        parse_options={"row_end_token":'\n',
                       "row_pattern":make_row_match_string(self.options["column_names"]),
                       "column_names":self.options["column_names"],"column_types":self.options["column_types"]}
        data=parse_lines(lines[data_begin_line:],**parse_options)
        self.options["data"]=data
        if CONVERT_S21:
            for row_index,row in enumerate(self.options["data"]):
                db_value=row[5]
                mag_value=10.**(-1*db_value/20.)
                self.options["data"][row_index][5]=mag_value

        self.options["header"]=lines[:data_begin_line-1]
        #print data


    def structure_metadata(self):
        """Returns a dictionary of key,value pairs extracted from the header"""
        keys=["System_Id","System_Letter","Connector_Type_Calibration","Connector_Type_Measurement",
              "Measurement_Type","Measurement_Date","Measurement_Time","Program_Used","Program_Revision","Operator",
              "Calibration_Name","Calibration_Date","Port_Used","Number_Connects","Number_Repeats","Nbs",
              "Number_Frequencies","Start_Frequency",
              "Device_Description","Device_Id"]
        self.metadata={}
        for index,key in enumerate(keys):
            self.metadata[key]=self.header[index].rstrip().lstrip()
    def show(self):
        fig, axes = plt.subplots(nrows=3, ncols=2)
        ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat
        ax0.plot(self.get_column('Frequency'),self.get_column('magS11'),'k-o')
        ax0.set_title('Magnitude S11')
        ax1.plot(self.get_column('Frequency'),self.get_column('argS11'),'ro')
        ax1.set_title('Phase S11')
        ax2.plot(self.get_column('Frequency'),self.get_column('magS21'),'k-o')
        ax2.set_title('Magnitude S21')
        ax3.plot(self.get_column('Frequency'),self.get_column('argS21'),'ro')
        ax3.set_title('Phase S21')
        ax4.plot(self.get_column('Frequency'),self.get_column('magS22'),'k-o')
        ax4.set_title('Magnitude S22')
        ax5.plot(self.get_column('Frequency'),self.get_column('argS22'),'ro')
        ax5.set_title('Phase S22')
        plt.tight_layout()
        plt.show()

class TwoPortNRRawModel(AsciiDataTable):
    """ Class that deals with the TwoPort Raw Files after conversion to Ascii using Ron Ginley's converter.
    These files typically have header information seperated from data by !!
    Header format is:
    Line 1:		Spid$ - identification of type of system used
    Line 2:		Systemletter$ - letter name indicating which system was used
    Line 3:		Conncal$ - connector type from the system calibration
    Line 4:		Connectors$ - connector type used for the measurement
    Line 5:		Meastype$ - type of measurement (basically 1-port, 2-port or power)
    Line 6:		Datea$ - date of measurement
    Line 7:		Timea$ - time of measurement
    Line 8:		Programm$ - name of program used
    Line 9:		Rev$ - program revision
    Line 10:	Opr$ - operator
    Line 11:	Cfile$ - calibration name
    Line 12:	Cdate$ - calibration date
    Line 13:	Sport - identification of which port or direction was used for measurement
    Line 14:	Numconnects ? number of disconnect/reconnect cycles
    Line 15:	Numrepeats ? number of repeat measurements for each connect (usually 1)
    Line 16:	Nbs ? not sure
    Line 17:	Nfreq ? number of frequencies
    Line 18:	Startfreq ? data row pointer for bdat files
    Line 19:	Devicedescript$ - description of device being measured or of test being done
    Line 20:	Devicenum$ - Identifying number for device ? used for file names
    """
    def __init__(self,file_path=None,**options):
        """Initializes the TwoPortRaw class, if a file_path is specified opens an existing file, else creates an
        empty container"""
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'Two_Port_NR_Raw',
                   "general_descriptor": 'Sparameter', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "column_types": ['float','int','int','float','float','float','float',
                                    'float','float','float','float'],
                   "column_descriptions": {"Frequency":"Frequency in GHz",
                                           "Direction":"Direction of connects, may be unused",
                                           "Connect":"Connect number", "magS11":"Linear magnitude for S11",
                                           "argS11":"Phase in degrees for S11",
                                           "magS12":"Linear magnitude for S21",
                                           "argS12":"Phase in degrees for S21",
                                           "magS21":"Linear magnitude for S21",
                                           "argS21":"Phase in degrees for S21",
                                           "magS22":"Linear magnitude for S22",
                                           "argS22":"Phase in degrees for S22"},
                   "header": None,
                   "column_names": ["Frequency","Direction","Connect", "magS11",
                                    "argS11","magS12","argS12","magS21","argS21","magS22","argS22"],
                   "column_names_end_token": "\n", "data": None,
                   'row_formatter_string': "{0:.5f}{delimiter}{1}{delimiter}{2}"
                                           "{delimiter}{3:.4f}{delimiter}{4:.2f}{delimiter}"
                                           "{5:.4f}{delimiter}{6:.2f}{delimiter}"
                                           "{7:.4f}{delimiter}{8:.2f}{delimiter}"
                                           "{9:.4f}{delimiter}{10:.2f}",
                   "data_table_element_separator": None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is not None:
            self.__read_and_fix__(file_path)

        AsciiDataTable.__init__(self,None,**self.options)
        self.path=file_path
        self.structure_metadata()

    def __read_and_fix__(self,file_path=None):
        """Inputs in the raw OnePortRaw file and fixes any problems with delimiters,etc."""
        lines=[]
        in_file=open(file_path,'r')
        for index,line in enumerate(in_file):
            lines.append(line)
            if re.search("!!",line):
                data_begin_line=index+1
        self.lines=lines
        in_file.close()
        parse_options={"row_end_token":'\n',
                       "row_pattern":make_row_match_string(self.options["column_names"]),
                       "column_names":self.options["column_names"],"column_types":self.options["column_types"]}
        data=parse_lines(lines[data_begin_line:],**parse_options)
        self.options["data"]=data
        if CONVERT_S21:
            for row_index,row in enumerate(self.options["data"]):
                db_value_S21=row[7]
                mag_value_S21=10.**(-1*db_value_S21/20.)
                db_value_S12=row[5]
                mag_value_S12=10.**(-1*db_value_S12/20.)
                self.options["data"][row_index][5]=mag_value_S12
                self.options["data"][row_index][7]=mag_value_S21
        self.options["header"]=lines[:data_begin_line-1]
        #print data


    def structure_metadata(self):
        """Returns a dictionary of key,value pairs extracted from the header"""
        keys=["System_Id","System_Letter","Connector_Type_Calibration","Connector_Type_Measurement",
              "Measurement_Type","Measurement_Date","Measurement_Time","Program_Used","Program_Revision","Operator",
              "Calibration_Name","Calibration_Date","Port_Used","Number_Connects","Number_Repeats","Nbs",
              "Number_Frequencies","Start_Frequency",
              "Device_Description","Device_Id"]
        self.metadata={}
        for index,key in enumerate(keys):
            self.metadata[key]=self.header[index].rstrip().lstrip()
    def show(self):
        fig, axes = plt.subplots(nrows=3, ncols=2)
        ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat
        ax0.plot(self.get_column('Frequency'),self.get_column('magS11'),'k-o')
        ax0.set_title('Magnitude S11')
        ax1.plot(self.get_column('Frequency'),self.get_column('argS11'),'ro')
        ax1.set_title('Phase S11')
        ax2.plot(self.get_column('Frequency'),self.get_column('magS12'),'b-o')
        ax3.plot(self.get_column('Frequency'),self.get_column('argS12'),'bo')
        ax2.plot(self.get_column('Frequency'),self.get_column('magS21'),'k-o')
        ax2.set_title('Magnitude S21')
        ax3.plot(self.get_column('Frequency'),self.get_column('argS21'),'ro')
        ax3.set_title('Phase S21')
        ax4.plot(self.get_column('Frequency'),self.get_column('magS22'),'k-o')
        ax4.set_title('Magnitude S22')
        ax5.plot(self.get_column('Frequency'),self.get_column('argS22'),'ro')
        ax5.set_title('Phase S22')
        plt.tight_layout()
        plt.show()

class PowerRawModel(AsciiDataTable):
    """ Class that deals with the PowerRaw Files after conversion to Ascii using Ron Ginley's converter.
    These files typically have header information seperated from data by !!
    Header format is:
    Line 1:		Spid$ - identification of type of system used
    Line 2:		Systemletter$ - letter name indicating which system was used
    Line 3:		Conncal$ - connector type from the system calibration
    Line 4:		Connectors$ - connector type used for the measurement
    Line 5:		Meastype$ - type of measurement (basically 1-port, 2-port or power)
    Line 6:		Datea$ - date of measurement
    Line 7:		Timea$ - time of measurement
    Line 8:		Programm$ - name of program used
    Line 9:		Rev$ - program revision
    Line 10:	Opr$ - operator
    Line 11:	Cfile$ - calibration name
    Line 12:	Cdate$ - calibration date
    Line 13:	Sport - identification of which port or direction was used for measurement
    Line 14:	Numconnects ? number of disconnect/reconnect cycles
    Line 15:	Numrepeats ? number of repeat measurements for each connect (usually 1)
    Line 16:	Nbs ? not sure
    Line 17:	Nfreq ? number of frequencies
    Line 18:	Startfreq ? data row pointer for bdat files
    Line 19:	Devicedescript$ - description of device being measured or of test being done
    Line 20:	Devicenum$ - Identifying number for device ? used for file names
    """
    def __init__(self,file_path=None,**options):
        """Initializes the PowerRaw class, if a file_path is specified opens an existing file, else creates an
        empty container"""
        defaults= {"data_delimiter": ",", "column_names_delimiter": ",", "specific_descriptor": 'Raw',
                   "general_descriptor": 'Power', "extension": 'txt', "comment_begin": "#", "comment_end": "\n",
                   "column_types": ['float','int','int','float','float','float','float'],
                   "column_descriptions": {"Frequency":"Frequency in GHz",
                                           "Direction":"Direction of connects, may be unused",
                                           "Connect":"Connect number", "magS11":"Linear magnitude for S11",
                                           "argS11":"Phase in degrees for S11",
                                           "Efficiency":"Effective Efficiency",
                                           "Calibration_Factor":"Effective efficiency "
                                                                "modified by reflection coefficient"},
                   "header": None,
                   "column_names": ["Frequency","Direction","Connect", "magS11",
                                    "argS11","Efficiency","Calibration_Factor"],
                   "column_names_end_token": "\n", "data": None,
                   'row_formatter_string': "{0:.5g}{delimiter}{1}{delimiter}{2}"
                                           "{delimiter}{3:.5g}{delimiter}{4:.3f}{delimiter}"
                                           "{5:.5g}{delimiter}{6:.5g}",
                   "data_table_element_separator": None}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is not None:
            self.__read_and_fix__(file_path)

        AsciiDataTable.__init__(self,None,**self.options)
        self.path=file_path
        self.structure_metadata()

    def __read_and_fix__(self,file_path=None):
        """Inputs in the PowerRaw file and fixes any problems with delimiters,etc."""
        lines=[]
        in_file=open(file_path,'r')
        for index,line in enumerate(in_file):
            lines.append(line)
            if re.search("!!",line):
                data_begin_line=index+1
        self.lines=lines
        in_file.close()
        parse_options={"row_end_token":'\n',
                       "row_pattern":make_row_match_string(self.options["column_names"],delimiter_pattern='[\s|(),]+'),
                       "column_names":self.options["column_names"],"column_types":self.options["column_types"]}
        data=parse_lines(lines[data_begin_line:],**parse_options)
        self.options["data"]=data
        self.options["header"]=lines[:data_begin_line-1]
        #print data


    def structure_metadata(self):
        """Returns a dictionary of key,value pairs extracted from the header"""
        keys=["System_Id","System_Letter","Connector_Type_Calibration","Connector_Type_Measurement",
              "Measurement_Type","Measurement_Date","Measurement_Time","Program_Used","Program_Revision","Operator",
              "Calibration_Name","Calibration_Date","Port_Used","Number_Connects","Number_Repeats","Nbs",
              "Number_Frequencies","Start_Frequency",
              "Device_Description","Device_Id"]
        self.metadata={}
        for index,key in enumerate(keys):
            self.metadata[key]=self.header[index].rstrip().lstrip()

class TwoPortCalrepModel():
    """TwoPortCalrepModel is a model that holds data output by analyzing several datafiles using the HPBasic program
    Calrep. The data is stored in 3 tables: a S11 table, a S21 table and a S22 table. The data is in linear
    magnitude and angle in degrees. There are 2 types of files, one is a single file with .asc extension
    and 3 files with .txt extension"""

    def __init__(self,file_path=None,**options):
        """Intializes the TwoPortCalrepModel class, if a file path is specified it opens and reads the file"""
        defaults= {"specific_descriptor": 'Two_Port_Calrep'}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        self.metadata={}
        if file_path is None:
            pass
        elif re.match('asc',file_path.split(".")[-1],re.IGNORECASE):
            self.table_names=['header','S11','S22','S21']
            self.row_pattern=make_row_match_string(ONE_PORT_COLUMN_NAMES)
            self.path=file_path
            self.__read_and_fix__()
            self.metadata["Device_Id"]=self.joined_table.header[0].rstrip().lstrip()
            self.metadata["Analysis_Date"]=self.joined_table.header[1].rstrip().lstrip()

        elif re.match('txt',file_path.split(".")[-1],re.IGNORECASE) or type(file_path) is ListType:
            self.table_names=['S11','S22','S21']
            if type(file_path) is ListType:
                self.file_names=file_path
                self.tables=[]
                for index,table in enumerate(self.table_names):
                    if index==2:
                        #fixes a problem with the c tables, extra comma at the end
                        options={"row_end_token":',\n'}
                        self.tables.append(OnePortCalrepModel(self.file_names[index],**options))
                        self.tables[2].options["row_end_token"]=None
                    else:
                        self.tables.append(OnePortCalrepModel(self.file_names[index]))
            else:
                try:
                    root_name_pattern=re.compile('(?P<root_name>\w+)[abc].txt',re.IGNORECASE)
                    root_name_match=re.search(root_name_pattern,file_path)
                    root_name=root_name_match.groupdict()["root_name"]
                    directory=os.path.dirname(os.path.realpath(file_path))
                    self.file_names=[os.path.join(directory,root_name+end) for end in ['a.txt','b.txt','c.txt']]
                    self.tables=[]
                    for index,table in enumerate(self.table_names):
                        if index==2:
                            #fixes a problem with the c tables, extra comma at the end
                            options={"row_end_token":',\n'}
                            self.tables.append(OnePortCalrepModel(self.file_names[index],**options))
                            self.tables[2].options["row_end_token"]=None
                        else:
                            self.tables.append(OnePortCalrepModel(self.file_names[index]))

                except:
                    print("Could not import {0} please check that the a,b,c "
                          "tables are all in the same directory".format(file_path))
                    raise
            for index,table in enumerate(self.tables):
                column_names=[]
                for column_number,column in enumerate(table.column_names):
                    if column is not "Frequency":
                        column_names.append(column+self.table_names[index])
                    else:
                        column_names.append(column)
                #print column_names
                table.column_names=column_names
            if CONVERT_S21:
                for row_number,row in enumerate(self.tables[2].data):
                    new_S21=self.tables[2].data[row_number][1]
                    new_S21=10.**(-1*new_S21/20.)
                    new_value=[self.tables[2].data[row_number][i] for i in range(2,6)]
                    new_value=map(lambda x:abs((1/np.log10(np.e))*new_S21*x/20.),new_value)
                    self.tables[2].data[row_number][1]=new_S21
                    for i in range(2,6):
                        self.tables[2].data[row_number][i]=new_value[i-2]
            for key,value in self.options.iteritems():
                self.tables[0].options[key]=value
            self.joined_table=ascii_data_table_join("Frequency",self.tables[0],self.tables[2])
            self.joined_table=ascii_data_table_join("Frequency",self.joined_table,self.tables[1])

    def __read_and_fix__(self):
        in_file=open(self.path,'r')
        self.lines=[]
        table_locators=["Table 1","Table 2","Table 3"]
        begin_lines=[]
        for index,line in enumerate(in_file):
            self.lines.append(line)
            for table in table_locators:
                if re.search(table,line,re.IGNORECASE):
                    begin_lines.append(index)
        in_file.close()
        self.table_line_numbers=[]
        for index,begin_line in enumerate(begin_lines):
            if index == 0:
                header_begin_line=0
                header_end_line=begin_line-2
                table_1_begin_line=begin_line+3
                table_1_end_line=begin_lines[index+1]#-1
                self.table_line_numbers.append([header_begin_line,header_end_line])
                self.table_line_numbers.append([table_1_begin_line,table_1_end_line])

            elif index>0 and index<(len(begin_lines)-1):
                table_begin_line=begin_line+3
                table_end_line=begin_lines[index+1]#-1
                self.table_line_numbers.append([table_begin_line,table_end_line])

            elif index==(len(begin_lines)-1):
                table_begin_line=begin_line+3
                table_end_line=None
                self.table_line_numbers.append([table_begin_line,table_end_line])
        self.tables=[]
        for index,name in enumerate(self.table_names):
            self.table_lines=self.lines[self.table_line_numbers[index][0]:self.table_line_numbers[index][1]]
            self.tables.append(self.table_lines)
        for index,table in enumerate(self.table_names):
            if index==0:
                # by using parse_lines we get a list_list of strings instead of list_string
                # we can just remove end lines
                self.tables[index]=strip_all_line_tokens(self.tables[index],begin_token=None,end_token='\n')
            else:
                column_types=['float' for i in range(len(ONE_PORT_COLUMN_NAMES))]
                options={"row_pattern":self.row_pattern,"column_names":ONE_PORT_COLUMN_NAMES,"output":"list_list"}
                options["column_types"]=column_types
                self.tables[index]=parse_lines(self.tables[index],**options)

        # need to put S21 mag into linear magnitude
        if CONVERT_S21:
            for row_number,row in enumerate(self.tables[3]):
                new_S21=self.tables[3][row_number][1]
                new_S21=10.**(-1*new_S21/20.)
                new_value=[self.tables[3][row_number][i] for i in range(2,6)]
                new_value=map(lambda x:abs((1/np.log10(np.e))*new_S21*x/20),new_value)
                self.tables[3][row_number][1]=new_S21
                for i in range(2,6):
                    self.tables[3][row_number][i]=new_value[i-2]

        for index,table in enumerate(self.tables):
            #print("{0} is {1}".format("index",index))
            if index==0:
                pass
            else:
                table_options={"data":self.tables[index]}
                self.tables[index]=OnePortCalrepModel(None,**table_options)
                #print("{0} is {1}".format("self.tables[index].column_names",self.tables[index].column_names))
                column_names=[]
                for column_number,column in enumerate(self.tables[index].column_names):
                    if column is not "Frequency":
                        #print("{0} is {1}".format("self.table_names[index]",self.table_names[index]))
                        #print("{0} is {1}".format("column",column))
                        column_names.append(column+self.table_names[:][index])
                    else:
                        column_names.append(column)
                self.tables[index].column_names=column_names

        self.tables[1].header=self.tables[0]
        for key,value in self.options.iteritems():
            self.tables[1].options[key]=value
        self.joined_table=ascii_data_table_join("Frequency",self.tables[1],self.tables[3])
        self.joined_table=ascii_data_table_join("Frequency",self.joined_table,self.tables[2])

    def __str__(self):
        return self.joined_table.build_string()

    def show(self):
        fig, axes = plt.subplots(nrows=3, ncols=2)
        ax0, ax1, ax2, ax3, ax4, ax5 = axes.flat
        ax0.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('magS11'),
             yerr=self.joined_table.get_column('uMgS11'),fmt='k-o')
        ax0.set_title('Magnitude S11')
        ax1.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('argS11'),
             yerr=self.joined_table.get_column('uAgS11'),fmt='ro')
        ax1.set_title('Phase S11')
        ax2.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('magS21'),
             yerr=self.joined_table.get_column('uMgS21'),fmt='k-o')
        ax2.set_title('Magnitude S21')
        ax3.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('argS21'),
             yerr=self.joined_table.get_column('uAgS21'),fmt='ro')
        ax3.set_title('Phase S21')
        ax4.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('magS22'),
             yerr=self.joined_table.get_column('uMgS22'),fmt='k-o')
        ax4.set_title('Magnitude S22')
        ax5.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('argS22'),
             yerr=self.joined_table.get_column('uAgS22'),fmt='ro')
        ax5.set_title('Phase S22')
        plt.tight_layout()
        plt.show()

class PowerCalrepModel():
    """PowerCalrep is a model that holds data output by analyzing several datafiles using the HPBasic program
    Calrep. The data is stored in 2 tables: a S11 table, and a power table. The data is in linear
    magnitude and angle in degrees. There are 2 types of files, one is a single file with .asc extension
    and 2 files with .txt extension"""

    def __init__(self,file_path=None,**options):
        """Intializes the PowerCalrep class, if a file path is specified it opens and reads the file"""
        defaults= {}
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        self.metadata={}
        if file_path is None:
            pass
        elif re.match('asc',file_path.split(".")[-1],re.IGNORECASE):
            self.table_names=['header','S11','Efficiency']
            self.row_pattern=make_row_match_string(ONE_PORT_COLUMN_NAMES)
            self.power_4term_row_pattern=make_row_match_string(POWER_4TERM_COLUMN_NAMES)
            self.power_3term_row_pattern=make_row_match_string(POWER_3TERM_COLUMN_NAMES)
            self.path=file_path
            self.__read_and_fix__()
            self.metadata["Device_Id"]=self.joined_table.header[0].rstrip().lstrip()
            self.metadata["Analysis_Date"]=self.joined_table.header[1].rstrip().lstrip()

        elif re.match('txt',file_path.split(".")[-1],re.IGNORECASE) or type(file_path) is ListType:
            self.table_names=['S11','Efficiency']
            if type(file_path) is ListType:
                self.file_names=file_path
                self.tables=[]
                for index,table in enumerate(self.table_names):
                    if index==0:
                        self.tables.append(PowerModel(self.file_names[index]))
                    elif index==1:
                        self.tables.append(OnePortCalrepModel(self.file_names[index]))
            else:
                try:
                    root_name_pattern=re.compile('(?P<root_name>\w+)[abc].txt',re.IGNORECASE)
                    root_name_match=re.search(root_name_pattern,file_path)
                    root_name=root_name_match.groupdict()["root_name"]
                    directory=os.path.dirname(os.path.realpath(file_path))
                    self.file_names=[os.path.join(directory,root_name+end) for end in ['a.txt','b.txt']]
                    self.tables=[]
                    for index,table in enumerate(self.table_names):
                        if index==0:
                            self.tables.append(OnePortCalrepModel(self.file_names[index]))
                        elif index==1:
                            self.tables.append(PowerModel(self.file_names[index]))
                except:
                    print("Could not import {0} please check that the a,b "
                          "tables are all in the same directory".format(file_path))
                    raise

            # for index,table in enumerate(self.tables):
            #     for column_number,column in enumerate(table.column_names):
            #         if column is not "Frequency":
            #             table.column_names[column_number]=self.table_names[index]+"_"+column

            self.joined_table=ascii_data_table_join("Frequency",self.tables[0],self.tables[1])
            #print self.joined_table

    def __read_and_fix__(self):
        in_file=open(self.path,'r')
        self.lines=[]
        table_locators=["Table 1","Table 2"]
        begin_lines=[]
        for index,line in enumerate(in_file):
            self.lines.append(line)
            for table in table_locators:
                if re.search(table,line,re.IGNORECASE):
                    begin_lines.append(index)
        in_file.close()
        self.table_line_numbers=[]
        for index,begin_line in enumerate(begin_lines):
            if index == 0:
                header_begin_line=0
                header_end_line=begin_line-1
                table_1_begin_line=begin_line+1
                table_1_end_line=begin_lines[index+1]
                self.table_line_numbers.append([header_begin_line,header_end_line])
                self.table_line_numbers.append([table_1_begin_line,table_1_end_line])
            elif index>0 and index<(len(begin_lines)-1):
                table_begin_line=begin_line+2
                print("{0} is {1}".format('begin_line',begin_line))
                table_end_line=begin_lines[index+1]
                self.table_line_numbers.append([table_begin_line,table_end_line])
            elif index==(len(begin_lines)-1):
                table_begin_line=begin_line+1
                table_end_line=None
                self.table_line_numbers.append([table_begin_line,table_end_line])
        self.tables=[]
        for index,name in enumerate(self.table_names):
            self.table_lines=self.lines[self.table_line_numbers[index][0]:self.table_line_numbers[index][1]]
            self.tables.append(self.table_lines)
        for index,table in enumerate(self.table_names):
            if index==0:
                # by using parse_lines we get a list_list of strings instead of list_string
                # we can just remove end lines
                self.tables[index]=strip_all_line_tokens(self.tables[index],begin_token=None,end_token='\n')
            elif index==1:
                column_types=['float' for i in range(len(ONE_PORT_COLUMN_NAMES))]
                options={"row_pattern":self.row_pattern,"column_names":ONE_PORT_COLUMN_NAMES,"output":"list_list"}
                options["column_types"]=column_types
                self.tables[index]=parse_lines(self.tables[index],**options)
                table_options={"data":self.tables[index]}
                self.tables[index]=OnePortCalrepModel(None,**table_options)
            elif index==2:
                # Here we need to test for the type of power model (how many columns)
                test_row=self.tables[index][2]
                if re.match(self.power_3term_row_pattern,test_row) and re.match(self.power_4term_row_pattern,test_row):
                    self.options["column_names"]=POWER_4TERM_COLUMN_NAMES
                    self.power_row_pattern=self.power_4term_row_pattern
                elif re.match(self.power_3term_row_pattern,test_row):
                    self.options["column_names"]=POWER_3TERM_COLUMN_NAMES
                    self.power_row_pattern=self.power_3term_row_pattern
                else:
                    raise ValueError("Power Table Does Not Conform")
                column_types=['float' for i in range(len(self.options["column_names"]))]
                table_options={"row_pattern":self.power_row_pattern,"column_names":self.options["column_names"],
                         "output":"list_list"}
                table_options["column_types"]=column_types
                self.tables[index]=parse_lines(self.tables[index],**table_options)
                table_options["data"]=self.tables[index]
                self.tables[index]=PowerModel(None,**table_options)

        # for table in self.tables:
        #     print table
        #print("Length of table 1 is {0}, Length of table 2 is {1}".format(len(self.tables[1].data),len(self.tables[2].data)))
        self.tables[1].header=self.tables[0]
        self.joined_table=ascii_data_table_join("Frequency",self.tables[1],self.tables[2])

    def __str__(self):
        return self.joined_table.build_string()

    def show(self):
        fig, axes = plt.subplots(nrows=2, ncols=2)
        ax0, ax1, ax2, ax3 = axes.flat
        ax0.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('mag'),
                     yerr=self.joined_table.get_column('uMg'),fmt='k--')
        ax0.set_title('Magnitude S11')
        ax1.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('arg'),
                     yerr=self.joined_table.get_column('uAg'),fmt='ro')
        ax1.set_title('Phase S11')
        ax2.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('Efficiency'),
                     yerr=self.joined_table.get_column('uEe'),fmt='k--')
        ax2.set_title('Effective Efficiency')
        ax3.errorbar(self.joined_table.get_column('Frequency'),self.joined_table.get_column('Calibration_Factor'),
                     yerr=self.joined_table.get_column('uCe'),fmt='ro')
        ax3.set_title('Calibration Factor')
        plt.tight_layout()
        plt.show()


class JBSparameter(AsciiDataTable):
    """JBSparameter is a class that holds data taken and stored using Jim Booth's two port format.
     """

    def __init__(self,file_path=None,**options):
        """Initializes the JBSparameter class. JB Sparameter data is very close to s2p, but has # as a comment
         begin token, and space as a data delimiter. The first line has structured metadata that usually includes
         date and IFBW"""
        defaults={"header_begin_line":0,"data_end_line":None,"column_names_delimiter":' ',
                "column_names_begin_token":'#',"column_names_end_token":'\n',"data_table_element_separator":None,
                 "data_delimiter":' ',"comment_begin":"#",
                 "comment_end":"\n","row_end_token":'\n',"column_types":['float' for i in range(9)],
                 "column_descriptions":["Frequency in Hz",
                                        "Real part of S11",
                                        "Imaginary part of S11",
                                        "Real part of S21",
                                        "Imaginary part of S21",
                                        "Real part of S12",
                                        "Imaginary part of S12",
                                        "Real part of S22",
                                        "Imaginary part of S22"]}
        rfs=""
        for i in range(9):
            if i==8:
                rfs=rfs+"{%s:.6g}"%(str(i))
            else:
                rfs=rfs+"{%s:.6g}{delimiter}"%(str(i))
        options["row_formatter_string"]=rfs
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)

        if file_path is not None:
            column_name_line=0
            in_file=open(file_path,'r')
            for line in in_file:
                if line[0] is '#':
                    column_name_line+=1
            in_file.close()
            self.options["header_end_line"]=column_name_line-1
            self.options["column_names_begin_line"]=column_name_line-1
            self.options["column_names_end_line"]=column_name_line
            self.options["data_begin_line"]=column_name_line
            self.path=file_path
            AsciiDataTable.__init__(self,file_path,**self.options)
        else:
            AsciiDataTable.__init__(self,file_path,**self.options)
    def get_frequency_units(self):
        """Returns the frequency units by looking at the 0 index element of column names"""
        pattern='freq\((?P<Frequency_Units>\w+)\)'
        match=re.match(pattern,self.column_names[0])
        return match.groupdict()['Frequency_Units']



class TwelveTermErrorModel(AsciiDataTable):
    """TwelveTermErrorModel holds the error coefficients for a twelve term model. The VNA calibration coefficeients
    are presumed to be stored in the following order frequency Edf Esf Erf Exf Elf Etf Edr Esr Err Exr Elr Etr, where
    all coefficients are in Real-Imaginary format. """
    def __init__(self):
        """Intializes the TwelveTermErrorModel """
        pass

class SwitchTermsFR():
    pass
class SwitchTermsPort():
    pass
class NoiseCalRaw():
    pass
class ReverbChamber():
    pass
class RobotData():
    pass

#-----------------------------------------------------------------------------
# Module Scripts
def convert_all_two_ports_script(top_directory=None,output_directory=None):
    """Script reads all file names in all sub directories looking for ones that end in c, and tries to open
    file_name.asc and save it in the output directory"""
    TOP_DIRECTORY=r'C:\Share\ascii.dut'
    # This pattern will find any names that have c in them
    TWO_PORT_PATTERN=re.compile('(?P<two_port_name>\w+)c',re.IGNORECASE)
    # now we test the os.walk function
    # This has a memory leak I am not sure but I suspect it is jupyter's fault
    for root,directory,file_names in os.walk(TOP_DIRECTORY):
        #print file_names
        for file_name in file_names:
            file_name=file_name.split('.')[0]
            match=re.search(TWO_PORT_PATTERN,file_name)
            try:
                if match:
                    asc_file_name=match.groupdict()["two_port_name"]+".asc"
                    print asc_file_name
                    if asc_file_name in ['de.asc','00.asc','dir.asc','IL.asc',"L2.asc","L1.asc"]:raise
                    converted_file=TwoPortCalrepModel(os.path.join(root,asc_file_name))
                    #print converted_file.joined_table.header
                    del converted_file
            except:
                pass

def test_OnePortCalrepModel(file_path_1='700437.txt',file_path_2="700437.asc"):
    os.chdir(TESTS_DIRECTORY)
    print(" Import of {0} results in:".format(file_path_1))
    new_table_1=OnePortCalrepModel(file_path=file_path_1)
    print new_table_1
    print("-"*80)
    print("\n")
    print(" Import of {0} results in:".format(file_path_2))
    new_table_2=OnePortCalrepModel(file_path=file_path_2)
    print new_table_2
    print("{0} results in {1}:".format('new_table_1.get_column("Frequency")',new_table_1.get_column("Frequency")))
    print new_table_1.get_options()
    print new_table_1.data[-1]
    new_table_1.show()

def test_OnePortCalrepModel_Ctable(file_path_1='700437.txt'):
    """Tests the OnePortCalrepModel on ctables from 2 port """
    os.chdir(TESTS_DIRECTORY)
    print(" Import of {0} results in:".format(file_path_1))
    new_table_1=OnePortCalrepModel(file_path=file_path_1,**{"row_end_token":",\n"})
    print new_table_1
    print("-"*80)
    print("\n")
    new_table_1.show()


def test_OnePortRawModel(file_path='OnePortRawTestFile.txt'):
    os.chdir(TESTS_DIRECTORY)
    print(" Import of {0} results in:".format(file_path))
    new_table_1=OnePortRawModel(file_path=file_path)
    print new_table_1
    print("-"*80)
    print("{0} results in {1}:".format('new_table_1.get_column("Frequency")',new_table_1.get_column("Frequency")))
    print new_table_1.get_options()
    print new_table_1.metadata
    print new_table_1.column_names
    print('index' in new_table_1.column_names )
    new_table_1.show()

def test_TwoPortRawModel(file_path='TestFileTwoPortRaw.txt'):
    os.chdir(TESTS_DIRECTORY)
    print(" Import of {0} results in:".format(file_path))
    new_table_1=TwoPortRawModel(file_path=file_path)
    print new_table_1
    new_table_1.show()

def test_PowerRawModel(file_path='TestFilePowerRaw.txt'):
    os.chdir(TESTS_DIRECTORY)
    print(" Import of {0} results in:".format(file_path))
    new_table_1=PowerRawModel(file_path=file_path)
    print new_table_1
    #new_table_1.show()

def test_JBSparameter(file_path="ftest6_L1_g5_HF_air"):
    """Tests the JBSparameter class"""
    os.chdir(TESTS_DIRECTORY)
    # open an existing file
    new_table=JBSparameter(file_path=file_path)
    print new_table.column_names
    print new_table.get_frequency_units()
    old_prefix=new_table.get_frequency_units().replace('Hz','')
    #new_table.change_unit_prefix(column_selector=0,old_prefix='',new_prefix='G',unit='Hz')
    new_table.change_unit_prefix(column_selector=0,old_prefix=old_prefix,new_prefix='G',unit='Hz')
    print new_table.column_names
    print new_table.get_column(None,0)
    print new_table.get_frequency_units()
    print new_table.get_header_string()

def test_TwoPortCalrepModel(file_name="922729a.txt"):
    """Tests the TwoPortCalrepModel model type"""
    os.chdir(TESTS_DIRECTORY)
    new_two_port=TwoPortCalrepModel(file_name)
    for table in new_two_port.tables:
        print table
    print new_two_port.joined_table
    #new_two_port.joined_table.save()
    new_two_port.joined_table.path='N205RV.txt'
    new_two_port.joined_table.header=None
    new_two_port.joined_table.column_names=None
    #new_two_port.joined_table.save()

def test_PowerCalrepModel(file_name="700083.asc"):
    """Tests the TwoPortCalrepModel model type"""
    os.chdir(TESTS_DIRECTORY)
    new_power=PowerCalrepModel(file_name)
    for table in new_power.tables:
        print table
    print new_power.joined_table
    #print new_power.joined_table.data[-1]
    new_power.show()

def test_sparameter_power_type(file_list=None):
    """Tests the sparameter_power_type function. Each file's type is determined and it is imported using
     the appropriate model"""
    os.chdir(TESTS_DIRECTORY)
    if file_list is None:
        file_list=[r'CTNP11.L36_062399','CTN106.D4_091799','CTN208.A1_011613','700083.ASC',
                   '700437.asc','922729.asc']
    else:
        file_list=file_list
    for file_name in file_list:
        file_type=sparameter_power_type(file_name)
        print(" The model of {0} is {1}".format(file_name,file_type))
        try:
            model=globals()[file_type]
            table=model(file_name)
            print table
        except:
            print("There was an error opening {0}".format(file_name))



#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_OnePortCalrepModel()
    #test_OnePortCalrepModel('700437.asc')
    #test_OnePortCalrepModel_Ctable(file_path_1='922729c.txt')
    #test_OnePortRawModel()
    #test_OnePortRawModel('OnePortRawTestFile_002.txt')
    test_TwoPortRawModel()
    #test_PowerRawModel()
    #test_JBSparameter()
    #test_JBSparameter('QuartzRefExample_L1_g10_HF')
    #test_TwoPortCalrepModel()
    #test_TwoPortCalrepModel('N205RV.asc')
    #test_PowerCalrepModel()
    #test_PowerCalrepModel('700083b.txt')
    #convert_all_two_ports_script()
    #test_sparameter_power_type()