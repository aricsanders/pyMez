#-----------------------------------------------------------------------------
# Name:        Translations
# Purpose:     To translate from one data form to another
# Author:      Aric Sanders
# Created:     3/3/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Translations.py holds the functions that map from one form to another"""

#-----------------------------------------------------------------------------
# Standard Imports
import timeit
import os
import sys
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
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def AsciiDataTable_to_XMLDataTable(ascii_data_table,**options):
    """Takes an AsciiDataTable and returns a XMLDataTable with **options"""
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

def AsciiDataTable_to_DataFrame(ascii_data_table):
    """Converts an AsciiDataTable to a pandas.DataFrame
    discarding any header or footer information"""
    data_frame=pandas.DataFrame(data=ascii_data_table.data,columns=ascii_data_table.column_names)
    return data_frame

def AsciiDataTable_to_DataFrame_dict(AsciiDataTable):
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

def DataFrame_dict_to_excel(DataFrame_dict,excel_file_name="Test.xlsx"):
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

def excel_to_DataFrame_dict(excel_file_name):
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

def AsciiDataTable_to_Excel(ascii_data_table,file_path=None):
    """Converts an AsciiDataTable to an excel spreadsheet using pandas"""
    if ascii_data_table.header:
        data_frame=pandas.DataFrame(data=ascii_data_table.data,columns=ascii_data_table.column_names,index=False)

def S2PV1_to_XMLDataTable(s2p,**options):
    """Transforms a s2p's sparameters to a XMLDataTable. Converts the format to #GHz DB first"""
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
def SNP_to_XMLDataTable(snp,**options):
    """Transforms a snp's sparameters to a XMLDataTable. Converts the format to #GHz DB first"""
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

def S1PV1_to_XMLDataTable(s1p,**options):
    """Transforms a s1p's sparameters to a XMLDataTable. Converts the format to RI first"""
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

def TwoPortCalrepModel_to_XMLDataTable(two_port_calrep_table,**options):
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
    new_xml=AsciiDataTable_to_XMLDataTable(table,**XML_options)
    return new_xml

def TwoPortCalrepModel_to_S2PV1(two_port_calrep_table,**options):
    """Transforms a TwoPortRawModel  to S2PV1"""
    table=two_port_calrep_table
    path=table.path.split('.')[0]+".s2p"
    data=[[row["Frequency"],row["magS11"],row["argS11"],row["magS21"],row["argS21"],row["magS21"],
           row["argS21"],row["magS22"],row["argS22"]] for row in table.joined_table.get_data_dictionary_list()]
    comments=[[line,index,0] for index,line in enumerate(table.joined_table.header[:])]
    s2p_options={"option_line":"# GHz S MA R 50","sparameter_data":data,
                 "comments":comments,"path":path,"option_line_line":len(table.joined_table.header),
                 "sparameter_begin_line":len(table.joined_table.header)+1,"column_names":S2P_MA_COLUMN_NAMES}
    s2p_file=S2PV1(None,**s2p_options)
    return s2p_file

def OnePortCalrep_to_XMLDataTable(one_port_calrep_table,**options):
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
    new_xml=AsciiDataTable_to_XMLDataTable(table,**XML_options)
    return new_xml

def TwoPortRawModel_to_XMLDataTable(two_port_raw_table,**options):
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
    new_xml=AsciiDataTable_to_XMLDataTable(table,**XML_options)
    return new_xml

