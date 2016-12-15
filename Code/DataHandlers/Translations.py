#-----------------------------------------------------------------------------
# Name:        Translations
# Purpose:     To translate from one data form to another
# Author:      Aric Sanders
# Created:     3/3/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Translations.py holds the functions that map from one form to another.
Warning!!! The functions defined in this module break from normal naming practices to better
reflect their purpose. A translation from one object or file takes the form UpperCamelCase_to_UpperCamelCase
This change is meant to make consistent node names for graph models found in
pyMeasure.Code.DataHandlers.GraphModels. Normal naming rules about
 HTML and XML abbreviations are not followed. (XmlList not XMLList)
 All types that end with File are on-disk file types,
composite types are denoted by ending the UpperCamelCase name with a full english version of the python
class name, such as DataFrameDictionary or DataFrameList"""

#-----------------------------------------------------------------------------
# Standard Imports
import timeit
import os
import sys
import json
import subprocess
import base64
import StringIO
import cStringIO
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.GeneralModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.GeneralModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.XMLModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.XMLModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.NISTModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.NISTModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.TouchstoneModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.TouchstoneModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.DataHandlers.StatistiCALModels import *
except:
    print("The module pyMeasure.Code.DataHandlers.StatistiCALModels was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    import pandas
except:
    print("The module pandas was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    import odo
except:
    print("The module odo was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    import PIL
except:
    print("The module PIL was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    import pdfkit
except:
    print("The module pdfkit was not found or had an error,"
          "please check module or put it on the python path use pip install pdfkit and also install "
          "wkhtmltopdf")
    raise ImportError
try:
    from scipy import misc
except:
    print("The module scipy.misc was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from scipy.io import savemat,loadmat
except:
    print("The module scipy.io was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from win32com import client
    WINDOWS_COM=True
except:
    print("The module win32com was not found or had an error,"
          "please check module or put it on the python path")
    WINDOWS_COM=False
    #raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
INKSCAPE_PATH=r'c:\PROGRA~1\Inkscape\inkscape.exe'
#-----------------------------------------------------------------------------
# Module Functions
# todo: rename all translations as UpperCamelCase_to_UpperCamelCase
def String_to_StringList(string):
    """Converts a string to a list of strings using splitlines"""
    string_list=string.splitlines()
    return string_list

def StringList_to_String(string_list):
    """Collapses a list of strings to a single list"""
    out_string=string_list_collapse(string_list)
    return out_string

def File_to_String(file_name):
    """Opens a file and returns the contents as a string"""
    in_file=open(file_name,'r')
    out_string=in_file.read()
    in_file.close()
    return out_string

def String_to_File(string,file_name="test"):
    """Saves a string as a file"""
    out_file=open(file_name,'w')
    out_file.write(string)
    out_file.close()
    return file_name
def StringList_to_File(string_list,file_name="test"):
    """Saves a string list as a file"""
    out_file=open(file_name,"w")
    for line in string_list:
        out_file.write(line)
    out_file.close()
    return file_name
def String_to_StringIo(string):
    """Converts a string to a StringIO.StringIO object"""
    return StringIO.StringIO(string)
def StringIo_to_String(string_io_object):
    """Converts a StringIO.StringIO object to a string """
    return string_io_object.getvalue()
def String_to_CStringIo(string):
    """Converts a string to a StringIO.StringIO object"""
    return cStringIO.StringIO(string)
def CStringIo_to_String(string_io_object):
    """Converts a StringIO.StringIO object to a string """
    return string_io_object.getvalue()
def AsciiDataTable_to_XmlDataTable(ascii_data_table,**options):
    """Takes an AsciiDataTable and returns a XmlDataTable with **options"""
    defaults={"specific_descriptor":ascii_data_table.options["specific_descriptor"],
                     "general_descriptor":ascii_data_table.options["general_descriptor"],
                      "directory":ascii_data_table.options["directory"],
              "style_sheet":"../XSL/ONE_PORT_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    # Todo: Clean this up so the AsciiDataTable.column_names always goes to an XML attribute that is properly named
    for index,column_name in enumerate(ascii_data_table.column_names[:]):
        ascii_data_table.column_names[index]=column_name.replace("*","_times_").replace("/","_div_").replace("(","_").replace(")","_").replace("-","_")

    data_description={}
    if ascii_data_table.options["column_descriptions"] is not None:
        if type(ascii_data_table.options["column_descriptions"]) is DictionaryType:
            for key,value in ascii_data_table.options["column_descriptions"].iteritems():
                data_description[key]=value
        elif type(ascii_data_table.options["column_descriptions"]) is ListType:
            for index,value in enumerate(ascii_data_table.options["column_descriptions"]):
                key=ascii_data_table.column_names[index]
                data_description[key]=value

    if ascii_data_table.metadata is not None:
        for key,value in ascii_data_table.metadata.iteritems():
            data_description[key]=value
    else:
        if ascii_data_table.header is not None:
            for index,line in enumerate(ascii_data_table.header):
                key="Header_{0:0>3}".format(index)
                data_description[key]=line
        if ascii_data_table.footer is not None:
            for index,line in enumerate(ascii_data_table.footer):
                key="Footer_{0:0>3}".format(index)
                data_description[key]=line
    data_dictionary={"Data_Description":data_description,"Data":ascii_data_table.get_data_dictionary_list()}
    XML_options["data_dictionary"]=data_dictionary
    new_xml_data_table=DataTable(None,**XML_options)
    return new_xml_data_table

def XmlBase_to_XsltResultString(xml_model,**options):
    """Uses the xml_model's to_HTML method to return a HTML string"""
    defaults={"style_sheet":os.path.join(TESTS_DIRECTORY,XSLT_REPOSITORY,"DEFAULT_STYLE.xsl")}
    transform_options={}
    for key,value in defaults.iteritems():
        transform_options[key]=value
    for key,value in options.iteritems():
        transform_options[key]=value
    return xml_model.to_HTML(**transform_options)

