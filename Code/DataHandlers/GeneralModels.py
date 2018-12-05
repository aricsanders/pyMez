#-----------------------------------------------------------------------------
# Name:        GeneralModels
# Purpose:     To create base classes
# Author:      Aric Sanders
# Created:     2/24/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" GeneralModels is a module that contains general data models and functions for handling them. Its key
 class is AsciiDataTable that is an abstracted model of a data table with a header full of metadata, a
 column modeled table (like excel or a csv table) and a footer. Made a change 10/19/2018 to AsciiDataTable
 that now by default saves a .schema file and looks for one to open the table (save_schema=True,
 open_with_schema =True ) Currently it is great for small ~1MB or less files. If it is extremely slow use numpy.loadtxt


Examples
--------
    #!python
    >>from pyMez import *
    >>table=AsciiDataTable(None,data=[[0,1],[1,0]],column_names=["a","b])
    >>print(table)
    >>table.header=["A header for you"]
    >>print(table)


<h3><a href="../../../Examples/Html/AsciiDataTable_Example.html">Data Table Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [numpy](http://www.numpy.org/)
+ [pyMez](https://github.com/aricsanders/pyMez)

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
from types import * # This no longer has StingType, etc
import os
import pickle
import sys
import copy
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Utils.Types import *
except:
    print("The module pyMez.Code.Utils.Types was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.Utils.Alias import *
    METHOD_ALIASES=1
except:
    print("The module pyMez.Code.Utils.Alias was not found")
    METHOD_ALIASES=0
    pass
try:
    from Code.Utils.Names import *
    DEFAULT_FILE_NAME=None
except:
    print("The function auto_name in pyMez.Code.Utils.Names was not found")
    print("Setting Default file name to New_Data_Table.txt")
    DEFAULT_FILE_NAME='New_Data_Table.txt'
    pass
try:
    import numpy as np
except:
    np.ndarray='np.ndarray'
    print("Numpy was not imported")
    pass
#-----------------------------------------------------------------------------
# Module Constants
TESTS_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')
"Directory that holds files generated or used in module testing."
# General Regular Expression For matching a number
NUMBER_MATCH_STRING=r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
"Regular expression that matches a number of any format."

#-----------------------------------------------------------------------------
# Module Functions

def print_comparison(var_1,var_2):
    """If var_1==var_2 prints True, else Prints false and a string representation of the 2 vars"""
    print((var_1==var_2))
    if var_1!=var_2:
        print("The value of variable 1 is :")
        print(var_1)
        print(("-"*80))
        print("The value of variable 2 is :")
        print(var_2)
        print(("-"*80))

def check_arg_type(arg,arg_type):
    "Checks argument and prints out a statement if arg is not type"
    if isinstance(arg, arg_type):
        return
    else:
        print(("{0} was not {1} but {2}".format(arg,arg_type,type(arg))))

def string_list_collapse(list_of_strings,string_delimiter='\n'):
    """ Makes a list of strings a single string"""
    check_arg_type(list_of_strings,ListType)
    if list_of_strings is None:
        return
    if string_delimiter is None:
        string_delimiter=""
    out_string=''
    for index,item in enumerate(list_of_strings):
        if index is len(list_of_strings)-1:
            out_string=out_string+item
        else:
            out_string=out_string+item+string_delimiter
    return out_string
def list_to_string(row_list,data_delimiter=None,row_formatter_string=None,begin=None,end=None):
    """Given a list of values returns a string, if row_formatter is specifed
     it uses it as a template, else uses data delimiter. Inserts data_delimiter between each list element. An optional
    begin and end wrap the resultant string. (i.e ['1','2','3']-> 'begin+'1'+','+'2'+','+'3'+'end') end defaults
    to \n to have nothing at the end use ''
    """
    check_arg_type(row_list,ListType)
    if data_delimiter is None:
        data_delimiter=','
    string_out=""
    if row_formatter_string is None:
        for index,item in enumerate(row_list):
            if index is len(row_list)-1:
                string_out=string_out+str(item)
            else:
                string_out=string_out+str(item)+data_delimiter
    else:
        string_out=row_formatter_string.format(*row_list,delimiter=data_delimiter)
    if end is None:
        end="\n"
    if begin is None:
        begin=""
    return begin+string_out+end

def list_list_to_string(list_lists,data_delimiter=None,row_formatter_string=None,line_begin=None,line_end=None):
    """Repeatedly calls list to string on each element of a list and string adds the result
    . ie coverts a list of lists to a string. If line end is None the value defaults to "\n", for no seperator use ''
    """
    if line_end is None:
        line_end="\n"
    check_arg_type(list_lists,ListType)
    string_out=""
    for index,row in enumerate(list_lists):
        if index==len(list_lists)-1:
            if line_end is "\n":
                last_end=""
            else:
                last_end=re.sub("\n","",line_end,count=1)
            string_out=string_out+list_to_string(row,data_delimiter=data_delimiter,
                                             row_formatter_string=row_formatter_string,
                                             begin=line_begin,end=last_end)
        else:
            string_out=string_out+list_to_string(row,data_delimiter=data_delimiter,
                                             row_formatter_string=row_formatter_string,
                                             begin=line_begin,end=line_end)
    return string_out

def line_comment_string(comment,comment_begin=None,comment_end=None):
    "Creates a comment optionally wrapped with comment_begin and comment_end, meant for a single string comment "
    check_arg_type(comment,StringType)
    string_out=""
    if comment_begin is None:
        if comment_end is None:
            string_out=comment
        else:
            string_out=comment+comment_end
    else:
        if comment_end is None:
            string_out=comment_begin+comment
        else:
            string_out=comment_begin+comment+comment_end
    return string_out

def line_list_comment_string(comment_list,comment_begin=None,comment_end=None,block=False):
    """Creates a string with each line wrapped in comment_begin and comment_end, by repeatedly calling
    line_comment_string,
    or the full string wrapped with block_comment_begin and block_comment_end if block is set to True. Meant
    to deal with a list of comment strings"""
    check_arg_type(comment_list,ListType)
    string_out=""
    if block:
        string_out=comment_begin+string_list_collapse(comment_list,string_delimiter='\n')+comment_end
    else:
        for item in comment_list:
            string_out=string_out+line_comment_string(item,comment_begin=comment_begin,comment_end=comment_end)
    return string_out

def ensure_string(input_object,  list_delimiter="",  end_if_list=""):
    """Returns a string given an object. If the object is a string just returns it,
    if it is a list of strings, returns a collapsed version. If is another type of object returns str(object).
      If all else fails it returns an empty string"""
    string_out=""
    try:
        if isinstance(input_object,StringType):
            string_out=input_object
        elif isinstance(input_object,(ListType,np.ndarray)):
            if isinstance(input_object[0],(ListType,np.ndarray)):
                string_out=list_list_to_string(input_object,data_delimiter=list_delimiter,end=end_if_list)
            else:
                string_out=list_to_string(input_object,data_delimiter=list_delimiter,end=end_if_list)
        else:
            string_out=str(input_object)
    except:
        pass
    return string_out

def strip_tokens(string_list,*remove_tokens):
    """Strips all tokens in the list remove_tokens from a list of strings
    Returns the list with less elements if the tokens contained "\n". Now newline characters are returned in the list
    elements. Meant to reverse the action of adding tokens to a list of strings"""
    temp_string=string_list_collapse(string_list,string_delimiter="")
    remove_list=[]
    for token in remove_tokens:
        if token:
            # we can't strip endlines f
            if token=="\n":
                print("Warning \\n is in the remove tokens")
                break
            remove_list.append(token)
            # print remove_list
    try:
        for item in remove_list:
            temp_string=temp_string.replace(item,"")
            #print temp_string
    except:
        print("Strip Tokens Did not work")
        pass
    # spliting using "\n" seems to give an extra empty element at the end always
    new_string_list=temp_string.splitlines()
    # now we add endlines back in for consistency
    for index,line in enumerate(new_string_list):
        new_string_list[index]=line+'\n'
    return new_string_list

def strip_begin_end_tokens(string_list,begin_token=None,end_token=None):
    """Strips out tokens at the begining and ending of a list of strings. Meant to reverse the
    action of "begin_data_token", etc. This does not work with the end_token's because of where the \n is."""
    check_arg_type(string_list,ListType)
    out_list=string_list
    # check the first line to see if it is equal to begin token, if so remove it
    # if any token is None ignore it
    # replace it and leave the line alone otherwize
    if begin_token is None or begin_token is "":
        pass
    else:
        #print("The {0} var is {1}".format('string_list',string_list))
        #print("The {0} var is {1}".format('string_list[0]',string_list[0]))
        #print_comparison(string_list[0],begin_token)
        if string_list[0]==begin_token:
            out_list.pop(0)
        else:
           out_list[0]=out_list[0].replace(begin_token,"")

    if end_token is None or end_token is "":
        pass
    else:
        #print_comparison(string_list[-1],end_token)
        if out_list[-1]==end_token:
            out_list.pop(-1)
        else:
            out_list[-1]=out_list[-1].replace(end_token,"")
    # print("The {0} var is {1}".format('out_list',out_list))
    return out_list




def strip_line_tokens(string,begin_token=None,end_token=None):
    """Strips a begin and end token if present from an inputted string, meant to remove line_comments"""
    check_arg_type(string,StringType)
    string_out=string
    if begin_token is None and end_token is None:
        return string_out
    try:
        match_string=""
        if begin_token is not None:
            match_string=begin_token
        match_string=match_string+"(?P<data>.+)"
        if end_token is not None:
            match_string=match_string+end_token
        match=re.match(match_string,string)
        if match:
            string_out=match.groupdict()['data']
        elif string in ['\n']:
            return ''
    except:
        print(("strip_line_tokens failed to strip {0},{1} from {2}".format(begin_token,end_token,string)))
        pass
    return string_out

def strip_all_line_tokens(string_list,begin_token=None,end_token=None):
    """Strips all line tokens from a list of strings, meant  to reverse the action of line_list_comment_string
    with block=false"""
    check_arg_type(string_list,ListType)
    stripped_list=[]
    for row in string_list:
        check_arg_type(row,StringType)
        stripped_list.append(strip_line_tokens(row,begin_token=begin_token,end_token=end_token))
    return stripped_list

def split_row(row_string,delimiter=None,escape_character=None,strip=True):
    """Splits a row given a delimiter, and ignores any delimiters after an escape character
    returns a list. If the string is unsplit returns a list of length 1"""
    check_arg_type(row_string,StringType)
    if strip:
        row_string=row_string.rstrip().lstrip()
    if delimiter is None:
        row_list=[row_string]
        return row_list
    if escape_character is None:
        row_list=re.split(delimiter,row_string)
    else:
        temp_row_string=row_string.replace(escape_character+delimiter,'TempPlaceHolder')
        temp_row_list=re.split(delimiter,temp_row_string)
        for item in temp_row_list:
            item.replace('TempPlaceHolder',escape_character+delimiter)
        row_list=temp_row_list
    return row_list

def split_all_rows(row_list,delimiter=None,escape_character=None):
    """Splits all rows in a list of rows and returns a 2d list """
    if not isinstance(row_list, ListType):
        print(("Split row argument (%s) was not a list"%str(row_list)))
        return row_list
    out_list=[]
    for row in row_list:
        out_list.append(split_row(row,delimiter=delimiter,escape_character=escape_character))
    return out_list

def convert_row(row_list_strings,column_types=None):
    """Converts a row list of strings to native
    python types using a column types list"""
    if column_types is None:
        column_types=['str' for value in row_list_strings]

    if len(row_list_strings) != len(column_types):
        print(("Convert row could not convert {0} using {1}".format(row_list_strings,column_types)))
        raise TypeConversionError("Convert row could not convert {0} using {1}".format(row_list_strings,column_types))
        #return row_list_strings
    else:
        out_row=row_list_strings
        for index,column_type in enumerate(column_types):
            if re.match('int',column_type,re.IGNORECASE):
                out_row[index]=int(row_list_strings[index])
            elif re.match('float',column_type,re.IGNORECASE):
                out_row[index]=float(row_list_strings[index])
            elif re.match('str|char|object',column_type,re.IGNORECASE):
                #print_comparison(row_list_strings[index],out_row[index])
                out_row[index]=str(row_list_strings[index])
            elif re.match('com',column_type,re.IGNORECASE):
                out_row[index]=complex(row_list_strings[index])
            elif re.match('list',column_type,re.IGNORECASE):
                out_row[index]=list(row_list_strings[index])
            elif re.match('dict',column_type,re.IGNORECASE):
                out_row[index]=dict(row_list_strings[index])
            else:
                out_row[index]=row_list_strings[index]
    return out_row

def convert_all_rows(list_rows,column_types=None):
    "Converts all the rows (list of strings) in a list of rows using column types "
    check_arg_type(list_rows,ListType)
    out_list=[]
    for index,row in enumerate(list_rows):
        out_list.append(convert_row(row,column_types))
    return out_list

def insert_inline_comment(list_of_strings,comment="",line_number=None,string_position=None,begin_token='(*',end_token='*)'):
    "Inserts an inline comment in a list of strings, location is determined by line_number and string_position"
    if line_number is None or string_position is None:
        print("inline comment must have both line number and string position")
        return
    if begin_token is None or end_token is None:
        print("inline comment must have both a begin and end token")
        return
    inline_comment=begin_token+comment+end_token
    #make sure there are no end lines
    inline_comment=inline_comment.replace('\n','')
    if string_position in [-1,'EOL','eol']:
        list_of_strings[line_number]=list_of_strings[line_number]+inline_comment
    else:
        list_of_strings[line_number]=list_of_strings[line_number][:string_position]+inline_comment+list_of_strings[line_number][string_position:]
    return list_of_strings

def collect_inline_comments(list_of_strings,begin_token=None,end_token=None):
    """Reads a list of strings and returns all of the inline comments in a list.
    Output form is ['comment',line_number,string_location] returns None  if there are none or tokens are set to None"""
    if begin_token in [None] and end_token in [None]:
        return None
    match=re.compile('{0}(?P<inline_comments>.*){1}'.format(re.escape(begin_token),re.escape(end_token)))
    inline_comment_list=[]
    for index,line in enumerate(list_of_strings):
        comment_match=re.search(match,line)
        if comment_match:
            inline_comment_list.append([comment_match.group('inline_comments'),index,comment_match.start()])
    if inline_comment_list:
        return inline_comment_list
    else:
        return None

def strip_inline_comments(list_of_strings,begin_token='(*',end_token='*)'):
    "Removes inline comments from a list of strings and returns the list of strings"
    if begin_token in [None] and end_token in [None]:
        return list_of_strings
    match=re.compile('{0}(?P<inline_comments>.+){1}'.format(re.escape(begin_token),re.escape(end_token)))
    out_list=[]
    for index,line in enumerate(list_of_strings):
        out_list.append(re.sub(match,'',line))
    return out_list


def read_schema(file_path, format=None):
    """Reads in a schema and returns it as a python dictionary, the default format is a single string"""
    if format in [None, 'python', 'pickle']:
        try:
            schema = pickle.load(open(file_path, 'rb'))
        except:
            schema_bytes = pickle.load(open(file_path, 'rb'), encoding='bytes')
            schema = {}
            for key, value in schema_bytes.items():
                if isinstance(value, bytes):
                    schema[key.decode()] = value.decode()
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        if isinstance(item, bytes):
                            value[index] = item.decode()

                else:
                    schema[key.decode()] = value
    elif format in ['txt', 'text', '.txt']:
        # Todo fix the other formats
        schema = {}
        in_file = open(file_path, 'r')
        in_lines = []
        for line in in_file:
            in_lines.append(line)
            schema[line.split(":")[0]] = line.split(":")[1].replace("\\n", "\n")
            # in_dictionary=dict(*str(in_dictionary).split(","))
    return schema

def parse_lines(string_list,**options):
    """Default behavior returns a two dimensional list given a list of strings that represent a table."""
    defaults={"row_pattern":None,"column_names":None,
              "column_types":None,"output":'list_list',"delimiter":None,"row_begin_token":None,
              "row_end_token":None,"data_begin_token":None,"data_end_token":None,"escape_character":None}
    parse_options={}
    for key,value in defaults.items():
        parse_options[key]=value
    for key,value in options.items():
        parse_options[key]=value
    out_list=[]
    out_dict_list=[]
    out_list=strip_tokens(string_list,*[parse_options["data_begin_token"],parse_options["data_begin_token"]])
    out_list=strip_all_line_tokens(out_list,begin_token=parse_options["row_begin_token"],
                                  end_token=parse_options["row_end_token"])
    #print("{0} is {1}".format('out_list',out_list))
    try:
        if parse_options["row_pattern"]:
            parsed_out_list=[]
            for line in out_list:
                match=re.match(parse_options["row_pattern"],line)
                if parse_options["column_names"]and match:
                    out_row_dict=match.groupdict()
                    out_dict_list.append(out_row_dict)
                    out_row=[]
                    for column_name in parse_options["column_names"]:
                        out_row.append(out_row_dict[column_name])
                    #print("{0} is {1}".format('out_row',out_row))
                    parsed_out_list.append(out_row)
            out_list=parsed_out_list
        else:
            out_list=split_all_rows(out_list,delimiter=parse_options["delimiter"],
                                     escape_character=parse_options["escape_character"])
        if parse_options["column_types"]:
            out_list=convert_all_rows(out_list,parse_options["column_types"])
        if out_dict_list == [] and parse_options["column_names"] is not None:
            for row in out_list:
                out_row_dict={column_name:row[index] for index,column_name in parse_options["column_names"]}
    except:
        print("Could not parse table")
        raise
    if parse_options["output"] in ['list_list']:
        return out_list
    elif parse_options["output"] in ['dict_list']:
        return out_dict_list
    elif parse_options["output"] in ['numpy']:
        return np.array(out_list)

    elif parse_options["output"] in ['pandas']:
        # Todo: Add the conversion to pandas
        return out_list

def ascii_data_table_join(column_selector,table_1,table_2):
    """Given a column selector (name or zero based index) and
    two tables a data_table with extra columns is returned. The options from table 1 are inherited
    headers and footers are added, if the tables have a different number of rows problems may occur"""
    if len(table_1.data) != len(table_2.data):
        raise DataDimensionError('The dim {0} is not equal to {1}'.format(len(table_1.data),len(table_2.data)))
    if table_1.header is None and table_2.header is None:
        header=None
    elif table_1.header is None:
        header=table_2.header[:]
    elif table_2.header is None:
        header=table_1.header[:]
    elif table_1.header==table_2.header:
        header=table_1.header
    else:
        header=[]
        for line in table_1.header:
            header.append(line)
        for line in table_2.header:
            header.append(line)

    if table_1.footer is None and table_2.footer is None:
        footer=None
    elif table_1.footer is None:
        footer=table_2.footer[:]
    elif table_2.header is None:
        footer=table_1.footer[:]
    elif table_1.footer==table_2.footer:
        footer=table_2.footer[:]
    else:
        footer=[]
        for line in table_1.footer:
            footer.append(line)
        for line in table_2.footer:
            footer.append(line)

    if column_selector in table_2.column_names:
        column_selector_2=table_2.column_names.index(column_selector)

    options=table_1.options.copy()
    new_table=AsciiDataTable(None,**options)
    new_table.data=table_1.data[:]
    new_table.column_names=table_1.column_names[:]
    if header is None:
        new_table.header=None
    else:
        new_table.header=header[:]
    if footer is None:
        new_table.footer=None
    else:
        new_table.footer=footer[:]
    #Todo: make this work for tables without column_names
    for index,column in enumerate(table_2.column_names):
        if column == table_2.column_names[column_selector_2]:
            pass
        else:
            if table_2.options["column_types"] is None:
                column_type=None
            else:
                if isinstance(table_2.options["column_types"], DictionaryType):
                    column_type=table_2.options["column_types"][column]
                elif isinstance(table_2.options["column_types"], ListType):
                    column_type=table_2.options["column_types"][index]
            column_data=table_2.get_column(column)
            new_table.add_column(column,column_type=column_type,column_data=column_data)

    return new_table

def join_ascii_data_table_list(table_list):
    """Joins a list of any subclass of AsciiDataTable returns a new table of the same type, input
    is assume to be a list of AsciiDataTable objects or any sub class. """
    first=table_list[0]
    joined_table=first.copy()
    for table in table_list[1:]:
        joined_table+table
    return joined_table

def structure_metadata(header_string,metadata_fact_delimiter=";",metadata_key_value_delimiter="=",comment_character="#"):
    """Strucutre Metadata returns a metadata string and returns a metadata dictionary"""
    string_list=re.split(metadata_fact_delimiter+'|\n',header_string.replace(comment_character,''))
    metadata_dictionary={}
    for string in string_list:
        pair=string.split(metadata_key_value_delimiter)
        #print pair
        #print len(pair)
        if len(pair)==2:
            key=pair[0].rstrip().lstrip().replace(".","_")
            value=pair[1].rstrip().lstrip()
            metadata_dictionary[key]=value
    return metadata_dictionary

#-----------------------------------------------------------------------------
# Module Classes
class DataDimensionError(Exception):
    """An error associated with a mismatch in data dimensions"""
    pass
class TypeConversionError(Exception):
    """An error in the conversion of rows with provided types"""
    pass

class AsciiDataTable(object):
    """ An AsciiDatable is a generalized model of a data table with optional header,
    column names,rectangular array of data, and footer """
    def __init__(self,file_path=None,**options):
        " Initializes the AsciiDataTable class "
        # This is a general pattern for adding a lot of options
        defaults={"data_delimiter":",",
                  "column_names_delimiter":",",
                  "specific_descriptor":'Data',
                  "general_descriptor":'Table',
                  "directory":None,
                  "extension":'txt',
                  "comment_begin":None,
                  "comment_end":None,
                  "inline_comment_begin":None,
                  "inline_comment_end":None,
                  "block_comment_begin":None,
                  "block_comment_end":None,
                  "footer_begin_line":None,
                  "footer_end_line":None,
                  "header_begin_line":None,
                  "header_end_line":None,
                  "column_names_begin_line":None,
                  "column_names_end_line":None,
                  "data_begin_line":None,
                  "data_end_line":None,
                  "footer_begin_token":None,
                  "footer_end_token":None,
                  "header_begin_token":None,
                  "header_end_token":None,
                  "column_names_begin_token":None,
                  "column_names_end_token":None,
                  "data_begin_token":None,
                  "data_end_token":None,
                  "metadata_delimiter":None,
                  "metadata_key_value_delimiter":None,
                  "header_line_types":None,
                  "column_types":None,
                  "column_descriptions":None,
                  "column_units":None,
                  "footer_line_types":None,
                  "header":None,
                  "column_names":None,
                  "data":None,
                  "footer":None,
                  "inline_comments":None,
                  "row_begin_token":None,
                  "row_end_token":None,
                  "row_formatter_string":None,
                  "empty_value":None,
                  "escape_character":None,
                  "data_table_element_separator":'\n',
                  "treat_header_as_comment":None,
                  "treat_footer_as_comment":None,
                  "metadata":None,
                  "data_list_dictionary":None,
                  "save_schema":True,
                  "open_with_schema":True,
                  "use_alternative_parser":True,
                  "validate":False,
                  }
        #some of the options have the abiltiy to confilct with each other, so there has to be a
        #built-in way to determine the precedence of each option, for import lines first, then begin and then end
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        self.elements=['header','column_names','data','footer','inline_comments','metadata']
        #Define Method Aliases if they are available
        #unqualified exec is not allowed in function '__init__' because it contains a nested function with free variables
        # This is because __init__ has nested functions
        # if METHOD_ALIASES:
        #     for command in alias(self):
        #         exec(command)
        if file_path is None:
            #create a new data table
            if DEFAULT_FILE_NAME is None:
                self.name=auto_name(self.options["specific_descriptor"],
                                    self.options["general_descriptor"],
                                    self.options["directory"],
                                    self.options["extension"])
                if self.options['directory'] is None:
                    self.path=self.name
                else:
                    self.path=os.path.join(self.options["directory"],self.name)
            if self.options["data_list_dictionary"]:
                column_names=list(self.options["data_list_dictionary"][0].keys())
                self.options["column_names"]=column_names
                self.options["data"]=[[row[key] for key in column_names ] \
                                      for row in self.options["data_list_dictionary"]]
            #Now we see if the table has been defined in the options
            # We should reset the self.options versions to None after this so as to not recreate or we
            # can use it as a cache and add a method reset_table which either redoes the below or reloads the saved file
            for element in self.elements:
                self.__dict__[element]=self.options[element]

            self.initial_state=[self.options["header"],self.options["column_names"],
                                self.options["data"],self.options["footer"],
                                self.options["inline_comments"]]
            #print "I got here {0}".format(self.path)
            for element in self.elements:
                if element not in ["metadata"]:
                    self.options[element]=None

            #if you are validating the model, you have to skip the updating until it hsa been parsed
            try:
                if self.options["validate"]:
                    del self.options["validate"]
                    pass
                else:
                    self.update_model()
            except KeyError:
                self.update_model()


        else:
            # open the file and read it in as lines
            # do we parse it here?
            # once parsed we should end up with the major components
            # if we are given options we should use them, if not try to autodetect them?
            # we can just return an error right now and then have an __autoload__ method
            # we can assume it is in ascii or utf-8
            # set any attribute that has no options to None

            # try to parse schema
            try:
                if self.options["open_with_schema"]:
                    new_options=read_schema(change_extension(file_path,new_extension="schema"))
                    for key,value in new_options.items():
                        self.options[key]=value
            except:
                pass

            self.structure_metadata()
            import_table=[]
            for item in self.elements:
                if len([x for x in list(self.get_options_by_element(item).values()) if None!=x])==0:
                    self.__dict__[item]=None
                    #elements.remove(item)
                elif item not in ['inline_comments','row','metadata','comment']:
                    self.__dict__[item]=[]
                    import_row=[self.options['%s_begin_line'%item],
                                self.options['%s_end_line'%item],
                                self.options['%s_begin_token'%item],
                                self.options['%s_end_token'%item]]
                    import_table.append(import_row)
                elif item in ['inline_comments']:
                    self.inline_comments=self.options['inline_comments']
            file_in=open(file_path,'r')
            # in order to parse the file we need to know line #'s, once we deduce them we use __parse__
            self.lines=[]
            for line in file_in:
                self.lines.append(line)
            file_in.close()
            self.path=file_path
            if self.lines_defined():
                self.__parse__()
            else:
                import_table[0][0]=0
                import_table[-1][1]=None
                # This is to make sure the lines inbetween the data table's elements are accounted for
                if self.options['data_table_element_separator'] is None:
                    inner_element_spacing=0
                else:
                    inner_element_spacing=self.options['data_table_element_separator'].count('\n')-1
                #print import_table
                self.update_import_options(import_table=import_table)
                #self.get_options()
                if self.lines_defined():
                    #print("%s says %s"%('self.lines_defined()',str(self.lines_defined())))
                    self.__parse__()
                row_zero=[import_table[i][0] for i in range(len(import_table))]
                for index,item in enumerate(row_zero):
                    #print import_table
                    #print index,item
                    if index>0:
                        #print("Row Zero Loop Returns index={0}, item={1}".format(index,item))
                        if item is not None:
                            import_table[index-1][1]=item+inner_element_spacing
                            #print import_table
                            self.update_import_options(import_table)
                            #print self.lines_defined()
                if self.lines_defined():
                        self.__parse__()
                else:
                    row_one=[import_table[i][1] for i in range(len(import_table))]
                    for index,item in enumerate(row_one):
                        #print("Row One Loop Returns index={0}, item={1}".format(index,item))
                        if index<(len(row_one)-1):
                            #print((index+1)<len(row_one))
                            #print("Row One Loop Returns index={0}, item={1}".format(index,item))
                            if item is not None:
                                #print import_table
                                import_table[index+1][0]=item-inner_element_spacing
                                self.update_import_options(import_table)
                    if self.lines_defined():
                        self.__parse__()
                    else:
                        row_two=[import_table[i][2] for i in range(len(import_table))]
                        for index,item in enumerate(row_two):
                            if item is not None:
                                import_table[index][0]=self.find_line(item)
                        for index,item in enumerate(row_zero):
                            if index>0:
                                if item is not None:
                                    import_table[index-1][1]=item++inner_element_spacing
                                    self.update_import_options(import_table)
                        if self.lines_defined():
                            self.__parse__()
                        else:
                            row_three=[import_table[i][3] for i in range(len(import_table))]
                            for index,item in enumerate(row_three):
                                if item is not None:
                                    import_table[index][1]=self.find_line(item)
                            for index,item in enumerate(row_one):
                                if index<(len(row_one)-1):
                                    if item is not None:
                                        import_table[index+1][0]=item-inner_element_spacing
                            self.update_import_options(import_table)
                            if self.lines_defined():
                                self.__parse__()
                            else:
                                try:
                                    if not self.options["use_alternative_parser"]:raise
                                    print("No schema was found, trying pandas parser, this may take a little while..")
                                    import pandas
                                    self.pandas_data_frame=pandas.read_csv(file_path,
                                                                           sep=self.options["data_delimiter"])
                                    self.column_names =self. pandas_data_frame.columns.tolist()[:]
                                    self.data = self.pandas_data_frame.as_matrix().tolist()[:]
                                    self.options["column_types"] = [str(x) for x in self.pandas_data_frame.dtypes.tolist()[:]]
                                except:
                                    print("FAILED to import file!")
                                    raise
    def structure_metadata(self):
        """Function that should be overridden by whatever model the datatable has, it only responds with a self.metadata
        attribute in its base state derived from self.options["metadata]"""
        self.metadata=self.options["metadata"]
    def find_line(self,begin_token):
        """Finds the first line that has begin token in it"""
        for index,line in enumerate(self.lines):
            if re.search(begin_token,line,re.IGNORECASE):
                return index

    def update_import_options(self,import_table,verbose=False):
        """Updates the options in the import table"""
        # discovered slight bug 2017-01-18 the variable index is not the right one to have here
        # it should be i from 0 to len(import_table)
        defined_element_index=0
        for index,element in enumerate(['header','column_names','data','footer']):
            if self.__dict__[element] is not None:
                if verbose:
                    print(("The {0} variable is {1}".format('index',index)))
                    print(("The {0} variable is {1}".format('element',element)))
                    print(("The {0} variable is {1}".format('import_table',import_table)))
                [self.options['%s_begin_line'%element],
                                self.options['%s_end_line'%element],
                                self.options['%s_begin_token'%element],
                                self.options['%s_end_token'%element]]=import_table[defined_element_index][:]
                defined_element_index+=1
                #self.get_options_by_element(element)

    def lines_defined(self):
        """If begin_line and end_line for all elements that are None are defined returns True"""
        truth_table=[]
        last_element=""
        output=False
        for index,element in enumerate(self.elements):
            if element not in ['inline_comments','metadata'] and self.__dict__[element] is not None:
                try:
                    last_element=element
                    if not None in [self.options['%s_begin_line'%element],self.options['%s_end_line'%element]]:
                        truth_table.append(True)
                    else:
                         truth_table.append(False)
                except:
                    return False
        #print truth_table
        # The last_line of the last element is fine to be none
        if truth_table[-1] is False:
            if self.options['%s_begin_line'%last_element] is not None:
                truth_table[-1]=True
        if False in truth_table:
            output=False
        else:
            output=True
        #print output
        return output

    def __parse__(self):
        """Parses self.lines into its components once all the relevant begin and end lines have been set. It assumes
         that the self.__dict__[self.element[i]]=None for elements that are not defined"""
        # Collect the inline comments if they are not already defined
        if self.inline_comments is None:
           self.inline_comments=collect_inline_comments(self.lines,begin_token=self.options["inline_comment_begin"],
                                                             end_token=self.options["inline_comment_end"])
        # Strip the inline comments
        self.lines=strip_inline_comments(self.lines,
                                             begin_token=self.options['inline_comment_begin'],
                                             end_token=self.options['inline_comment_end'])
        # Define each major element that are not inline comments by their line numbers
        for index,element in enumerate(self.elements):
            if element not in ['inline_comments','metadata'] and self.__dict__[element] is not None :
                try:
                    if not None in [self.options['%s_begin_line'%element]]:
                        content_list=self.lines[
                                            self.options['%s_begin_line'%element]:self.options['%s_end_line'%element]]
                        self.__dict__[element]=content_list
                        # print("The result of parsing is self.{0} = {1}".format(element,content_list))
                except:
                    raise
        # Remove any defined begin and end tokens
        for index,element in enumerate(self.elements):
            if element not in ["inline_comments","metadata"] and self.__dict__[element] is not None:
                        for index,line in enumerate(self.__dict__[element]):
                            self.__dict__[element][index]=line

                        content_list=strip_tokens(self.__dict__[element],
                                                  *[self.options['%s_begin_token'%element],
                                                    self.options['%s_end_token'%element]])
                        self.__dict__[element]=content_list
                        # print("The result of parsing is self.{0} = {1}".format(element,content_list))
        # parse the header
        if self.header is not None:
            #print("The {0} variable is {1}".format('self.header',self.header))
            remove_tokens=[self.options['block_comment_begin'],self.options['block_comment_end']]
            temp_header=self.header
            if self.options["treat_header_as_comment"] is None or self.options["treat_header_as_comment"]:
                remove_tokens=[self.options["block_comment_begin"],
                                                    self.options["block_comment_end"]]
                if self.options["data_table_element_separator"] is not None and self.options['comment_end'] != None:
                    remove_tokens.append(self.options['comment_end']+self.options["data_table_element_separator"])
                temp_header=strip_tokens(temp_header,
                                                   *remove_tokens)
                temp_header=strip_all_line_tokens(temp_header,
                                                  self.options['comment_begin'],self.options['comment_end'])
            else:
                pass

            #print("The {0} variable is {1}".format('temp_header',temp_header))
            #temp_header=strip_tokens(temp_header,*remove_tokens)
            # print("The {0} variable is {1}".format('temp_header',temp_header))
            for index,line in enumerate(temp_header):
                temp_header[index]=line.replace('\n',"")

            self.header=temp_header
            # print("The {0} variable is {1}".format('self.header',self.header))
        # parse the column_names
        if self.column_names is not None:
            #print("The result of parsing is self.{0} = {1}".format('column_names',self.column_names))
            self.column_names=strip_all_line_tokens(self.column_names,begin_token=self.options['column_names_begin_token'],
                                              end_token=self.options['column_names_end_token'])
            # print("The result of parsing is self.{0} = {1}".format('column_names',self.column_names))
            self.column_names=split_all_rows(self.column_names,delimiter=self.options["column_names_delimiter"],
                                        escape_character=self.options["escape_character"])
            #print("The result of parsing is self.{0} = {1}".format('column_names',self.column_names))
            self.column_names=self.column_names[0]
            for index,line in enumerate(self.column_names):
                self.column_names[index]=line.replace('\n',"")
            # print("The result of parsing is self.{0} = {1}".format('column_names',self.column_names))
        # parse the data
        if self.data is not None:
            self.data=strip_all_line_tokens(self.data,begin_token=self.options["row_begin_token"],
                                            end_token=self.options["row_end_token"])
            #print("The result of parsing is self.{0} = {1}".format('data',self.data))
            self.data=split_all_rows(self.data,delimiter=self.options["data_delimiter"],
                                     escape_character=self.options["escape_character"])
            #print("The result of parsing is self.{0} = {1}".format('data',self.data))
            self.data=convert_all_rows(self.data,self.options["column_types"])
            #print("The result of parsing is self.{0} = {1}".format('data',self.data))
        # parse the footer
        if self.footer is not None:
            #print("The {0} variable is {1}".format('self.footer',self.footer))
            remove_tokens=[self.options['block_comment_begin'],self.options['block_comment_end']]
            temp_footer=self.footer
            if self.options["treat_footer_as_comment"] is None or self.options["treat_footer_as_comment"]:
                temp_footer=strip_tokens(temp_footer,
                                                   *[self.options["block_comment_begin"],
                                                   self.options["block_comment_end"]])
                temp_footer=strip_all_line_tokens(temp_footer,
                                                  self.options['comment_begin'],self.options['comment_end'])
            else:
                pass

            #print("The {0} variable is {1}".format('temp_footer',temp_footer))
            #temp_footer=strip_tokens(temp_footer,*remove_tokens)
            #print("The {0} variable is {1}".format('temp_footer',temp_footer))
            for index,line in enumerate(temp_footer):
                temp_footer[index]=line.replace('\n',"")

            self.footer=temp_footer
            # print("The {0} variable is {1}".format('self.footer',self.footer))


    def get_options_by_element(self,element_name):
        """ returns a dictionary
         of all the options that have to do with element. Element must be header,column_names,data, or footer"""
        keys_regarding_element=[x for x in list(self.options.keys()) if re.search(element_name,str(x),re.IGNORECASE)]
        out_dictionary={key:self.options[key] for key in keys_regarding_element}
        #print out_dictionary
        return out_dictionary

    def __str__(self):
        "Controls the str output of AsciiDataTable"
        self.string=self.build_string()
        return self.string

    def update_index(self):
        """ Updates the index column if it exits, otherwise exits quietly
        """
        if 'index' not in self.column_names:
            return
        else:
            try:
                #This should be 0 but just in case
                index_column_number=self.column_names.index('index')
                for i in range(len(self.data)):
                    self.data[i][index_column_number]=i
            except:
                pass

    def update_model(self):
        """Updates the model after a change has been made. If you add anything to the attributes of the model,
        or change this updates the values. If the model has an index column it will make sure the numbers are correct.
        In addition, it will update the options dictionary to reflect added rows, changes in deliminators etc.  """
        if self.column_names is not None and 'index' in self.column_names:
           self.update_index()
        #make sure there are no "\n" characters in the element lists (if so replace them with "") for data this is
        # done on import
        list_types=["header","column_names","footer"]
        for element in list_types:
            if self.__dict__[element] is not None:
                for index,item in enumerate(self.__dict__[element]):
                    if isinstance(self.__dict__[element][index], StringType):
                        self.__dict__[element][index]=item.replace("\n","")
        self.update_column_names()
        if self.data is not None:
            self.data=convert_all_rows(self.data,self.options["column_types"])
        self.string=self.build_string()
        self.lines=self.string.splitlines()

    def update_column_names(self):
        """Update column names adds the value x# for any column that exists in self.data that is not named"""
        if self.data is None:
            return
        elif isinstance(self.column_names, StringType):
            self.column_names=split_row(self.column_names,self.options["column_names_delimiter"])
        elif self.column_names is None:
            column_names=[]
            for index,column in enumerate(self.data[0]):
                column_names.append("x"+str(index))
            self.column_names=column_names
            return
        elif len(self.column_names)==len(self.data[0]):
            return
        elif len(self.column_names) < len(self.data[0]):
            for index in range(len(self.column_names),len(self.data[0])):
                self.column_names.append("x"+str(index))
            return

    def save(self,path=None,**temp_options):
        """" Saves the file, to save in another ascii format specify elements in temp_options, the options
        specified do not permanently change the object's options. If path is supplied it saves the file to that path
        otherwise uses the object's attribute path to define the saving location """
        original_options=self.options
        for key,value in temp_options.items():
            self.options[key]=value
        out_string=self.build_string(**temp_options)
        if path is None:
            path=self.path
        file_out=open(path,'w')
        file_out.write(out_string)
        file_out.close()
        if self.options["save_schema"]:
            self.save_schema(change_extension(path,new_extension="schema"))
        self.options=original_options

    def build_string(self,**temp_options):
        """Builds a string representation of the data table based on self.options, or temp_options.
        Passing temp_options does not permanently change the model"""
        # store the original options to be put back after the string is made
        original_options=self.options
        for key,value in temp_options.items():
            self.options[key]=value
        section_end=0
        next_section_begin=0
        if self.options['data_table_element_separator'] is None:
            inner_element_spacing=0
        else:
            # if header does not end in "\n" and
            inner_element_spacing=self.options['data_table_element_separator'].count('\n')
        string_out=""
        between_section=""
        if self.options['data_table_element_separator'] is not None:
            between_section=self.options['data_table_element_separator']
        if not self.header:
            self.options['header_begin_line']=self.options['header_end_line']=None
            pass
        else:
            self.options["header_begin_line"]=0
            if self.data is None and self.column_names is None and self.footer is None:
                string_out=self.get_header_string()
                self.options["header_end_line"]=None
            else:
                string_out=self.get_header_string()+between_section
                #print("{0} is {1}".format("self.get_header_string()",self.get_header_string()))
                header_end=self.get_header_string()[-1]
                #print("{0} is {1}".format("header_end",header_end))
                if header_end in ["\n"]:
                    adjust_header_lines=0
                else:
                    adjust_header_lines=1
                # I think this is wrong If header string ends in an "\n" fixed for now
                inner_element_spacing=inner_element_spacing
                last_header_line=self.get_header_string().count('\n')+adjust_header_lines
                self.options["header_end_line"]=last_header_line
                next_section_begin=last_header_line+inner_element_spacing-adjust_header_lines

        if not self.column_names:
            self.options['column_names_begin_line']=self.options['column_names_end_line']=None
            pass
        else:
            self.options["column_names_begin_line"]=next_section_begin
            if self.data is None and self.footer is None:
                self.options["column_names_end_line"]=None
                string_out=string_out+self.get_column_names_string()
            else:
                string_out=string_out+self.get_column_names_string()+between_section
                column_names_end=self.get_column_names_string()[-1]
                #print("{0} is {1}".format("column_names_end",column_names_end))
                if column_names_end in ["\n"]:
                    adjust_column_names_lines=0
                else:
                    adjust_column_names_lines=1
                last_column_names_line=self.get_column_names_string().count('\n')+\
                                       self.options["column_names_begin_line"]+adjust_column_names_lines
                self.options["column_names_end_line"]=last_column_names_line
                next_section_begin=last_column_names_line+inner_element_spacing-adjust_column_names_lines
        if not self.data:
            self.options['data_begin_line']=self.options['data_end_line']=None
            pass
        else:
            self.options["data_begin_line"]=next_section_begin
            if self.footer is None:
                self.options["data_end_line"]=None
                string_out=string_out+self.get_data_string()
            else:
                string_out=string_out+self.get_data_string()+between_section
                data_end=self.get_data_string()[-1]
                #print("{0} is {1}".format("column_names_end",column_names_end))
                if data_end in ["\n"]:
                    adjust_data_lines=0
                else:
                    adjust_data_lines=1
                last_data_line=self.get_data_string().count("\n")+\
                                self.options["data_begin_line"]+adjust_data_lines
                self.options["data_end_line"]=last_data_line
                next_section_begin=last_data_line+inner_element_spacing-adjust_data_lines
        if not self.footer:
            self.options['footer_begin_line']=self.options['footer_end_line']=None
            pass
        else:
            self.options["footer_begin_line"]=next_section_begin
            string_out=string_out+self.get_footer_string()
            self.options['footer_end_line']=None
        # set the options back after the string has been made
        if self.inline_comments is None:
            pass
        else:
            lines=string_out.splitlines()
            for comment in self.inline_comments:
                lines=insert_inline_comment(lines,comment=comment[0],line_number=comment[1],
                                            string_position=comment[2],
                                            begin_token=self.options['inline_comment_begin'],
                                            end_token=self.options['inline_comment_end'])
            string_out=string_list_collapse(lines,string_delimiter='\n')
        self.options=original_options
        return string_out

    def get_header_string(self):
        """Returns the header using options in self.options. If block comment is specified, and the header is a
        list it will block comment out the header. If comment_begin and comment_end are specified it will use
        those to represent each line of the header. If header_begin_token and/or header_end_token are specified it
         will wrap the header in those.
        """
        string_out=""
        header_begin=""
        header_end=""
        if self.options["header_begin_token"] is None:
            header_begin=""
        else:
            header_begin=self.options["header_begin_token"]
        if self.options["header_end_token"] is None:
            header_end=""
        else:
            header_end=self.options["header_end_token"]
        # This writes the header
        if self.header is None:
            string_out= ""
        elif self.options["header_line_types"] is not None:
            for index,line in enumerate(self.options["header_line_types"]):
                if index == len(self.options["header_line_types"])-1:
                    end=''
                else:
                    end='\n'
                if line in ['header','header_line','normal']:
                    string_out=string_out+self.header[index]+end
                elif line in ['line_comment','comment']:
                    #print("{0} is {1}".format("index",index))
                    string_out=string_out+line_comment_string(self.header[index],
                                               comment_begin=self.options["comment_begin"],
                                               comment_end=self.options["comment_end"])+end
                elif line in ['block_comment','block']:
                    if index-1<0:
                        block_comment_begin=index
                        block_comment_end=index+2
                        continue
                    elif self.options["header_line_types"][index-1] not in ['block_comment','block']:
                        block_comment_begin=index
                        block_comment_end=index+2
                        continue
                    else:
                        if index+1>len(self.options["header_line_types"])-1:
                            string_out=string_out+line_list_comment_string(self.header[block_comment_begin:],
                                                                           comment_begin=self.options['block_comment_begin'],
                                                                             comment_end=self.options['block_comment_end'],
                                                                           block=True)+end
                        elif self.options["header_line_types"][index+1] in ['block_comment','block']:
                            block_comment_end+=1
                        else:
                            string_out=string_out+\
                                       line_list_comment_string(self.header[block_comment_begin:block_comment_end],
                                                                comment_begin=self.options['block_comment_begin'],
                                                                comment_end=self.options['block_comment_end'],
                                                                block=True)+end
                else:
                    string_out=string_out+line
        elif self.options['treat_header_as_comment'] in [None,True] and self.options["header_line_types"] in [None]:
            # Just happens if the user has set self.header manually
            if isinstance(self.header, StringType):
                string_out=line_comment_string(self.header,
                                               comment_begin=self.options["comment_begin"],
                                               comment_end=self.options["comment_end"])
                #string_out=re.sub('\n','',string_out,count=1)
            elif isinstance(self.header, ListType):
                if self.options['block_comment_begin'] is None:
                    if self.options['comment_begin'] is None:
                        string_out=string_list_collapse(self.header)

                    else:
                        string_out=line_list_comment_string(self.header,comment_begin=self.options['comment_begin'],
                                                        comment_end=self.options['comment_end'])
                        lines_out=string_out.splitlines()

                        # if re.search('\n',self.options['comment_end']):
                        #     string_out=re.sub('\n','',string_out,count=1)
                        #self.options["header_line_types"]=["line_comment" for line in self.header]
                else:
                    string_out=line_list_comment_string(self.header,comment_begin=self.options['block_comment_begin'],
                                                        comment_end=self.options['block_comment_end'],block=True)
                    #self.options["header_line_types"]=["block_comment" for line in self.header]
        else:
            string_out=ensure_string(self.header,list_delimiter="\n",end_if_list="")
        return header_begin+string_out+header_end

    def get_column_names_string(self):
        "Returns the column names as a string using options"
        string_out=""
        # This writes the column_names
        column_name_begin=""
        column_name_end=""
        if self.options["column_names_begin_token"] is None:
            column_name_begin=""
        else:
            column_name_begin=self.options["column_names_begin_token"]
        if self.options["column_names_end_token"] is None:
            column_name_end=""
        else:
            column_name_end=self.options["column_names_end_token"]

        if self.column_names is None:
            string_out=""
        else:
            if isinstance(self.column_names, StringType):
                string_out=self.column_names

            elif isinstance(self.column_names, ListType):
                string_out=list_to_string(self.column_names,
                                          data_delimiter=self.options["column_names_delimiter"],end="")
                #print("{0} is {1}".format('string_out',string_out))
            else:

                string_out=ensure_string(self.column_names)

        #print column_name_begin,string_out,column_name_end
        return column_name_begin+string_out+column_name_end

    def get_data_string(self):
        "Returns the data as a string"
        #Todo:refactor to cut out unused lines
        string_out=""
        if self.data is None:
            string_out= ""
        else:
            if isinstance(self.data, StringType):
                if self.options['data_begin_token'] is None:
                       if self.options['data_end_token'] is None:
                           string_out=self.data
                       else:
                           if re.search(self.options['data_end_token'],self.data):
                               string_out=self.data
                           else:
                               string_out=self.data+self.options['data_end_token']
                else:
                        if self.options['data_end_token'] is None:
                            if re.match(self.options['data_begin_token'],self.data):
                                string_out=self.data
                            else:
                                string_out=self.options['data_begin_token']+self.data
            elif isinstance(self.data,(ListType,np.ndarray)):
                try:
                        #If the first row is a string, we should strip all the tokens and add them back in
                        if isinstance(self.data[0], StringType):
                            if self.options['data_begin_token'] is None:
                                string_out=string_list_collapse(self.data)
                            else:
                                if re.match(self.options['data_begin_token'],self.data[0]):
                                    if self.options['data_end_token'] is None:
                                        string_out=string_list_collapse(self.data)
                                    else:
                                        if re.search(self.options['data_end_token'],self.data[-1]):
                                            string_out=string_list_collapse(self.data)
                                        else:
                                            string_out=string_list_collapse(self.data)+self.options['data_end_token']
                                else:
                                    if self.options['data_end_token'] is None:
                                        string_out=self.options['data_begin_token']+string_list_collapse(self.data)
                                    else:
                                        if re.search(self.options['data_end_token'],self.data[-1]):
                                            string_out=self.options['data_begin_token']+string_list_collapse(self.data)
                                        else:
                                            string_out=self.options['data_begin_token']+\
                                                       string_list_collapse(self.data)+\
                                                       self.options['data_end_token']

                        elif isinstance(self.data[0],(ListType,np.ndarray)):
                            prefix=""
                            if self.options['data_begin_token'] is None:
                                if self.options['data_end_token'] is None:
                                    string_out=list_list_to_string(self.data,data_delimiter=self.options['data_delimiter'],
                                                                   row_formatter_string=self.options['row_formatter_string'],
                                                                   line_begin=self.options["row_begin_token"],
                                                                   line_end=self.options["row_end_token"])
                                else:
                                    string_out=list_list_to_string(self.data,data_delimiter=self.options['data_delimiter'],
                                                                   row_formatter_string=self.options['row_formatter_string'],
                                                                   line_begin=self.options["row_begin_token"],
                                                                   line_end=self.options["row_end_token"])+\
                                                                    self.options['data_end_token']
                            else:
                                if self.options['data_end_token'] is None:
                                    string_out=self.options['data_begin_token']+\
                                               list_list_to_string(self.data,
                                                                   data_delimiter=self.options['data_delimiter'],
                                                                   row_formatter_string=self.options['row_formatter_string'],
                                                                   line_begin=self.options["row_begin_token"],
                                                                   line_end=self.options["row_end_token"])
                                else:
                                    string_out=self.options['data_begin_token']+\
                                               list_list_to_string(self.data,
                                                                   data_delimiter=self.options['data_delimiter'],
                                                                   row_formatter_string=\
                                                                   self.options['row_formatter_string'],
                                                                   line_begin=self.options["row_begin_token"],
                                                                   line_end=self.options["row_end_token"])+\
                                                                    self.options['data_end_token']
                        else:
                            string_out=list_to_string(self.data,
                                                      data_delimiter=self.options['data_delimiter'],
                                                      row_formatter_string=self.options['row_formatter_string'],
                                                      begin=self.options["row_begin_token"],
                                                      end=self.options["row_end_token"])

                except IndexError:
                    pass
            else:
                string_out=ensure_string(self.data)
        if string_out[-1] not in ["\n"] and self.footer is not None and self.options["data_table_element_separator"] is None:
            string_out=string_out+"\n"
        return string_out

    def get_footer_string(self):
        """Returns the footer using options in self.options. If block comment is specified, and the footer is a
        list it will block comment out the footer. If comment_begin and comment_end are specified it will use
        those to represent each line of the footer. If footer_begin_token and/or footer_end_token are specified it
         will wrap the footer in those.
        """
        string_out=""
        footer_begin=""
        footer_end=""
        if self.options["footer_begin_token"] is None:
            footer_begin=""
        else:
            footer_begin=self.options["footer_begin_token"]
        if self.options["footer_end_token"] is None:
            footer_end=""
        else:
            footer_end=self.options["footer_end_token"]
        # This writes the footer
        if self.footer is None:
            string_out= ""
        elif self.options["footer_line_types"] is not None:
            for index,line in enumerate(self.options["footer_line_types"]):
                if index == len(self.options["footer_line_types"])-1:
                    end=''
                else:
                    end='\n'
                if line in ['footer','footer_line','normal']:
                    string_out=string_out+self.footer[index]+end
                elif line in ['line_comment','comment']:
                    end=""
                    string_out=string_out+line_comment_string(self.footer[index],
                                               comment_begin=self.options["comment_begin"],
                                               comment_end=self.options["comment_end"])+end
                elif line in ['block_comment','block']:
                    if index-1<0:
                        block_comment_begin=index
                        block_comment_end=index+2
                        continue
                    elif self.options["footer_line_types"][index-1] not in ['block_comment','block']:
                        block_comment_begin=index
                        block_comment_end=index+2
                        continue
                    else:
                        if index+1>len(self.options["footer_line_types"])-1:
                            string_out=string_out+line_list_comment_string(self.footer[block_comment_begin:],
                                                                           comment_begin=self.options['block_comment_begin'],
                                                                             comment_end=self.options['block_comment_end'],
                                                                           block=True)+end
                        elif self.options["footer_line_types"][index+1] in ['block_comment','block']:
                            block_comment_end+=1
                        else:
                            string_out=string_out+\
                                       line_list_comment_string(self.footer[block_comment_begin:block_comment_end],
                                                                comment_begin=self.options['block_comment_begin'],
                                                                comment_end=self.options['block_comment_end'],
                                                                block=True)+end
                else:
                    string_out=string_out+line
        elif self.options['treat_footer_as_comment'] in [None,True] and self.options["footer_line_types"] in [None]:
            # Just happens if the user has set self.footer manually
            if isinstance(self.footer, StringType):
                string_out=line_comment_string(self.footer,
                                               comment_begin=self.options["comment_begin"],
                                               comment_end=self.options["comment_end"])
                #string_out=re.sub('\n','',string_out,count=1)
            elif isinstance(self.footer, ListType):
                if self.options['block_comment_begin'] is None:
                    if self.options['comment_begin'] is None:
                        string_out=string_list_collapse(self.footer)

                    else:
                        string_out=line_list_comment_string(self.footer,comment_begin=self.options['comment_begin'],
                                                        comment_end=self.options['comment_end'])
                        lines_out=string_out.splitlines()

                        # if re.search('\n',self.options['comment_end']):
                        #     string_out=re.sub('\n','',string_out,count=1)
                        #self.options["footer_line_types"]=["line_comment" for line in self.footer]
                else:
                    string_out=line_list_comment_string(self.footer,comment_begin=self.options['block_comment_begin'],
                                                        comment_end=self.options['block_comment_end'],block=True)
                    #self.options["footer_line_types"]=["block_comment" for line in self.footer]
        else:
            string_out=ensure_string(self.footer,list_delimiter="\n",end_if_list="")
        return footer_begin+string_out+footer_end
    # our current definition of add is not reversible !!!!!!!!!
    # def __radd__(self, other):
    #     "Controls the behavior of radd to use the sum function it is required"
    #     if other==0:
    #         return self
    #     else:
    #         return self.__add__(other)

    def __add__(self, other):
        """Controls the behavior of the addition operator, if column_names are equal it adds rows at the end
        and increments any column named index. If the column_names and number of rows are different it adds columns
        to the table and fills the non-defined rows with self.options['empty_character'] which is None by default. If
        the rows are equal it adds the columns to the table ignoring any columns that are the same. If the headers or
        footers are different it appends them to the left most object."""
        if self==other:
            return
        if self.column_names == other.column_names:
            for row in other.data:
                self.add_row(row)
        elif len(self.data)==len(other.data):
            for index,column in enumerate(other.column_names):
                if column in self.column_names:
                    pass
                else:
                    if other.column_types is not None:
                        column_type=other.column_types[index]
                    else:
                        column_type='string'
                    self.add_column(column_name=column,
                                    column_type=column_type,column_data=other.get_column(column_name=column))
        else:
            for column in other.column_names:
                self.add_column(column)
            for row in other.data:
                data=[self.options['empty_value'] for i in self.column_names]
                self.add_row(data.append(row))
        if self.header is not other.header:
            for line in other.header:
                if line is None:
                    pass
                else:
                    self.header.append(line)
        if self.footer is not other.footer:
            for line in other.footer:
                if line is None:
                    pass
                else:
                    self.footer.append(line)
        return self

    def is_valid(self):
        """Returns True if ascii table conforms to its specification given by its own options"""
        options={}
        for key,value in self.options.items():
            options[key]=value
            # print("self.options[{0}] is {1} ".format(key,value))
        for element in self.elements:
            if self.__dict__[element] is None:
                options[element]=None
            else:
                options[element]=[]
        options["validate"]=True
        newtable=AsciiDataTable(None,**options)
        lines=self.build_string().splitlines()
        for index,line in enumerate(lines):
            lines[index]=line+"\n"
        newtable.lines=lines
        newtable.__parse__()
        # print newtable.data
        # print newtable.column_names
        # print newtable
        #print_comparison(newtable.footer,None)
        newtable.update_model()
        # The new table rows are not being coerced into the right format
        #print newtable
        #newtable.update_model()
        #print newtable.options
        #print self.options
        #print newtable.data
        # print newtable.options==self.options
        # for option_key,option_value in newtable.options.iteritems():
        #     print("New Table Option {0} is {1} ".format(option_key,option_value))
        #     print("self.options[{0}] is {1} ".format(option_key,self.options[option_key]))
        #     print_comparison(option_value,self.options[option_key])
        # #print self
        return self==newtable
        # create a clone and then parse the clone and compare it to the
        # original. If they are equal then it is valid
        #self.add_inline_comments()

    def __eq__(self, other):
        """Defines what being equal means for the AsciiDataTable Class"""
        compare_elements=['metadata','header','column_names','data','footer']
        truth_table=[]
        output=False
        for item in compare_elements:
            if self.__dict__[item]==other.__dict__[item]:
                truth_table.append(True)
            else:
                truth_table.append(False)
        if False in truth_table:
            output=False
        else:
            output=True
        #print("{0} is {1}".format("truth_table",truth_table))

        return output

    def __ne__(self,other):
        """Defines what being not equal means for the AsciiDataTable Class"""
        compare_elements=['metadata','header','column_names','data','footer']
        truth_table=[]
        output=True
        for item in compare_elements:
            if self.__dict__[item]==other.__dict__[item]:
                truth_table.append(True)
            else:
                truth_table.append(False)
        if False in truth_table:
            output=True
        else:
            output=False
        return output

    def add_row(self,row_data):
        """Adds a single row given row_data which can be an ordered list/tuple or a dictionary with
        column names as keys"""
        if self.data is None:
            self.data=[]
        if len(row_data) not in [len(self.column_names),len(self.column_names)]:
            print(" could not add the row, dimensions do not match")
            return
        if isinstance(row_data,(ListType,np.ndarray)):
            self.data.append(row_data)
        elif isinstance(row_data,DictionaryType):
            data_list=[row_data[column_name] for column_name in self.column_names]
            self.data.append(data_list)

    def remove_row(self,row_index):
        """Removes the row specified by row_index and updates the model. Note index is relative to the
        data attribute so to remove the first row use row_index=0 and the last data row is row_index=-1"""
        self.data.pop(row_index)
        self.update_model()

    def add_column(self,column_name=None,column_type=None,column_data=None,format_string=None):
        """Adds a column with column_name, and column_type. If column data is supplied and it's length is the
        same as data(same number of rows) then it is added, else self.options['empty_character'] is added in each
        spot in the preceding rows"""
        original_column_names=self.column_names[:]
        try:
            self.column_names=original_column_names+[column_name]
            if self.options["column_types"]:
                old_column_types=self.options["column_types"][:]
                self.options["column_types"]=old_column_types+[column_type]
            if len(column_data) == len(self.data):
                for index,row in enumerate(self.data[:]):
                    #print("{0} is {1}".format('self.data[index]',self.data[index]))
                    #print("{0} is {1}".format('row',row))
                    new_row=row[:]
                    new_row.append(column_data[index])
                    self.data[index]=new_row
            else:
                for index,row in enumerate(self.data[:]):
                    self.data[index]=row.append(self.options['empty_value'])
                    if column_data is not None:
                        for item in column_data:
                            empty_row=[self.options['empty_value'] for column in original_column_names]
                            empty_row.append(item)
                            self.add_row(empty_row)
            if self.options["row_formatter_string"] is None:
                pass
            else:
                if format_string is None:
                    self.options["row_formatter_string"]=self.options["row_formatter_string"]+\
                                                                 '{delimiter}'+"{"+str(len(self.column_names)-1)+"}"
                else:
                    self.options["row_formatter_string"]=self.options["row_formatter_string"]+format_string
            #self.update_model()
        except:
            self.column_names=original_column_names
            print("Could not add columns")
            raise

    def remove_column(self,column_name=None,column_index=None):
        """Removes the column specified by column_name or column_index and updates the model. The column is removed from
        column_names, data and if present column_types, column_descriptions and row formatter"""
        if self.column_names:
            number_of_columns=len(self.column_names[:])
        elif self.data:
            number_of_columns=len(self.data[0])
        else:
            raise
        if column_name:
            column_index=self.column_names.index(column_name)
        elif column_index:
            pass
        else:
            raise TypeError("To remove a column either the name or index must be specified")
        #print("{0} is {1}".format("column_index",column_index))
        #print("{0} is {1}".format("type(column_index)",type(column_index)))
        self.column_names.pop(column_index)
        for row in self.data:
            row.pop(column_index)
        if self.options["row_formatter_string"]:
            format_string="{"+str(column_index)+"}"+"{delimiter}"
            self.options["row_formatter_string"]=\
                self.options["row_formatter_string"].replace(format_string,"")
            for index in range(column_index+1,number_of_columns):

                old_format_string="{"+str(index)
                new_format_string="{"+str(index-1)
                self.options["row_formatter_string"]=\
                    self.options["row_formatter_string"].replace(old_format_string,new_format_string)

        #Todo:Add remove column functionality

    def add_index(self):
        """Adds a column with name index and values that are 0 referenced indices, does nothing if there is
        already a column with name index, always inserts it at the 0 position"""
        if 'index' in self.column_names:
            print("Add Index passed")
            pass
        else:
            self.column_names.insert(0,'index')
            for index,row in enumerate(self.data):
                self.data[index].insert(0,index)
            if self.options['column_types']:
                self.options['column_types'].insert(0,'int')
            if self.options['row_formatter_string']:
                temp_formatter_list=self.options['row_formatter_string'].split("{delimiter}")
                iterated_row_formatter_list=[temp_formatter_list[i].replace(str(i),str(i+1))
                                             for i in range(len(temp_formatter_list))]
                new_formatter=string_list_collapse(iterated_row_formatter_list,string_delimiter="{delimiter}")
                self.options['row_formatter_string']='{0}{delimiter}'+new_formatter

    def move_footer_to_header(self):
        """Moves the DataTable's footer to the header and updates the model"""
        # check to see if the footer is defined
        if self.footer is None:
            return
        try:
          for item in self.footer:
              self.header.append(item)
        except:
          self.header=ensure_string(self.header)+ensure_string(self.footer)
        self.footer=None

    # # This actually operated on self.lines before parsing and not directly on self.header
    # def add_comment(self,comment):
    #     "Adds a line comment to the header"
    #     self.header.append(comment)
    #     self.options["header_line_types"].insert('line_comment',len(self.header)-1)

    def add_inline_comment(self,comment="",line_number=None,string_position=None):
        "Adds an inline in the specified location"
        try:
            self.inline_comments.append([comment,line_number,string_position])
        except:pass

    # def add_block_comment(self,comment,element=None,location=None):
    #     "Adds a block comment in the specified location"
    #     pass

    def get_options(self):
        "Prints the option list"
        for key,value in self.options.items():
            print(("{0} = {1}".format(key,value)))
    def get_row(self,row_index=None):
        """Returns the row as a list specified by row_index"""
        if row_index is None:
            return
        else:
            return self.data[row_index]

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

    def get_unique_column_values(self,column_name=None,column_index=None):
        """Returns the unique values in a  column as a list given a column name or column index"""
        if column_name is None:
            if column_index is None:
                return
            else:
                column_selector=column_index
        else:
            column_selector=self.column_names.index(column_name)
        out_list=list(set([self.data[i][column_selector] for i in range(len(self.data))]))
        return out_list

    def __getitem__(self, items):
        """Controls how the model responds to self["Item"]"""
        out_data=[]
        column_selectors=[]
        #print items[0]
        if isinstance(items,(StringType,IntType)):
            return self.get_column(items)
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

    def get_data_dictionary_list(self,use_row_formatter_string=True):
        """Returns a python list with a row dictionary of form {column_name:data_column}"""
        try:
            if self.options["row_formatter_string"] is None:
                use_row_formatter_string=False
            if use_row_formatter_string:
                list_formatter=[item.replace("{"+str(index),"{0")
                                for index,item in enumerate(self.options["row_formatter_string"].split("{delimiter}"))]
            else:
                list_formatter=["{0}" for i in self.column_names]
            #print self.column_names
            #print self.data
            #print list_formatter
            #print len(self.column_names)==len(self.data[0])
            #print len(list_formatter)==len(self.data[0])
            #print type(self.data[0])
            out_list=[{self.column_names[i]:list_formatter[i].format(value) for i,value in enumerate(line)}
                      for line in self.data]
            return out_list
        except:
            print("Could not form a data_dictionary_list, check that row_formatter_string is properly defined")
            #print(out_list)
            raise

    def save_schema(self,path=None,format=None):
        """Saves the tables options as a text file or pickled dictionary (default).
        If no name is supplied, autonames it and saves"""
        if path is None:
            path=auto_name(self.name.replace('.'+self.options["extension"],""),'Schema',self.options["directory"],'txt')
        if format in [None,'python','pickle']:
            pickle.dump(self.options,open(path,'wb'))
        elif format in ['txt','text','.txt']:
            file_out=open(path,'w')
            keys=sorted(list(self.options.keys()))
            for key in keys:
                out_key=str(key).replace("\n","\\n")
                out_value=str(self.options[key]).replace("\n","\\n")
                file_out.write("{0} : {1} \n".format(out_key,out_value))
            file_out.close()
    def change_unit_prefix(self,column_selector=None,old_prefix=None,new_prefix=None,unit='Hz'):
        """Changes the prefix of the units of the column specified by column_selector (column name or index)
        example usage is self.change_unit_prefix(column_selector='Frequency',old_prefix=None,new_prefix='G',unit='Hz')
        to change a column from Hz to GHz. It updates the data values, column_descriptions, and column_units if they
        exist, see http://www.nist.gov/pml/wmd/metric/prefixes.cfm for possible prefixes"""

        multipliers={"yotta":10.**24,"Y":10.**24,"zetta":10.**21,"Z":10.**21,"exa":10.**18,"E":10.**18,"peta":10.**15,
                     "P":10.**15,"tera":10.**12,"T":10.**12,"giga":10.**9,"G":10.**9,"mega":10.**6,"M":10.**6,
                     "kilo":10.**3,"k":10.**3,"hecto":10.**2,"h":10.**2,"deka":10.,"da":10.,None:1.,"":1.,
                     "deci":10.**-1,"d":10.**-1,"centi":10.**-2,"c":10.**-2,"milli":10.**-3,"m":10.**-3,
                     "micro":10.**-6,"mu":10.**-6,"\u00B5":10.**-6,"nano":10.**-9,
                     "n":10.**-9,"pico":10.**-12,"p":10.**-12,"femto":10.**-15,
                     "f":10.**-15,"atto":10.**-18,"a":10.**-18,"zepto":10.**-21,"z":10.**-21,
                     "yocto":10.**-24,"y":10.**-24}
        # change column name into column index
        try:
            if old_prefix is None:
                old_prefix=""
            if new_prefix is None:
                new_prefix=""
            old_unit=old_prefix+unit
            new_unit=new_prefix+unit
            if column_selector in self.column_names:
                column_selector=self.column_names.index(column_selector)
            for index,row in enumerate(self.data):
                if isinstance(self.data[index][column_selector],FloatType):
                    #print "{0:e}".format(multipliers[old_prefix]/multipliers[new_prefix])
                    self.data[index][column_selector]=\
                    (multipliers[old_prefix]/multipliers[new_prefix])*self.data[index][column_selector]
                elif isinstance(self.data[index][column_selector],(StringType,IntType)):
                    self.data[index][column_selector]=\
                    str((multipliers[old_prefix]/multipliers[new_prefix])*float(self.data[index][column_selector]))
                else:
                    print(type(self.data[index][column_selector]))
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
            print(("Could not change the unit prefix of column {0}".format(column_selector)))
            raise
    def copy(self):
        "Creates a shallow copy of the data table"
        return copy.copy(self)


class KnowledgeSystem(AsciiDataTable):
    """A Knowledge System is a collection of properties (context) and a collection of metadata about those properties
    (obligate contexts). """
    def __init__(self,file_path=None,**options):
        """Intializes a knowledge system"""
        defaults={"context":None,"key_formatter_string":"{context}.{obligate}:{property}"}
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        if file_path is None:
            self.options["column_names"]=["Property"]
            self.options["data"]=[["Self"],["Default"]]
            AsciiDataTable.__init__(self,None,**self.options)
        else:
            AsciiDataTable.__init__(self,file_path,**self.options)
        self.context=self.options["context"]
        self.obligate_names=self.column_names
        self.properties=self["Property"]
    #get a row of a knowledge system based on property
    def get_property_defintion(self,property_name):
        """Retrieves a row of the knowledge system based on the property_name"""
        row_index=self["Property"].index(property_name)
        return self.get_row(row_index)

    def get_property_dictionary(self,property_name):
        """Returns a dictionary of the form {obligate_name:obligate_value}"""
        row_index=self["Property"].index(property_name)
        property_dictionary={self.column_names[index]:value for index,value in enumerate(self.data[:][row_index])}
        return  property_dictionary

    def add_property(self,property_name,**obilgate_values):
        """Adds a new row to the knowledge system, obilgate values should be in the form of a dictionary, or key
        word arguments like obligate=value.
        obligate_values={obligate:value}, if an obligate is not specified, the value defaults to the default property
        or to None if not specified"""
        if property_name in self["Property"]:
            print("Property Exists Use edit_entry to modify values")
            return None
        defaults={}
        obligate_dictionary={}
        for key,value in defaults.items():
            obligate_dictionary[key]=value
        for key,value in obilgate_values.items():
            obligate_dictionary[key]=value
        new_row=[]
        column_names=self.column_names[:]
        for column_index,column_name in enumerate(column_names):
            if column_name in list(obligate_dictionary.keys()):
                new_row.append(obligate_dictionary[column_name])
            elif re.match("property",column_name,re.IGNORECASE):
                new_row.append(property_name)
            else:
                if self.data[1][column_index]:
                    new_row.append(self.data[1][column_index])
                else:
                    new_row.append(None)
        self.add_row(new_row)

    def edit_entry(self,property_name,obligate_name,new_value):
        """Edit a value for a specific property and obligate"""
        column_index=self.column_names.index(obligate_name)
        row_index=self["Property"].index(property_name)
        self.data[row_index][column_index]=new_value

    def get_entry(self,property_name,obligate_name):
        """returns a value for a specific property and obligate"""
        column_index=self.column_names.index(obligate_name)
        row_index=self["Property"].index(property_name)
        out=self.data[:][row_index][column_index]
        return out


    def to_row_modelled(self):
        """Returns a sparse, row modelled version of the knowledge system"""
        out_dictionary={}
        for property_name in self["Property"][:]:
            for obligate_name in self.column_names[:]:
                if obligate_name is not "Property":
                    key=self.options["key_formatter_string"].format(**{"context":self.context,
                                                                       "obligate":obligate_name,"property":property_name})
                    # this leaves out Nones
                    if self.get_entry(property_name,obligate_name):
                        out_dictionary[key]=self.get_entry(property_name,obligate_name)
        return out_dictionary
    def add_obligate(self,obligate_name,**property_value_dictionary):
        """Adds an obligate-context to the knowledge system. Optional default and self values. Default will be assumed
        for all properties without an obligate value defined, self holds a description of the obligate.
        care must be taken not to try to assign the value as self but use Self"""
        # adds a column to the table where the first two rows are obligate_self and obligate_default
        defaults={"Self":None,"Default":None}
        obligate_dictionary={}
        for key,value in defaults.items():
            obligate_dictionary[key]=value
        for key,value in property_value_dictionary.items():
            obligate_dictionary[key]=value
        column_data=[]
        properties=self.get_column("Property")
        for property_name in properties:
            if property_name in list(obligate_dictionary.keys()):
                column_data.append(obligate_dictionary[property_name])
            else:
                if obligate_dictionary["Default"]:
                    column_data.append(obligate_dictionary["Default"])
                else:
                    column_data.append(None)

        self.add_column(column_name=obligate_name,column_data=column_data)


class Encyclopedia(object):
    """An Encyclopedia is a collection of descriptions"""

    def __init__(self, file_path=None, **options):
        """Initializes an Encyclopedia"""
        defaults = {"key_formatter_string": "{Entity}-{Context}-{Property}",
                    "key_value__formatter": None,
                    "key_value_pattern": None,
                    "entity_table": None,
                    "entity_attributes": None,
                    "universe": None,
                    "context_obligate_delimiter": ".",
                    "encyclopedia_begin_token": "Begin Encyclopedia",
                    "encyclopedia_end_token": "End Encyclopedia",
                    "entity_table_primary_key": "index",
                    "entity_table_begin_token": "Begin Entity Table",
                    "entity_table_end_token": "End Entity Table",
                    "universe_begin_token": "Begin Universe",
                    "universe_end_token": "End Universe",
                    "description_begin_token": "Begin Descriptions",
                    "descriptions_end_token": "End Descriptions",
                    "knowledge_system_begin_prefix": "Begin Knowledge System",
                    "knowledge_system_end_prefix": "End Knowledge System"
                    }
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        if file_path is None:
            # Create a new encylcopedia
            self.entity_table = AsciiDataTable(None, column_names=["Entity"], data=[["self"]])
            self.universe = {}
            self.descriptions = AsciiDataTable(None, column_names=["Entity", "Context", "Property", "Value"])
            self.contexts = []
        else:
            pass
        # parse an existing data table
        # requires options to be set properly

    def set_entity_primary_key(entity_table_column_name):
        """Sets the column name to use for the entity primary key,
        by default the primary key is row number (index)"""
        # The primary key is a column or columns that can be refered to instead of the full row of the entity table
        self.entity_primary_key = entity_table_column_name

    def add_description(self, entity, context, property_name, value, obligate=None):
        """Adds a description to the encyclopedia, the entity, context (or knowledge_system name),property_name,
        and value are required. If the context is an obligate-context then add obligate"""
        if obligate is not None:
            context = context + self.options["context_obligate_deilimiter"] + obligate

        self.descriptions.add_row([entity, context, property_name, value])

    def add_knowledge_system(self, knowledge_system):
        """Adds a knowledge system to the universe being used for the encyclopedia"""
        self.universe[knowledge_system.context] = knowledge_system
        self.contexts = sorted(list(self.universe.keys())[:])

    def add_entity(self, entity):
        """Adds an entity to entity_table. The entity is a row in the entity table"""
        self.entity_table.add_row(entity)

    def get_entity(self, entity_reference, by="row"):
        """Gets an entity, it can be by row index (i.e index) or the primary key"""
        if re.search("pk|primary|key", by, re.IGNORECASE) and not re.match("index", self.entity_primary_key):
            try:
                row_number = self.entity_table[self.entity_primary_key].index(entity)
                return self.entity_table.data[:][row_number]
            except:
                print(("Could not find {0} in entity table".format(entity_reference)))
        else:
            return self.entity_table.data[:][entity_reference]

    def __str__(self):
        """Controls the string behavior of the encyclopedia"""
        out_string = ""
        if self.entity_table:
            out_string = "Begin Entity\n" + str(self.entity_table) + "\nEnd Entity\n"
        if self.contexts:
            for key in self.contexts[:]:
                out_string = out_string + "\nBegin Knowledge System {0} \n".format(key) + str(self.universe[key]) + \
                             "\nEnd Knowledge System: {0} \n".format(key)
        if self.descriptions:
            out_string = out_string + "\nBegin Descriptions \n" + str(self.descriptions) + "\nEnd Descriptions \n"
        return out_string

    def get_descriptions(self, entity):
        """Returns all descriptions of an entity"""
        results = [x for x in self.descriptions.data if x[0] == entity]
        return results

    def get_entities(self, context, property_name, value, obligate=None):
        """Returns a subset of entity table that has context:property=Value"""
        if obligate is not None:
            context = context + self.options["context_obligate_deilimiter"] + obligate
        results = [x for x in self.descriptions.data if x[1] == context and x[2] == property_name and x[3] == value]
        return results[0]

    def get_flat_table(self):
        """Returns a flat table representation of the Encyclopedia"""
        # makes sure the entity is expanded and the context is of the form context.obligate
        pass

    def get_description_dictionary(self):
        """Returns a python dictionary of descriptions where the key is determined by key_formatter_string"""
        dictionary_form = {}
        descriptions_dictionary_list = self.descriptions.get_data_dictionary_list()
        for row_index, description in enumerate(self.descriptions.data[:]):
            key = self.options["key_formatter_string"].format(**descriptions_dictionary_list[row_index])
            dictionary_form[key] = descriptions_dictionary_list[row_index]["Value"]
        return dictionary_form


#-----------------------------------------------------------------------------
# Module Scripts
def test_AsciiDataTable():
    options={"column_names":["a","b","c"],"data":[[0,1,2],[2,3,4]],"data_delimiter":'\t',
             "header":['Hello There\n',"My Darling"],"column_names_begin_token":'!',"comment_begin":'#',
             "directory":TESTS_DIRECTORY}
    new_table=AsciiDataTable(file_path=None,**options)
    print(new_table.data)
    #print dir(new_table)
    for key,value in new_table.options.items():
        print(("{0} = {1}".format(key,value)))
    print(new_table.get_header_string())
    print(new_table.get_data_string())
    print(new_table.build_string())
    print(new_table.path)
    new_table.save()
    print("Test add_index")
    new_table.add_index()
    new_table.add_index()
    new_table.add_index()
    print(new_table)
    new_table.data[1][0]=4
    print(new_table)
    new_table.update_index()
    print(new_table)

def test_open_existing_AsciiDataTable():
    # To make this controlled we should create a data table and then save it.
    # after saving it we should open it with the options
    options={"data_delimiter":',',
                  "column_names_delimiter":"{column_names_delimiter}",
                  "specific_descriptor":'Data',
                  "general_descriptor":'Table',
                  "directory":None,
                  "extension":'txt',
                  "comment_begin":"{comment_begin}",
                  "comment_end":"{comment_end}",
                  "inline_comment_begin":"{inline_comment_begin}",
                  "inline_comment_end":"{inline_comment_end}",
                  "block_comment_begin":"{block_comment_begin}\n",
                  "block_comment_end":"\n{block_comment_end}",
                  "footer_begin_token":"{footer_begin_token}\n",
                  "footer_end_token":"\n{footer_end_token}",
                  "header_begin_token":"{header_begin_token}\n",
                  "header_end_token":"\n{header_end_token}",
                  "column_names_begin_token":"{column_names_begin_token}",
                  "column_names_end_token":"{column_names_end_token}",
                  "data_begin_token":"{data_begin_token}\n",
                  "data_end_token":"\n{data_end_token}",
                  "metadata_delimiter":"{metadata_delimiter}",
                  "header":["self.header[0]","self.header[1]","self.header[2]","self.header[3]","","self.header[4]"],
                  "column_names":["column_names[0]","column_names[1]","column_names[2]"],
                  "data":[["data[0][0]","data[1][0]","data[2][0]",1.0],["data[0][1]","data[1][1]","data[2][1]",2.0]],
                  "footer":["self.footer[0]","self.footer[1]"],
                  "inline_comments":[["inline_comments[0][0]",2,-1]],
                  "empty_value":None,
                  "data_table_element_separator":'\n{data_table_element_separator}\n',
                  "treat_header_as_comment":None,
                  "treat_footer_as_comment":None,
                  "header_line_types":["block_comment","block_comment","line_comment","header","header","line_comment"],
                  "column_types":["str","string","STR","float"],
                  "row_formatter_string":"{0}{delimiter}{1}{delimiter}{2}{delimiter}{3:.2f}"
                  }
    os.chdir(TESTS_DIRECTORY)
    new_table=AsciiDataTable(None,**options)
    table_string_1=str(new_table)
    print("Printing the lines representation of the table with line numbers")
    print(("-"*80+"\n"))
    for index,line in enumerate(table_string_1.splitlines()):
        print(("{0} {1}".format(index,line)))
    new_table.save()
    file_path=new_table.path
    new_options={}
    for key,value in new_table.options.items():
        new_options[key]=value
    new_table_1=AsciiDataTable(file_path=file_path,**new_options)
    table_string_2=str(new_table_1)
    print("Printing the lines representation of the opened table with line numbers")
    print(("-"*80+"\n"))
    for index,line in enumerate(table_string_2.splitlines()):
        print(("{0} {1}".format(index,line)))
    #print new_table_1
    print("Printing the line by line equality of the table strings")
    print(("-"*80))
    for index,line in enumerate(table_string_2.splitlines()):
        print(("{0} {1}".format(index,line==table_string_1.splitlines()[index])))
    print(("table_1 header is {0}".format(new_table.header)))
    print(("new_table_1 header is {0}".format(new_table_1.header)))
    print(("The assertion that the built table is equal to the opened table is {0}".format(new_table==new_table_1)))
    # new_table.get_options_by_element('columns')
    # print new_table.lines
    # print new_table.header
    # print new_table.get_header_string()
    # print new_table.column_names
    # print new_table.get_column_names_string()
    # print new_table.data
    # print new_table.get_data_string()
    # print new_table.footer
    # print new_table.get_footer_string()
    # print new_table_1
    # temp_options={"data_delimiter":',','column_names_delimiter':',',
    #          "column_names_begin_token":'#',"comment_begin":'#',"comment_end":'\n',
    #          "directory":TESTS_DIRECTORY,'header_begin_token':'BEGIN HEADER\n',
    #               'header_end_token':'END HEADER','data_begin_token':'BEGIN DATA\n','data_end_token':"END DATA"}
    # new_table.save('new_test_table.txt',**temp_options)

def test_AsciiDataTable_equality():
    options={"column_names":["a","b","c"],"data":[[0,1,2],[2,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'!',"comment_begin":'#',
             "directory":TESTS_DIRECTORY,"treat_header_as_comment":False}
    new_table=AsciiDataTable(file_path=None,**options)
    print(new_table.data)
    new_table_2=AsciiDataTable()
    new_table_2.options=new_table.options
    new_table_2.header=new_table.header
    new_table_2.column_names=new_table.column_names
    new_table_2.data=[[0,1,2],[2,3,4]]
    print(new_table==new_table_2)
    print(new_table!=new_table_2)
    new_table_2.data[0][0]=9

    print(new_table.data==new_table_2.data)
    print(new_table==new_table_2)
    print(new_table_2)
    print(new_table)

def test_inline_comments():
    options={"column_names":["a","b","c"],"data":[[0,1,2],[2,3,4]],"data_delimiter":'\t',
             "header":['Hello There\n',"My Darling"],"column_names_begin_token":'!',"comment_begin":'#',
             "directory":TESTS_DIRECTORY,'inline_comment_begin':'(*','inline_comment_end':'*)',
             'inline_comments':[["My Inline Comment",0,5]]}
    new_table=AsciiDataTable(**options)
    print(new_table)

def test_add_row():
    options={"column_names":["a","b","c"],"data":[[0,1,2],[2,3,4]],"data_delimiter":'\t',
             "header":['Hello There\n',"My Darling"],"column_names_begin_token":'!',"comment_begin":'#',
             "directory":TESTS_DIRECTORY}
    new_table=AsciiDataTable(**options)
    print("Table before add row")
    print(new_table)
    print("Add the row 0,1,3")
    new_table.add_row([0,1,3])
    print(new_table)

def test_add_index():
    options={"column_names":["a","b","c"],"data":[[0,1,2],[2,3,4]],"data_delimiter":'\t',
             "header":['Hello There\n',"My Darling"],"column_names_begin_token":'!',"comment_begin":'#',
             "directory":TESTS_DIRECTORY,'treat_header_as_comment':False}
    new_table=AsciiDataTable(None,**options)
    print("Table before add row")
    print("*"*80)
    print(new_table)
    print("Add the row 0,1,3")
    print("*"*80)
    new_table.add_row([0,1,3])
    print(new_table)
    print("Add an index")
    print("*"*80)
    new_table.add_index()
    print(new_table)
    print("Now Get the index column")
    print(new_table.get_column(column_name='index'))

def show_structure_script():
    """ Shows a table elements by substituting the names Explicitly
    :return: None
    """
    os.chdir(TESTS_DIRECTORY)
    options={"data_delimiter":'{data_delimiter}',
                  "column_names_delimiter":"{column_names_delimiter}",
                  "specific_descriptor":'Data',
                  "general_descriptor":'Table',
                  "directory":None,
                  "extension":'txt',
                  "comment_begin":"{comment_begin}",
                  "comment_end":"{comment_end}\n",
                  "inline_comment_begin":"{inline_comment_begin}",
                  "inline_comment_end":"{inline_comment_end}",
                  "block_comment_begin":"{block_comment_begin}\n",
                  "block_comment_end":"\n{block_comment_end}",
                  "footer_begin_token":"{footer_begin_token}\n",
                  "footer_end_token":"\n{footer_end_token}",
                  "header_begin_token":"{header_begin_token}\n",
                  "header_end_token":"\n{header_end_token}",
                  "column_names_begin_token":"{column_names_begin_token}",
                  "column_names_end_token":"{column_names_end_token}",
                  "data_begin_token":"{data_begin_token}\n",
                  "data_end_token":"\n{data_end_token}",
                  "metadata_delimiter":"{metadata_delimiter}",
                  "header":["self.header[0]","self.header[1]","self.header[2]","self.header[3]","self.header{4]"],
                  "column_names":["column_names[0]","column_names[1]","column_names[2]"],
                  "data":[["data[0][0]","data[1][0]","data[2][0]"],["data[0][1]","data[1][1]","data[2][1]"]],
                  "footer":["self.footer[0]","self.footer[1]"],
                  "inline_comments":[["inline_comments[0][0]",2,-1]],
                  "row_formatter_string":None,
                  "row_begin_token":"{row_begin_token}",
                  "row_end_token":"{row_end_token}\n",
                  "empty_value":None,
                  "data_table_element_separator":'\n{data_table_element_separator}\n',
                  "treat_header_as_comment":None,
                  "treat_footer_as_comment":None
                  }
    new_table=AsciiDataTable(**options)
    #new_table.options["block_comment_begin"]=new_table.options["block_comment_end"]=None
    new_table.options["header_line_types"]=["header","header","line_comment","block_comment","block_comment"]
    print("Printing the string representation of the table")
    print(("-"*80))
    print(new_table)
    test_string=str(new_table)
    test_lines=test_string.splitlines()
    print("Printing the lines representation of the table with line numbers")
    print(("-"*80))
    for index,line in enumerate(test_lines):
        print(("{0} {1}".format(index,line)))

    for item in new_table.elements:
        if item in ['inline_comments','metadata']:
            pass
        else:
            begin_line=new_table.options["%s_begin_line"%item]
            end_line=new_table.options["%s_end_line"%item]
            print(("-"*80))
            print(("The result of self.lines[{0}:{1}] is :".format(begin_line,end_line)))
            for line in test_lines[begin_line:end_line]:
                print(line)
            print(("-"*80))
    # new_table.footer=None
    # print("Printing the string representation of the table")
    # print("-"*80)
    # print new_table
    # test_string=str(new_table)
    # test_lines=test_string.splitlines()
    # print("Printing the lines representation of the table with line numbers")
    # print("-"*80)
    # for index,line in enumerate(test_lines):
    #     print("{0} {1}".format(index,line))
    #
    # for item in new_table.elements:
    #     if item is 'inline_comments':
    #         pass
    #     else:
    #         begin_line=new_table.options["%s_begin_line"%item]
    #         end_line=new_table.options["%s_end_line"%item]
    #         print("-"*80)
    #         print("The result of self.lines[{0}:{1}] is :".format(begin_line,end_line))
    #         for line in test_lines[begin_line:end_line]:
    #             print line
    #         print("-"*80)
    #     #
    # end_line=6
    # print("-"*80)
    # print("The result of self.lines[:{0}] is :".format(end_line))
    # for line in test_lines[:end_line]:
    #     print line
    #print new_table.get_options()

def test_save_schema():
    "tests the save schema method of the Ascii Data Table"
    os.chdir(TESTS_DIRECTORY)
    options={"data_delimiter":'{data_delimiter}',
                  "column_names_delimiter":"{column_names_delimiter}",
                  "specific_descriptor":'Data',
                  "general_descriptor":'Table',
                  "directory":None,
                  "extension":'txt',
                  "comment_begin":"{comment_begin}",
                  "comment_end":"{comment_end}",
                  "inline_comment_begin":"{inline_comment_begin}",
                  "inline_comment_end":"{inline_comment_end}",
                  "block_comment_begin":"{block_comment_begin}\n",
                  "block_comment_end":"\n{block_comment_end}",
                  "footer_begin_token":"{footer_begin_token}\n",
                  "footer_end_token":"\n{footer_end_token}",
                  "header_begin_token":"{header_begin_token}\n",
                  "header_end_token":"\n{header_end_token}",
                  "column_names_begin_token":"{column_names_begin_token}",
                  "column_names_end_token":"{column_names_end_token}",
                  "data_begin_token":"{data_begin_token}\n",
                  "data_end_token":"\n{data_end_token}",
                  "metadata_delimiter":"{metadata_delimiter}",
                  "header":["self.header[0]","self.header[1]","self.header[2]","self.header[3]","","self.header[4]"],
                  "column_names":["column_names[0]","column_names[1]","column_names[2]"],
                  "data":[["data[0][0]","data[1][0]","data[2][0]",'1.0'],["data[0][1]","data[1][1]","data[2][1]",2.0]],
                  "footer":["self.footer[0]","self.footer[1]"],
                  "inline_comments":[["inline_comments[0][0]",2,-1]],
                  "empty_value":None,
                  "data_table_element_separator":'\n{data_table_element_separator}\n',
                  "treat_header_as_comment":None,
                  "treat_footer_as_comment":None,
                  "header_line_types":["block_comment","block_comment","line_comment","header","header","line_comment"],
                  "column_types":["str","string","STR","float"],
                  "row_formatter_string":"{0}{delimiter}{1}{delimiter}{2}{delimiter}{3:.2f}"

                  }
    new_table=AsciiDataTable(None,**options)
    print(" New Table is:")
    new_table.__parse__()
    print(new_table)
    print(type(new_table.data[0][3]))
    print(new_table.get_data_dictionary_list())
    new_table.add_index()
    print(new_table.get_data_dictionary_list(False))
    #print("-"*80)
    #new_table.save()
    #new_table.save_schema()
    options_2=new_table.options
    #new_table_2=AsciiDataTable(new_table.path,**options_2)
    #print_comparison(new_table.header,new_table_2.header)

def test_read_schema():
    """ Tests the read_schema function
    """
    os.chdir(TESTS_DIRECTORY)
    file_path="Data_Table_20160301_031_Schema_20160301_001.txt"
    schema=read_schema(file_path)
    print(schema)

def test_change_unit_prefix():
    """Tests the change_unit_prefix method of the AsciiDataTable Class
    """
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)
    print(" After creation the table looks like")
    print(("*"*80))
    print(new_table)
    print(new_table.options["column_units"])
    print(new_table.options["column_descriptions"])
    new_table.change_unit_prefix(column_selector='Frequency',old_prefix=None,new_prefix='G',unit='Hz')
    print(" After running change_unit_prefix(column_selector='Frequency',old_prefix=None,new_prefix='G',unit='Hz')  "
          "the table is ")
    print(new_table)
    print("The options column_units and column_descriptions are:")
    print(new_table.options["column_units"])
    print(new_table.options["column_descriptions"])
    print(new_table.is_valid())

def test_add_column():
    "Tests the add_column method of AsciiDataTable"
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)
    print("The new table before adding the column is :\n")
    print(new_table)
    new_table.add_column(column_name='Test',column_type='float',column_data=[3,5.0201],format_string=None)
    print(("The value of {0} is {1}".format('new_table.options["row_formatter_string"]',
                                           new_table.options["row_formatter_string"])))
    print("The new table after adding the column is :\n")
    print(new_table)
def test_AsciiDataTable_get_column_and_getitem():
    """Tests the get_column and __getitem__ methods"""
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)
    print("The new table is :\n")
    print(new_table)

    print(("The value of {0} is {1}".format('new_table["Frequency"]',
                                           new_table["Frequency"])))
    print(("The value of {0} is {1}".format('new_table.get_column("Frequency")',
                                           new_table.get_column("Frequency"))))
def test_copy_method():
    """Tests the copy() method"""
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)
    print("The new table is :\n")
    print(new_table)

    print("Coping the new table")
    copy_of_table=new_table.copy()

    print(("The value of {0} is {1}".format('new_table.copy()',
                                           copy_of_table)))
def test_add_method():
    """Tests the __add__ method"""
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],
             "data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)
    new_table_2=AsciiDataTable(None,**options)
    new_table_2.add_row([0.3*10**10,1,2])
    add_table=new_table+new_table_2
    print(add_table)
    print(new_table)
def test_get_item():
    """Tests the __add__ method"""
    options={"column_names":["Frequency","b","c"],"column_names_delimiter":",","data":[[0.1*10**10,1,2],[2*10**10,3,4]],"data_delimiter":'\t',
             "header":['Hello There',"My Darling"],"column_names_begin_token":'#',"comment_begin":'!',
             "comment_end":"\n",
             "directory":TESTS_DIRECTORY,
             "column_units":["Hz",None,None],
             "column_descriptions":["Frequency in Hz",None,None],
             "column_types":['float','float','float'],
             "row_formatter_string":"{0:.2e}{delimiter}{1}{delimiter}{2}",
             "treat_header_as_comment":True}
    new_table=AsciiDataTable(None,**options)



    print(new_table["Frequency"])
    print(new_table[("Frequency",1)])
    print(new_table[["Frequency","c"]])

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    test_AsciiDataTable()
    test_open_existing_AsciiDataTable()
    test_AsciiDataTable_equality()
    test_inline_comments()
    test_add_row()
    test_add_index()
    show_structure_script()
    #test_save_schema()
    #test_read_schema()
    test_change_unit_prefix()
    test_add_column()
    test_AsciiDataTable_get_column_and_getitem()
    test_copy_method()
    test_add_method()
    test_get_item()