def TwoPortRawModel_to_S2PV1(two_port_raw_table,**options):
    """Transforms a TwoPortRawModel  to S2PV1"""
    table=two_port_raw_table
    path=table.path.split('.')[0]+".s2p"
    data=[[row[0],row[3],row[4],row[5],row[6],row[5],row[6],row[7],row[8]] for row in table.data]
    comments=[[line,index,0] for index,line in enumerate(table.header[:])]
    s2p_options={"option_line":"# GHz S MA R 50","sparameter_data":data,
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
    s2p_options={"option_line":"# GHz S RI R 50","sparameter_data":data,
                 "comments":comments,"path":path,"option_line_line":len(table.header),
                 "sparameter_begin_line":len(table.header)+1,"column_names":S2P_RI_COLUMN_NAMES}
    s2p_file=S2PV1(None,**s2p_options)
    return s2p_file

def PowerRawModel_to_XMLDataTable(power_raw_table,**options):
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
    new_xml=AsciiDataTable_to_XMLDataTable(table,**XML_options)
    return new_xml

def DataFrame_to_hdf(pandas_data_frame):
    pandas_data_frame.to_hdf("Test.hdf","table")
    return "Test.hdf"
def hdf_to_DataFrame(hdf_file_name):
    df=pandas.read_hdf(hdf_file_name,"table")
    return df
def XMLDataTable_to_AsciiDataTable(xml_table):

    table=AsciiDataTable(None,
                         column_names=xml_table.attribute_names,
                         data=xml_table.data)
    return table
def AsciiDataTable_to_XMLDataTable_2(data_table):
    xml=AsciiDataTable_to_XMLDataTable(data_table)
    return xml
def DataFrame_to_excel(pandas_data_frame,file_name="Test.xlsx"):
    pandas_data_frame.to_excel(file_name,index=False)
    return file_name

def excel_to_DataFrame(excel_file_name):
    df=pandas.read_excel(excel_file_name)
    return df
def DataFrame_to_HTML_string(pandas_data_frame):
    html=pandas_data_frame.to_html(index=False)
    return html

def HTML_string_to_DataFrame(html_string):
    list_df=pandas.read_html(html_string)
    return list_df[0]
def DataFrame_to_json(pandas_data_frame):
    json=pandas_data_frame.to_json("test.json",orient='records')
    return "test.json"

def json_to_DataFrame(json_file_name):
    data_frame=pandas.read_json(json_file_name,orient='records')
    return data_frame

def DataFrame_to_json_string(pandas_data_frame):
    json=pandas_data_frame.to_json(orient='records')
    return json

def json_string_to_DataFrame(json_string):
    data_frame=pandas.read_json(json_string,orient='records')
    return data_frame

def DataFrame_to_csv(pandas_data_frame,file_name="test.csv"):
    csv=pandas_data_frame.to_csv(file_name,index=False)
    return file_name

def csv_to_DataFrame(csv_file_name):
    data_frame=pandas.read_csv(csv_file_name)
    return data_frame

def AsciiDataTable_to_Matlab(ascii_data_table,file_name="test.mat"):
    matlab_data_dictionary={"data":ascii_data_table.data,"column_names":ascii_data_table.column_names}
    savemat(file_name,matlab_data_dictionary)
    return file_name

def Matlab_to_AsciiDataTable(matlab_file_name):
    matlab_data_dictionary=loadmat(matlab_file_name)
    ascii_data_table=AsciiDataTable(None,
                                    column_names=map(lambda x: x.rstrip().lstrip(),
                                                     matlab_data_dictionary["column_names"].tolist()),
                                     data=matlab_data_dictionary["data"].tolist())
    return ascii_data_table

def DataTable_to_XML(xml_data_table,file_name="test.xml"):
    xml_data_table.save(file_name)
    return file_name

def XML_to_DataTable(xml_file_name):
    xml_data_table=DataTable(xml_file_name)
    return xml_data_table
def html_string_to_html_file(html_string,file_name="test.html"):
    out_file=open(file_name,'w')
    out_file.write(html_string)
    out_file.close()
    return file_name
# this is broken, something does not work properly
def html_file_to_pandas(html_file_name):
    in_file=open(html_file_name,'r')
    pandas_data_frame=pandas.read_html(in_file)
    return pandas_data_frame

def html_file_to_html_string(html_file_name):
    in_file=open(html_file_name,'r')
    html_string=in_file.read()
    return html_string

def DataFrame_to_html_file(pandas_data_frame,file_name="test.html"):
    out_file=open(file_name,'w')
    pandas_data_frame.to_html(out_file,index=False)
    return file_name

def json_to_DataTable(json_file_name):
    data_dictionary_list=json.load(open(json_file_name,'r'))
    xml=DataTable(None,data_dictionary={"data":data_dictionary_list})
    return xml

def csv_to_AsciiDataTable(csv_file_name):
    options={"column_names_begin_line":0,"column_names_end_line":1,
             "data_begin_line":1,"data_end_line":-1,"data_delimiter":",","column_names_delimiter":","}
    table=AsciiDataTable(csv_file_name,**options)
    return table
def png_to_jpg(png_file_name):
    [root_name,extension]=png_file_name.split(".")
    jpeg_file_name=root_name+".jpg"
    PIL.Image.open(png_file_name).save(jpeg_file_name)
    return jpeg_file_name
def file_to_Image(file_path):
    new_image=PIL.Image.open(file_path)
    if re.search(".gif",file_path,re.IGNORECASE):
        new_image=new_image.convert("RGB")
    return new_image

def Image_to_file(pil_image,file_path=None):
    if file_path is None:
        file_path=pil_image.filename
    pil_image.save(file_path)
    return file_path

def Image_to_file_type(pil_image,file_path=None,extension="png"):

    if file_path is None:
        file_path=pil_image.filename
    root_name=file_path.split(".")[0]
    new_file_name=root_name+"."+extension.replace(".","")
    if re.search('jp|bmp',extension,re.IGNORECASE):
        pil_image.convert('RGB')
    print("{0} is {1}".format("pil_image.mode",pil_image.mode))
    pil_image.save(new_file_name)
    return new_file_name

def Image_to_thumbnail(pil_image,file_path="thumbnail.jpg"):
    size = (64, 64)
    temp_image=pil_image.copy()
    temp_image.thumbnail(size)
    temp_image.save(file_path)
    return file_path

def png_to_base64(file_name):
    in_file=open(file_name, "rb")
    encoded=base64.b64encode(in_file.read())
    return encoded

def base64_to_png(base64_encoded_png,file_name="test.png"):
    out_file=open(file_name, "wb")
    decoded=base64.b64decode(base64_encoded_png)
    out_file.write(decoded)
    out_file.close()
    return file_name




#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
def test_AsciiDataTable_to_XMLDataTable(input_file="700437.asc"):
    """Tests a one port ascii data table to an XMLDataTable transformation
    and saves the result in the tests directory. The one port file should be the output
    of Calrep7.1 or similar."""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortRawModel(input_file)
    XML_one_port=AsciiDataTable_to_XMLDataTable(one_port)
    print XML_one_port
    XML_one_port.save()
    XML_one_port.save_HTML()

def test_OnePortRaw_to_XMLDataTable(input_file="OnePortRawTestFile.txt"):
    """Tests a one port raw ascii data table to an XMLDataTable transformation
    and saves the result in the tests directory. The one port file should be the output
    of Meas HP Basic program or similar. Average time without print is 7.2 ms for 10 loops."""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortRawModel(input_file)
    options={"style_sheet":"../XSL/ONE_PORT_RAW_STYLE.xsl"}
    XML_one_port=AsciiDataTable_to_XMLDataTable(one_port,**options)
    #print XML_one_port
    XML_one_port.save()
    XML_one_port.save_HTML()

def test_StatistiCALSolutionModel_to_XMLDataTable(input_file="Solution_Plus.txt"):
    """Tests a StatistiCALSolutionModel  ascii data table to an XMLDataTable transformation
    and saves the result in the tests directory. """
    os.chdir(TESTS_DIRECTORY)
    solution=StatistiCALSolutionModel(input_file)
    options={"style_sheet":"../XSL/DEFAULT_MEASUREMENT_STYLE.xsl"}
    XML_solution=AsciiDataTable_to_XMLDataTable(solution,**options)
    print XML_solution
    XML_solution.show()
    print XML_solution.to_HTML()

def test_AsciiDataTable_to_DataFrame(input_file="700437.asc"):
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortCalrepModel(input_file)
    data_frame=AsciiDataTable_to_DataFrame(one_port)
    data_frame.to_excel('one_port.xlsx', sheet_name='Sheet1')
    #print data_frame

def test_S2P_to_XMLDataTable(file_path="thru.s2p"):
    os.chdir(TESTS_DIRECTORY)
    s2p_file=S2PV1(file_path)
    XML_s2p=S2PV1_to_XMLDataTable(s2p_file)
    XML_s2p.save()
    #print XML_s2p
def test_S1PV1_to_XMLDataTable(file_path="OnePortTouchstoneTestFile.s1p"):
    """Tests the S1PV1 to XMLDataTable translation"""
    os.chdir(TESTS_DIRECTORY)
    s1p_file=S1PV1(file_path)
    XML_s1p=S1PV1_to_XMLDataTable(s1p_file)
    XML_s1p.show()
def timeit_script(script='test_AsciiDataTable_to_XMLDataTable()',
                  setup="from __main__ import test_AsciiDataTable_to_XMLDataTable",n_loops=10):
    """Returns the mean time from running script n_loops time. To import a script, put a string
    import statement in setup"""
    print timeit.timeit(script,setup=setup,number=n_loops)/n_loops

def test_S2P_to_XMLDataTable_02(file_path="thru.s2p",**options):
    os.chdir(TESTS_DIRECTORY)
    s2p_file=S2PV1(file_path)
    XML_s2p=S2PV1_to_XMLDataTable(s2p_file,**options)
    #XML_s2p.save()

def test_TwoPortCalrep_to_XMLDataTable(file_path='922729.asc',**options):
    """Test's the conversion of the TwoPortCalrep to XMLDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortCalrepModel(file_path)
    two_port.joined_table.save()
    xml=TwoPortCalrepModel_to_XMLDataTable(two_port,**options)
    xml.save()
    xml.save_HTML()

def test_OnePortCalrep_to_XMLDataTable(file_path='700437.asc',**options):
    """Test's the conversion of the OnePortCalrep to XMLDataTable"""
    os.chdir(TESTS_DIRECTORY)
    one_port=OnePortCalrepModel(file_path)
    one_port.save("ExportedOnePortCalrep.txt")
    xml=OnePortCalrep_to_XMLDataTable(one_port,**options)
    xml.save()
    xml.save_HTML()

def test_TwoPortRawModel_to_XMLDataTable(file_path='TestFileTwoPortRaw.txt',**options):
    """Test's the conversion of the TwoPorRaw to XMLDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortRawModel(file_path)
    two_port.save("SavedTest2PortRaw.txt")
    xml=TwoPortRawModel_to_XMLDataTable(two_port,**options)
    xml.save("SavedTest2PortRaw.xml")
    xml.save_HTML(file_path="SavedTest2PortRaw.html")

def test_TwoPortRawModel_to_S2PV1(file_path='TestFileTwoPortRaw.txt',**options):
    """Test's the conversion of the TwoPorRaw to XMLDataTable"""
    os.chdir(TESTS_DIRECTORY)
    two_port=TwoPortRawModel(file_path)
    s2p=TwoPortRawModel_to_S2PV1(two_port,**options)
    print(s2p)
    s2p.save("SavedTest2PortRaw.s2p")

def test_PowerRawModel_to_XMLDataTable(file_path='CTNP15.A1_042601',**options):
    """Test's the conversion of the TwoPorRaw to XMLDataTable"""
    os.chdir(TESTS_DIRECTORY)
    power=PowerRawModel(file_path)
    print power
    xml=PowerRawModel_to_XMLDataTable(power,**options)
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
    #test_AsciiDataTable_to_XMLDataTable()
    #test_OnePortRaw_to_XMLDataTable()
    #test_AsciiDataTable_to_pandas()
    #timeit_script()
    #timeit_script(script="test_AsciiDataTable_to_pandas()",
     #             setup="from __main__ import test_AsciiDataTable_to_pandas",n_loops=10)
    # timeit_script(script="test_OnePortRaw_to_XMLDataTable()",
    #               setup="from __main__ import test_OnePortRaw_to_XMLDataTable",n_loops=10)
    #test_S2P_to_XMLDataTable()
    #test_S2P_to_XMLDataTable('TwoPortTouchstoneTestFile.s2p')
    #test_S2P_to_XMLDataTable('20160301_30ft_cable_0.s2p')
    #test_S2P_to_XMLDataTable_02('20160301_30ft_cable_0.s2p',**{"style_sheet":"../XSL/S2P_STYLE_02.xsl"})
    #test_TwoPortCalrep_to_XMLDataTable(r'C:\Share\ascii.dut\000146a.txt')
    #test_TwoPortRaw_to_XMLDataTable()
    #test_TwoPortRawModel_to_S2PV1()
    #test_PowerRawModel_to_XMLDataTable(**{"style_sheet":"../XSL/POWER_RAW_STYLE_002.xsl"})
    #test_JBSparameter_to_S2PV1()
    #test_OnePortCalrep_to_XMLDataTable(**{"style_sheet":"../XSL/ONE_PORT_CALREP_STYLE_002.xsl"})
    #test_S2P_to_XMLDataTable('704b.S2P')
    test_S1PV1_to_XMLDataTable()
    test_StatistiCALSolutionModel_to_XMLDataTable()