def XmlBase_to_XsltResultFile(xml_model,**options):
    """Uses the xml_model's save_HTML method to return a HTML file"""
    defaults={"style_sheet":os.path.join(TESTS_DIRECTORY,XSLT_REPOSITORY,"DEFAULT_STYLE.xsl"),
              "file_path":"test.xml"}
    transform_options={}
    for key,value in defaults.iteritems():
        transform_options[key]=value
    for key,value in options.iteritems():
        transform_options[key]=value
    xml_model.save_HTML(XSLT=transform_options["style_sheet"],file_path=transform_options["file_path"])
    return transform_options["file_path"]

def AsciiDataTable_to_DataFrame(ascii_data_table):
    """Converts an AsciiDataTable to a pandas.DataFrame
    discarding any header or footer information"""
    data_frame=pandas.DataFrame(data=ascii_data_table.data,columns=ascii_data_table.column_names)
    return data_frame

def AsciiDataTable_to_DataFrameDictionary(AsciiDataTable):
    """Converts an AsciiDataTable to a dictionary of pandas.DataFrame s"""
    output_dict={}
    for element in AsciiDataTable.elements:
        #print("{0} is {1}".format('element',element))
        if AsciiDataTable.__dict__[element]:
            if re.search('header',element,re.IGNORECASE):
                header_table=pandas.DataFrame(AsciiDataTable.header,columns=["Header_Line_Content"])
                output_dict["Header"]=header_table
            # needs to be before data search
            elif re.search('meta',element,re.IGNORECASE):
                #print("{0} is {1}".format('element',element))
                metadata_table=pandas.DataFrame([[key,value] for key,value in AsciiDataTable.metadata.iteritems()],
                                columns=["Property","Value"])
                output_dict["Metadata"]=metadata_table
            elif re.search('data|^meta',element,re.IGNORECASE):

                data_table=pandas.DataFrame(AsciiDataTable.data,columns=AsciiDataTable.column_names)
                output_dict["Data"]=data_table

            elif re.search('footer',element,re.IGNORECASE):
                footer_table=pandas.DataFrame(AsciiDataTable.footer,columns=["Footer_Line_Content"])
                output_dict["Footer"]=footer_table

            elif re.search('comment',element,re.IGNORECASE):
                comments=AsciiDataTable.__dict__[element]
                inline_comments=pandas.DataFrame(comments,columns=["Comment","Line","Location"])
                output_dict["Comments"]=inline_comments
    return output_dict

def DataFrameDictionary_to_ExcelFile(DataFrame_dict,excel_file_name="Test.xlsx"):
    """Converts a dictionary of pandas DataFrames to a single excel file with sheet names
    determined by keys"""
    # sort the keys so that they will display in the same order
    writer = pandas.ExcelWriter(excel_file_name)
    keys=sorted(DataFrame_dict.keys())
    for key in keys:
        #print key
        DataFrame_dict[key].to_excel(writer,sheet_name=key,index=False)
        writer.close()
    return excel_file_name

def ExcelFile_to_DataFrameDictionary(excel_file_name):
    """Reads an excel file into a dictionary of data frames"""
    data_frame_dictionary=pandas.read_excel(excel_file_name,sheetname=None)
    return data_frame_dictionary

def DataFrame_to_AsciiDataTable(pandas_data_frame,**options):
    """Converts a pandas.DataFrame to an AsciiDataTable"""
    # Set up defaults and pass options
    defaults={}
    conversion_options={}
    for key,value in defaults.iteritems():
        conversion_options[key]=value
    for key,value in options.iteritems():
        conversion_options[key]=value

    conversion_options["column_names"]=pandas_data_frame.columns.tolist()[:]
    conversion_options["data"]=pandas_data_frame.as_matrix().tolist()[:]
    conversion_options["column_types"]=map(lambda x:str(x),pandas_data_frame.dtypes.tolist()[:])

    new_table=AsciiDataTable(None,**conversion_options)
    return new_table

def AsciiDataTable_to_ExcelFile(ascii_data_table,file_path=None):
    """Converts an AsciiDataTable to an excel spreadsheet using pandas"""
    if ascii_data_table.header:
        data_frame=pandas.DataFrame(data=ascii_data_table.data,columns=ascii_data_table.column_names,index=False)

def S2PV1_to_XmlDataTable(s2p,**options):
    """Transforms a s2p's sparameters to a XmlDataTable. Converts the format to #GHz DB first"""
    defaults={"specific_descriptor":s2p.options["specific_descriptor"],
                     "general_descriptor":s2p.options["general_descriptor"],
                      "directory":s2p.options["directory"],
              "style_sheet":"../XSL/S2P_DB_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    data_description={}
    if s2p.options["column_descriptions"] is not None:
        for key,value in s2p.options["column_descriptions"].iteritems():
            data_description[key]=value
    if s2p.metadata is not None:
        for key,value in s2p.metadata.iteritems():
            data_description[key]=value
    else:
        if s2p.comments is not None:
            for index,line in enumerate(s2p.comments):
                key="Comments_{0:0>3}".format(index)
                data_description[key]=line[0]
    s2p.change_data_format(new_format='DB')
    s2p.change_frequency_units('GHz')
    data_dictionary={"Data_Description":data_description,"Data":s2p.get_data_dictionary_list()}
    XML_options["data_dictionary"]=data_dictionary
    new_xml_data_table=DataTable(None,**XML_options)
    return new_xml_data_table

def SNP_to_XmlDataTable(snp,**options):
    """Transforms a snp's sparameters to a XmlDataTable. Converts the format to #GHz DB first"""
    defaults={"specific_descriptor":snp.options["specific_descriptor"],
                     "general_descriptor":snp.options["general_descriptor"],
                      "directory":snp.options["directory"],
              "style_sheet":"../XSL/DEFAULT_MEASUREMENT_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    data_description={}
    if snp.options["column_descriptions"] is not None:
        for key,value in snp.options["column_descriptions"].iteritems():
            data_description[key]=value
    if snp.metadata is not None:
        for key,value in snp.metadata.iteritems():
            data_description[key]=value
    else:
        if snp.comments is not None:
            for index,line in enumerate(snp.comments):
                key="Comments_{0:0>3}".format(index)
                data_description[key]=line[0]
    snp.change_data_format(new_format='RI')
    snp.change_frequency_units('GHz')
    data_dictionary={"Data_Description":data_description,"Data":snp.get_data_dictionary_list()}
    XML_options["data_dictionary"]=data_dictionary
    new_xml_data_table=DataTable(None,**XML_options)
    return new_xml_data_table

def S1PV1_to_XmlDataTable(s1p,**options):
    """Transforms a s1p's sparameters to a XmlDataTable. Converts the format to RI first"""
    defaults={"specific_descriptor":s1p.options["specific_descriptor"],
                     "general_descriptor":s1p.options["general_descriptor"],
                      "directory":s1p.options["directory"],
              "style_sheet":"../XSL/S1P_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    data_description={}
    if s1p.options["column_descriptions"] is not None:
        for key,value in s1p.options["column_descriptions"].iteritems():
            data_description[key]=value
    if s1p.metadata is not None:
        for key,value in s1p.metadata.iteritems():
            data_description[key]=value
    else:
        if s1p.comments is not None:
            for index,line in enumerate(s1p.comments):
                key="Comments_{0:0>3}".format(index)
                data_description[key]=line[0]
    s1p.change_data_format(new_format='RI')
    s1p.change_frequency_units('GHz')
    data_dictionary={"Data_Description":data_description,"Data":s1p.get_data_dictionary_list()}
    XML_options["data_dictionary"]=data_dictionary
    new_xml_data_table=DataTable(None,**XML_options)
    return new_xml_data_table

def TwoPortCalrepModel_to_XmlDataTable(two_port_calrep_table,**options):
    """Converts the 2-port calrep model to xml"""
    table=two_port_calrep_table.joined_table
    defaults={"specific_descriptor":table.options["specific_descriptor"],
                     "general_descriptor":table.options["general_descriptor"],
                      "directory":table.options["directory"],
              "style_sheet":"../XSL/TWO_PORT_CALREP_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    new_xml=AsciiDataTable_to_XmlDataTable(table,**XML_options)
    return new_xml

def TwoPortCalrepModel_to_S2PV1(two_port_calrep_table,**options):
    """Transforms a TwoPortRawModel  to S2PV1"""
    table=two_port_calrep_table
    path=table.path.split('.')[0]+".s2p"
    data=[[row["Frequency"],row["magS11"],row["argS11"],row["magS21"],row["argS21"],row["magS21"],
           row["argS21"],row["magS22"],row["argS22"]] for row in table.joined_table.get_data_dictionary_list()]
    comments=[[line,index,0] for index,line in enumerate(table.joined_table.header[:])]
    s2p_options={"option_line":"# GHz S MA R 50","data":data,
                 "comments":comments,"path":path,"option_line_line":len(table.joined_table.header),
                 "sparameter_begin_line":len(table.joined_table.header)+1,"column_names":S2P_MA_COLUMN_NAMES}
    s2p_file=S2PV1(None,**s2p_options)
    return s2p_file

def OnePortCalrep_to_XmlDataTable(one_port_calrep_table,**options):
    """Converts the 1-port calrep model to xml"""
    table=one_port_calrep_table
    defaults={"specific_descriptor":table.options["specific_descriptor"],
                     "general_descriptor":table.options["general_descriptor"],
                      "directory":table.options["directory"],
              "style_sheet":"../XSL/ONE_PORT_CALREP_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    new_xml=AsciiDataTable_to_XmlDataTable(table,**XML_options)
    return new_xml

def TwoPortRawModel_to_XmlDataTable(two_port_raw_table,**options):
    """Converts the 2-port raw model used by s-parameters to xml"""
    table=two_port_raw_table
    defaults={"specific_descriptor":table.options["specific_descriptor"],
                     "general_descriptor":table.options["general_descriptor"],
                      "directory":table.options["directory"],
              "style_sheet":"../XSL/TWO_PORT_RAW_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    new_xml=AsciiDataTable_to_XmlDataTable(table,**XML_options)
    return new_xml

def TwoPortRawModel_to_S2PV1(two_port_raw_table,**options):
    """Transforms a TwoPortRawModel  to S2PV1"""
    table=two_port_raw_table
    path=table.path.split('.')[0]+".s2p"
    data=[[row[0],row[3],row[4],row[5],row[6],row[5],row[6],row[7],row[8]] for row in table.data]
    comments=[[line,index,0] for index,line in enumerate(table.header[:])]
    s2p_options={"option_line":"# GHz S MA R 50","data":data,
                 "comments":comments,"path":path,"option_line_line":len(table.header),
                 "sparameter_begin_line":len(table.header)+1,"column_names":S2P_MA_COLUMN_NAMES}
    s2p_file=S2PV1(None,**s2p_options)
    return s2p_file

def JBSparameter_to_S2PV1(jb_model,**options):
    """Transforms a JBSparameter file to S2PV1 """
    table=jb_model
    path=table.path.split('.')[0]+".s2p"
    old_prefix=table.get_frequency_units().replace('Hz','')
    table.change_unit_prefix(column_selector=0,old_prefix=old_prefix,new_prefix='G',unit='Hz')
    data=table.data[:]
    comments=[[line,index,0] for index,line in enumerate(table.header[:])]
    s2p_options={"option_line":"# GHz S RI R 50","data":data,
                 "comments":comments,"path":path,"option_line_line":len(table.header),
                 "sparameter_begin_line":len(table.header)+1,"column_names":S2P_RI_COLUMN_NAMES}
    s2p_file=S2PV1(None,**s2p_options)
    return s2p_file

def PowerRawModel_to_XmlDataTable(power_raw_table,**options):
    """Converts the 2-port raw model used by s-parameters to xml"""
    table=power_raw_table
    defaults={"specific_descriptor":table.options["specific_descriptor"],
                     "general_descriptor":table.options["general_descriptor"],
                      "directory":table.options["directory"],
              "style_sheet":"../XSL/POWER_RAW_STYLE.xsl"
                     }
    XML_options={}
    for key,value in defaults.iteritems():
        XML_options[key]=value
    for key,value in options.iteritems():
        XML_options[key]=value
    new_xml=AsciiDataTable_to_XmlDataTable(table,**XML_options)
    return new_xml
# Table Translations
def DataFrame_to_HdfFile(pandas_data_frame,hdf_file_name="test.hdf"):
    """Saves a DataFrame as an HDF File, returns the file name"""
    pandas_data_frame.to_hdf(hdf_file_name,"table")
    return hdf_file_name

def HdfFile_to_DataFrame(hdf_file_name):
    """Opens a HDF with a Group named table and creates a pandas.DataFrame"""
    pandas_data_frame=pandas.read_hdf(hdf_file_name,"table")
    return pandas_data_frame

def XmlDataTable_to_AsciiDataTable(xml_table):
    """Turns A XMLData to AsciiDataTable table without preserving Metadata"""
    table=AsciiDataTable(None,
                         column_names=xml_table.attribute_names,
                         data=xml_table.data)
    return table

# def AsciiDataTable_to_XmlDataTable_2(data_table):
#     xml=AsciiDataTable_to_XmlDataTable(data_table)
#     return xml

def DataFrame_to_ExcelFile(pandas_data_frame,file_name="Test.xlsx"):
    pandas_data_frame.to_excel(file_name,index=False)
    return file_name

def ExcelFile_to_DataFrame(excel_file_name):
    df=pandas.read_excel(excel_file_name)
    return df

def DataFrame_to_HtmlString(pandas_data_frame):
    html=pandas_data_frame.to_html(index=False)
    return html

def HtmlString_to_DataFrame(html_string):
    list_df=pandas.read_html(html_string)
    return list_df[0]

def DataFrame_to_JsonFile(pandas_data_frame,file_name="test.json"):
    json=pandas_data_frame.to_json(file_name,orient='records')
    return file_name

def JsonFile_to_DataFrame(json_file_name):
    data_frame=pandas.read_json(json_file_name,orient='records')
    return data_frame

def DataFrame_to_JsonString(pandas_data_frame):
    json=pandas_data_frame.to_json(orient='records')
    return json

def JsonString_to_DataFrame(json_string):
    data_frame=pandas.read_json(json_string,orient='records')
    return data_frame

def DataFrame_to_CsvFile(pandas_data_frame,file_name="test.csv"):
    csv=pandas_data_frame.to_csv(file_name,index=False)
    return file_name

def CsvFile_to_DataFrame(csv_file_name):
    data_frame=pandas.read_csv(csv_file_name)
    return data_frame

def AsciiDataTable_to_MatFile(ascii_data_table,file_name="test.mat"):
    matlab_data_dictionary={"data":ascii_data_table.data,"column_names":ascii_data_table.column_names}
    savemat(file_name,matlab_data_dictionary)
    return file_name

def MatFile_to_AsciiDataTable(matlab_file_name):
    matlab_data_dictionary=loadmat(matlab_file_name)
    ascii_data_table=AsciiDataTable(None,
                                    column_names=map(lambda x: x.rstrip().lstrip(),
                                                     matlab_data_dictionary["column_names"].tolist()),
                                     data=matlab_data_dictionary["data"].tolist())
    return ascii_data_table

def XmlDataTable_to_XmlFile(xml_data_table,file_name="test.xml"):
    xml_data_table.save(file_name)
    return file_name

def XmlFile_to_XmlDataTable(xml_file_name):
    xml_data_table=DataTable(xml_file_name)
    return xml_data_table

def HtmlString_to_HtmlFile(html_string,file_name="test.html"):
    out_file=open(file_name,'w')
    out_file.write(html_string)
    out_file.close()
    return file_name
# this is broken, something does not work properly
def HtmlFile_to_DataFrame(html_file_name):
    in_file=open(html_file_name,'r')
    pandas_data_frame=pandas.read_html(in_file)
    return pandas_data_frame

def HtmlFile_to_HtmlString(html_file_name):
    in_file=open(html_file_name,'r')
    html_string=in_file.read()
    return html_string

def DataFrame_to_HtmlFile(pandas_data_frame,file_name="test.html"):
    out_file=open(file_name,'w')
    pandas_data_frame.to_html(out_file,index=False)
    return file_name

def HtmlFile_to_PdfFile(html_file_name,pdf_file_name="test.pdf"):
    """Takes an html page and converts it to pdf using wkhtmltopdf and pdfkit"""
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_file(html_file_name,pdf_file_name,configuration=config)
    return pdf_file_name

def HtmlString_to_PdfFile(html_string,pdf_file_name="test.pdf"):
    """Takes an html string and converts it to pdf using wkhtmltopdf and pdfkit"""
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html_string,pdf_file_name,configuration=config)
    return pdf_file_name

def JsonFile_to_XmlDataTable(json_file_name):
    data_dictionary_list=json.load(open(json_file_name,'r'))
    xml=DataTable(None,data_dictionary={"data":data_dictionary_list})
    return xml

def CsvFile_to_AsciiDataTable(csv_file_name):
    options={"column_names_begin_line":0,"column_names_end_line":1,
             "data_begin_line":1,"data_end_line":-1,"data_delimiter":",","column_names_delimiter":","}
    table=AsciiDataTable(csv_file_name,**options)
    return table

# Image Translations
def PngFile_to_JpgFile(png_file_name):
    [root_name,extension]=png_file_name.split(".")
    jpeg_file_name=root_name+".jpg"
    PIL.Image.open(png_file_name).save(jpeg_file_name)
    return jpeg_file_name

def File_to_Image(file_path):
    new_image=PIL.Image.open(file_path)
    if re.search(".gif",file_path,re.IGNORECASE):
        new_image=new_image.convert("RGB")
    return new_image

def Image_to_File(pil_image,file_path=None):
    if file_path is None:
        file_path=pil_image.filename
    pil_image.save(file_path)
    return file_path

def Image_to_FileType(pil_image,file_path=None,extension="png"):

    if file_path is None:
        file_path=pil_image.filename
    root_name=file_path.split(".")[0]
    new_file_name=root_name+"."+extension.replace(".","")
    if re.search('jp|bmp',extension,re.IGNORECASE):
        pil_image.convert('RGB')
    print("{0} is {1}".format("pil_image.mode",pil_image.mode))
    pil_image.save(new_file_name)
    return new_file_name

def Image_to_ThumbnailFile(pil_image,file_path="thumbnail.jpg"):
    size = (64, 64)
    temp_image=pil_image.copy()
    temp_image.thumbnail(size)
    temp_image.save(file_path)
    return file_path

def PngFile_to_Base64(file_name):
    in_file=open(file_name, "rb")
    encoded=base64.b64encode(in_file.read())
    return encoded

def Base64_to_PngFile(base64_encoded_png,file_name="test.png"):
    out_file=open(file_name, "wb")
    decoded=base64.b64decode(base64_encoded_png)
    out_file.write(decoded)
    out_file.close()
    return file_name


def PngFile_to_Ndarray(file_name):
    nd_array=misc.imread(file_name)
    return nd_array

def Ndarray_to_PngFile(nd_array,file_name="test.png"):
    misc.imsave(file_name,nd_array)
    return file_name

# change this to base64png
def Base64Png_to_EmbeddedHtmlString(base64_encoded_png):
    html_string="<img src='data:image/png;base64,{0}' />".format(base64_encoded_png)
    return html_string

def EmbeddedHtmlString_to_Base64Png(html_string):
    pattern=re.compile("<img src='data:image/png;base64,(?P<data>.+)' />")
    match=re.search(pattern,html_string)
    if match:
        encoded=match.groupdict()["data"]
    else:
        raise
    return encoded

def Ndarray_to_Matplotlib(nd_array):
    figure=plt.imshow(nd_array)
    figure.axes.get_xaxis().set_visible(False)
    figure.axes.get_yaxis().set_visible(False)
    plt.show()

def Ndarray_to_MatplotlibFigure(nd_array):
    plt.close()
    figure=plt.figure("Image",frameon=False)
    plt.figimage(nd_array,resize=True)
    return figure

def MatplotlibFigure_to_File(figure,file_name):
    """Saves the figure to file name"""
    figure.savefig(file_name,bbox_inches='tight', pad_inches=.1,dpi="figure")
    return file_name

def MatplotlibFigure_to_PngFile(figure,file_name="test.png"):
    figure.savefig(file_name,bbox_inches='tight', pad_inches=.1,dpi="figure")
    return file_name

def MatplotlibFigure_to_SvgFile(figure,file_name="test.svg"):
    figure.savefig(file_name,bbox_inches='tight', pad_inches=.1,dpi="figure")
    return file_name

# Transformations that use Inkscape
# Todo: put an error handler and a message about InkScape path
def SvgFile_to_PngFile(svg_file_path,export_file_path="test.png"):
    """Uses Inkscape to convert SVG to png via commandline """
    p=subprocess.call([INKSCAPE_PATH,svg_file_path,
                       '--export-png',export_file_path])
    return export_file_path

def SvgFile_to_EpsFile(svg_file_path,export_file_path="test.eps"):
    """Uses Inkscape to convert SVG to Eps via commandline """
    p=subprocess.call([INKSCAPE_PATH,svg_file_path,
                       '--export-eps',export_file_path])
    return export_file_path

def SvgFile_to_PdfFile(svg_file_path,export_file_path="test.pdf"):
    """Uses Inkscape to convert SVG to pdf via commandline """
    p=subprocess.call([INKSCAPE_PATH,svg_file_path,
                       '--export-pdf',export_file_path])
    return export_file_path

# Matlab Figure Translation
def FigFile_to_MatplotlibFigure(filename,fignr=1):
    "Function that uses loadmat to create a matplotlib plot of a matlab fig file"
    from scipy.io import loadmat
    from numpy import size
    from matplotlib.pyplot import plot,figure,hold,xlabel,ylabel,show,clf,xlim,legend
    d = loadmat(filename,squeeze_me=True, struct_as_record=False)
    ax1 = d['hgS_070000'].children
    if size(ax1) > 1:
        legs= ax1[1]
        ax1 = ax1[0]
    else:
        legs=0
    figure(fignr)
    clf()
    hold(True)
    counter = 0
    for line in ax1.children:
        if line.type == 'graph2d.lineseries':
            if hasattr(line.properties,'Marker'):
                mark = "%s" % line.properties.Marker
                mark = mark[0]
            else:
                mark = '.'
            if hasattr(line.properties,'LineStyle'):
                linestyle = "%s" % line.properties.LineStyle
            else:
                linestyle = '-'
            if hasattr(line.properties,'Color'):
                r,g,b =  line.properties.Color
            else:
                r = 0
                g = 0
                b = 1
            if hasattr(line.properties,'MarkerSize'):
                marker_size = line.properties.MarkerSize
            else:
                marker_size = 1
            x = line.properties.XData
            y = line.properties.YData
            plot(x,y,marker=mark,linestyle=linestyle,color=(r,g,b),markersize=marker_size)
        elif line.type == 'text':
            if counter <1:
                #print(dir(line.properties))
                counter += 1
            elif counter < 2:
                #print dir(line.properties.String)
                xlabel("%s" % line.properties.String,fontsize = 16)
                counter += 1
            elif counter < 3:
                #print dir(line.properties.String)
                ylabel("%s" % line.properties.String,fontsize = 16)
                counter += 1
    xlim(ax1.properties.XLim)
    if legs:
        leg_entries = tuple(legs.properties.String)
        py_locs = ['upper center','lower center','right','left','upper right','upper left','lower right','lower left','best']
        MAT_locs=['North','South','East','West','NorthEast', 'NorthWest', 'SouthEast', 'SouthWest','Best']
        Mat2py = dict(zip(MAT_locs,py_locs))
        location = legs.properties.Location
        legend(leg_entries,loc=Mat2py[location])
    hold(False)
    show()

# Metadata Translations
def replace_None(string):
    """Replaces the string 'None' with the python value None"""
    if string:
        if re.match("None",string):
            return None
        else:
            return string
    else:
        return string

def Dictionary_to_JsonString(python_dictionary):
    """Uses json module to create a json string from a python dictionary"""
    return json.dumps(python_dictionary)

def JsonString_to_Dictionary(json_string):
    """Uses json module to return a python dictionary"""
    out_dictionary=json.loads(json_string)
    for key,value in out_dictionary.iteritems():
        out_dictionary[key]=replace_None(value)
    return out_dictionary

def JsonString_to_JsonFile(json_string,file_name="test.json"):
    out_file=open(file_name,'w')
    out_file.write(json_string)
    out_file.close()
    return file_name

def JsonFile_to_JsonString(json_file_name):
    in_file=open(json_file_name,'r')
    json_string=in_file.read()
    in_file.close()
    return json_string



def Dictionary_to_XmlString(dictionary=None,char_between='\n'):
    string_output=''
    for key,value in dictionary.iteritems():
        xml_open="<"+str(key)+">"
        xml_close="</"+str(key)+">"
        string_output=string_output+xml_open+str(value)+xml_close+char_between
    return string_output

def XmlString_to_Dictionary(xml_string):
    """XML string must be in the format <key>value</key>\n<key2>.. to work"""
    pattern='<(?P<XML_tag>.+)>(?P<XML_text>.+)</.+>'
    lines=xml_string.splitlines()
    out_dictionary={}
    for line in lines:
        match=re.search(pattern,line)
        if match:
            key=match.groupdict()["XML_tag"].rstrip().lstrip().replace("\'","")
            value=match.groupdict()["XML_text"].rstrip().lstrip().replace("\'","")
            out_dictionary[key]=value
    return out_dictionary


def Dictionary_to_HtmlMetaString(python_dictionary):
    """Converts a python dictionary to meta tags for html"""
    out_string=""
    for key,value in python_dictionary.iteritems():
        out_string=out_string+"<meta name="+'"{0}"'.format(key)+" content="+'"{0}"'.format(value)+" />\n"
    return out_string

def HtmlMetaString_to_Dictionary(HTML_meta_tags_string):
    """Converts a python dictionary to meta tags for html"""
    pattern='<meta name="(?P<key>.+)" content="(?P<value>.+)" />'
    lines=HTML_meta_tags_string.splitlines()
    out_dictionary={}
    for line in lines:
        match=re.search(pattern,line)
        if match:
            key=match.groupdict()["key"]
            value=match.groupdict()["value"]
            out_dictionary[key]=value
    return out_dictionary

def Dictionary_to_XmlTupleString(python_dictionary):
    """transforms a python dictionary into a xml line in the form
    <Tuple key1="value1" key2="value2"..keyN="valueN" />"""
    prefix="<Tuple "
    postfix=" />"
    inner=""
    for key,value in python_dictionary.iteritems():
        inner=inner+'{0}="{1}" ' .format(key,value)
        xml_out=prefix+inner+postfix
    return xml_out

def XmlTupleString_to_Dictionary(tuple_line):
    """Takes a line in the form of <Tuple key1="value1" key2="Value2" ...KeyN="ValueN" />
    and returns a dictionary"""
    stripped_string=tuple_line.replace("<Tuple","")
    stripped_string=stripped_string.replace("/>","")
    pattern="(?<=\")(?<!,|:)\s+(?!,+)"
    lines=re.split(pattern,stripped_string)
    out_dictionary={}
    for line in lines:
        split_line=line.split("=")
        print split_line
        if len(split_line)==2:
            key=split_line[0].rstrip().lstrip().replace("\"","")
            value=split_line[1].rstrip().lstrip().replace("\"","")
            out_dictionary[key]=value
    return out_dictionary

def Dictionary_to_PickleFile(python_dictionary,file_name="dictionary.pkl"):
    """Python Dictionary to pickled file"""
    pickle.dump(python_dictionary,open(file_name,'wb'))
    return file_name

def PickleFile_to_Dictionary(pickle_file_name):
    """open and read a pickled file with only a single python dictionary in it"""
    dictionary_out=pickle.load(open(pickle_file_name,'rb'))
    return dictionary_out

def Dictionary_to_ListList(python_dictionary):
    """Returns a list with two lists : [[key_list][item_list]]"""
    key_list=[]
    value_list=[]
    for key,value in python_dictionary.iteritems():
        key_list.append(key)
        value_list.append(value)
    out_list=[key_list,value_list]
    return out_list

def ListList_to_Dictionary(list_list):
    """takes a list of [[keys],[items]] and returns a dictionary """
    keys=list_list[0]
    items=list_list[1]
    out_dictionary={}
    for index,key in enumerate(keys):
        out_dictionary[key]=items[index]
    return out_dictionary

def Dictionary_to_DataFrame(python_dictionary):
    """Takes a python dictionary and maps it to a pandas dataframe"""
    data_frame=pandas.DataFrame([[key,value] for key,value in python_dictionary.iteritems()],
                                columns=["Property","Value"])
    data_frame.fillna("None")
    return data_frame

def DataFrame_to_Dictionary(pandas_data_frame):
    """Takes a pandas.DataFrame with column names ["Property","Value"] and returns a python dictionary"""
    list_of_lists=pandas_data_frame.as_matrix().tolist()
    dictionary={row[0]:replace_None(row[1]) for row in list_of_lists}
    return dictionary

def Dictionary_to_HeaderList(python_dictionary):
    "Converts a python dictionary to a list of strings in the form ['key1=value1',..'keyN=valueN']"
    out_string=""
    out_list=[]
    for key,value in python_dictionary.iteritems():
        out_string="{0}={1}".format(key,value)
        out_list.append(out_string)
    return out_list

def HeaderList_to_Dictionary(header_list):
    "Creates a python dictionary from a list of strings in the form ['key1=value1',..'keyN=valueN']"
    out_dictionary={}
    for item in header_list:
        key_value_list=item.split("=")
        key=key_value_list[0].rstrip().lstrip()
        value=key_value_list[1].rstrip().lstrip()
        out_dictionary[key]=value
    return out_dictionary


def MatFile_to_AsciiDataTableKeyValue(matlab_file_name):
    matlab_data_dictionary=loadmat(matlab_file_name)
    #print matlab_data_dictionary
    data=[map(lambda x: x.rstrip().lstrip(),row) for row in matlab_data_dictionary["data"].tolist()]
    column_names=map(lambda x: x.rstrip().lstrip(), matlab_data_dictionary["column_names"].tolist())
    ascii_data_table=AsciiDataTable(None,column_names=column_names,data=data)
    return ascii_data_table
# Word Translations Warning COM interface can be very unreliable
if WINDOWS_COM:
    def DocFile_to_PdfFile(doc_file_name,pdf_file_name="test.pdf"):
        """Converts a microsoft doc or docx file to a pdf using word.
        Requires word and win32com to be installed.
        FileFormat=17 is pdf for SaveAs, search for WdSaveFormat Enumeration to see more details.
        Returns the new file name"""
        word=client.DispatchEx("Word.Application")
        doc=word.Documents.Open(doc_file_name)
        doc.SaveAs(pdf_file_name,FileFormat=17)
        doc.Close()
        word.Quit()
        return pdf_file_name

    def DocFile_to_HtmlFile(doc_file_name,html_file_name="test.html"):
        """Converts a microsoft doc or docx file to a filtered html file using word.
        Requires word and win32com to be installed.
        FileFormat=10 is filtered html for SaveAs, search for WdSaveFormat Enumeration to see more details.
        Returns the new file name"""
        word=client.DispatchEx("Word.Application")
        doc=word.Documents.Open(doc_file_name)
        doc.SaveAs(html_file_name,FileFormat=10)
        doc.Close()
        word.Quit()
        return html_file_name

    def DocFile_to_OdtFile(doc_file_name,odt_file_name="test.odt"):
        """Converts a microsoft doc or docx file to a open document format file using word.
        Requires word and win32com to be installed.
        FileFormat=23 is odt for SaveAs, search for WdSaveFormat Enumeration to see more details.
        This one required guessing at the integer value.
        Returns the new file name"""
        word=client.DispatchEx("Word.Application")
        doc=word.Documents.Open(doc_file_name)
        doc.SaveAs(odt_file_name,FileFormat=23)
        doc.Close()
        word.Quit()
        return odt_file_name

    def ExcelFile_to_OdsFile(excel_file_name,ods_file_name="test.ods"):
        """Converts a microsoft xlsx or xls file to a open document spreadsheet file using excel.
        Requires word and win32com to be installed.
        FileFormat=60 is ods for SaveAs, search for XlFileFormat Enumeration to see more details.
        Returns the new file name"""
        excel=client.DispatchEx("Excel.Application")
        workbook=excel.Workbooks.Open(excel_file_name)
        workbook.SaveAs(ods_file_name,FileFormat=60)
        workbook.Close()
        excel.Quit()
        return ods_file_name

    def OdsFile_to_ExcelFile(ods_file_name,excel_file_name="test.xlsx"):
        """Converts a microsoft doc or docx file to a open document format file using excel.
        Requires word and win32com to be installed.
        FileFormat=51 is Workbook default for SaveAs, search for XlFileFormat Enumeration to see more details.
        Returns the new file name"""
        excel=client.DispatchEx("Excel.Application")
        workbook=excel.Workbooks.Open(ods_file_name)
        workbook.SaveAs(excel_file_name,FileFormat=51)
        workbook.Close()
        excel.Quit()
        return excel_file_name

    def PptxFile_to_OdpFile(power_point_file_name,odp_file_name="test.odp"):
        """Converts a pptx or ppt file to a open presentation format file using Power Point.
        Requires word and win32com to be installed.
        FileFormat=35 is odp  default for SaveAs,
        search for PowerPointFileFormat Enumeration to see more details.
        Returns the new file name"""
        power_point=client.DispatchEx("PowerPoint.Application")
        presentation=power_point.Presentations.Open(power_point_file_name)
        presentation.SaveAs(odp_file_name,FileFormat=35)
        presentation.Close()
        power_point.Quit()
        return odp_file_name

    def OdpFile_to_PptxFile(odp_file_name,power_point_file_name="test.pptx"):
        """Converts a odp  to a open pptx format file using Power Point.
        Requires word and win32com to be installed.
        FileFormat=11 is DefaultPresentation  default for SaveAs,
        search for PowerPointFileFormat Enumeration to see more details.
        Returns the new file name"""
        power_point=client.DispatchEx("PowerPoint.Application")
        presentation=power_point.Presentations.Open(odp_file_name)
        presentation.SaveAs(power_point_file_name,FileFormat=11)
        presentation.Close()
        power_point.Quit()
        return power_point_file_name
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_AsciiDataTable_to_XmlDataTable(input_file="700437.asc"):
    """Tests a one port ascii data table to an XmlDataTable transformation
    and saves the result in the tests directory. The one port file should be the output
    of Calrep7.1 or similar."""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortRawModel(input_file)
    XML_one_port=AsciiDataTable_to_XmlDataTable(one_port)
    print XML_one_port
    XML_one_port.save()
    XML_one_port.save_HTML()

def test_OnePortRaw_to_XmlDataTable(input_file="OnePortRawTestFile.txt"):
    """Tests a one port raw ascii data table to an XmlDataTable transformation
    and saves the result in the tests directory. The one port file should be the output
    of Meas HP Basic program or similar. Average time without print is 7.2 ms for 10 loops."""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortRawModel(input_file)
    options={"style_sheet":"../XSL/ONE_PORT_RAW_STYLE.xsl"}
    XML_one_port=AsciiDataTable_to_XmlDataTable(one_port,**options)
    #print XML_one_port
    XML_one_port.save()
    XML_one_port.save_HTML()

def test_StatistiCALSolutionModel_to_XmlDataTable(input_file="Solution_Plus.txt"):
    """Tests a StatistiCALSolutionModel  ascii data table to an XmlDataTable transformation
    and saves the result in the tests directory. """
    os.chdir(TESTS_DIRECTORY)
    solution=StatistiCALSolutionModel(input_file)
    options={"style_sheet":"../XSL/DEFAULT_MEASUREMENT_STYLE.xsl"}
    XML_solution=AsciiDataTable_to_XmlDataTable(solution,**options)
    print XML_solution
    XML_solution.show()
    print XML_solution.to_HTML()

def test_AsciiDataTable_to_DataFrame(input_file="700437.asc"):
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortCalrepModel(input_file)
    data_frame=AsciiDataTable_to_DataFrame(one_port)
    data_frame.to_excel('one_port.xlsx', sheet_name='Sheet1')
    #print data_frame

def test_S2P_to_XmlDataTable(file_path="thru.s2p"):
    os.chdir(TESTS_DIRECTORY)
    s2p_file=S2PV1(file_path)
    XML_s2p=S2PV1_to_XmlDataTable(s2p_file)
    XML_s2p.save()
    #print XML_s2p
def test_S1PV1_to_XmlDataTable(file_path="OnePortTouchstoneTestFile.s1p"):
    """Tests the S1PV1 to XmlDataTable translation"""
    os.chdir(TESTS_DIRECTORY)
    s1p_file=S1PV1(file_path)
    XML_s1p=S1PV1_to_XmlDataTable(s1p_file)
    XML_s1p.show()
def timeit_script(script='test_AsciiDataTable_to_XmlDataTable()',
                  setup="from __main__ import test_AsciiDataTable_to_XmlDataTable",n_loops=10):
    """Returns the mean time from running script n_loops time. To import a script, put a string
    import statement in setup"""
    print timeit.timeit(script,setup=setup,number=n_loops)/n_loops

def test_S2P_to_XmlDataTable_02(file_path="thru.s2p",**options):
    os.chdir(TESTS_DIRECTORY)
    s2p_file=S2PV1(file_path)
    XML_s2p=S2PV1_to_XmlDataTable(s2p_file,**options)
    #XML_s2p.save()

def test_TwoPortCalrep_to_XmlDataTable(file_path='922729.asc',**options):
    """Test's the conversion of the TwoPortCalrep to XmlDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortCalrepModel(file_path)
    two_port.joined_table.save()
    xml=TwoPortCalrepModel_to_XmlDataTable(two_port,**options)
    xml.save()
    xml.save_HTML()

def test_OnePortCalrep_to_XmlDataTable(file_path='700437.asc',**options):
    """Test's the conversion of the OnePortCalrep to XmlDataTable"""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortCalrepModel(file_path)
    one_port.save("ExportedOnePortCalrep.txt")
    xml=OnePortCalrep_to_XmlDataTable(one_port,**options)
    xml.save()
    xml.save_HTML()

def test_TwoPortRawModel_to_XmlDataTable(file_path='TestFileTwoPortRaw.txt',**options):
    """Test's the conversion of the TwoPorRaw to XmlDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortRawModel(file_path)
    two_port.save("SavedTest2PortRaw.txt")
    xml=TwoPortRawModel_to_XmlDataTable(two_port,**options)
    xml.save("SavedTest2PortRaw.xml")
    xml.save_HTML(file_path="SavedTest2PortRaw.html")

def test_TwoPortRawModel_to_S2PV1(file_path='TestFileTwoPortRaw.txt',**options):
    """Test's the conversion of the TwoPorRaw to XmlDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortRawModel(file_path)
    s2p=TwoPortRawModel_to_S2PV1(two_port,**options)
    print(s2p)
    s2p.save("SavedTest2PortRaw.s2p")

def test_PowerRawModel_to_XmlDataTable(file_path='CTNP15.A1_042601',**options):
    """Test's the conversion of the TwoPorRaw to XmlDataTable"""
    os.chdir(TESTS_DIRECTORY)
    power=PowerRawModel(file_path)
    print power
    xml=PowerRawModel_to_XmlDataTable(power,**options)
    xml.save("SavedTestPowerRaw.xml")
    xml.save_HTML(file_path="SavedTestPowerPortRaw.html")
def test_JBSparameter_to_S2PV1(file_path='QuartzRefExample_L1_g10_HF'):
    """Tests the conversion of JBSparameter files to S2PV1"""
    os.chdir(TESTS_DIRECTORY)
    table=JBSparameter(file_path)
    s2p=JBSparameter_to_S2PV1(table)
    print("Before conversion the JBSparameter file is {0} ".format(table))
    s2p.change_data_format('RI')
    print("After Conversion the JBSparameter file is {0} ".format(s2p))
    s2p.show()
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_AsciiDataTable_to_XmlDataTable()
    #test_OnePortRaw_to_XmlDataTable()
    #test_AsciiDataTable_to_pandas()
    #timeit_script()
    #timeit_script(script="test_AsciiDataTable_to_pandas()",
     #             setup="from __main__ import test_AsciiDataTable_to_pandas",n_loops=10)
    # timeit_script(script="test_OnePortRaw_to_XmlDataTable()",
    #               setup="from __main__ import test_OnePortRaw_to_XmlDataTable",n_loops=10)
    #test_S2P_to_XmlDataTable()
    #test_S2P_to_XmlDataTable('TwoPortTouchstoneTestFile.s2p')
    #test_S2P_to_XmlDataTable('20160301_30ft_cable_0.s2p')
    #test_S2P_to_XmlDataTable_02('20160301_30ft_cable_0.s2p',**{"style_sheet":"../XSL/S2P_STYLE_02.xsl"})
    #test_TwoPortCalrep_to_XmlDataTable(r'C:\Share\ascii.dut\000146a.txt')
    #test_TwoPortRaw_to_XmlDataTable()
    #test_TwoPortRawModel_to_S2PV1()
    #test_PowerRawModel_to_XmlDataTable(**{"style_sheet":"../XSL/POWER_RAW_STYLE_002.xsl"})
    #test_JBSparameter_to_S2PV1()
    #test_OnePortCalrep_to_XmlDataTable(**{"style_sheet":"../XSL/ONE_PORT_CALREP_STYLE_002.xsl"})
    #test_S2P_to_XmlDataTable('704b.S2P')
    test_S1PV1_to_XmlDataTable()
    test_StatistiCALSolutionModel_to_XmlDataTable()