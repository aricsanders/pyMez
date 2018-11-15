#-----------------------------------------------------------------------------
# Name:        HTMLModels
# Purpose:    Module for the processing of HTML based Models
# Author:      Aric Sanders
# Created:     12/16/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" HTMLModels is a module for the creation and manipulation of HTML based models.
It provides a model to open, print, add to and convert html to pdf.

Examples
--------
    #!python
    >>new_html=HTMLBase(os.path.join(TESTS_DIRECTORY,"One_Port_Sparameter_20160307_001.html"))
    >>print(new_html)

 <h3><a href="../../../Examples/Html/HTMLModels_Example.html">HTMLModels Example</a></h3>

Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html?highlight=os#module-os)
+ [lxml](http://lxml.de/)
+ [types](https://docs.python.org/2/library/types.html)
+ [pyMez](https://github.com/aricsanders/pyMez)
+ [pdfkit](http://pdfkit.org/)
+ [wkhtmltopdf](http://wkhtmltopdf.org/)

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
import sys
import lxml.html
import lxml.html.builder
from types import *
import re
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Utils.Alias import alias
    METHOD_ALIASES=1
except:
    raise
    print("The module pyMez.Code.Utils.Alias was not found")
    METHOD_ALIASES=0
    pass
# For Auto-naming of files if path is not specified
try:
    from Code.Utils.Names import auto_name,change_extension
    DEFAULT_FILE_NAME=None
except:
    print("The function auto_name in pyMez.Code.Utils.Names was not found")
    print("Setting Default file name to New_XML.xml")
    DEFAULT_FILE_NAME='New_XML.xml'
    pass

try:
    from Code.Utils.Types import *
except:
    print("The module pyMez.Code.Utils.Types was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
# TODO: decide if I am going to use cssselect
# try:
#     import cssselect
# except:
#     print("The module lxml.html.cssselect was not found or had an error. If it is not installed"
#           "Install it with pip install cssselect")
#     #raise
#     pass

try:
    import pdfkit
    PDF_CONVERT=True
except:
    print("The module pdfkit was not found or had an error. Install it using pip install pdfkit, also"
          "requires wkhtmltpdf to be installed. Wkhtmltopdf can be found at http://wkhtmltopdf.org/")
    PDF_CONVERT=False
    pass

#-----------------------------------------------------------------------------
# Module Constants
HTML_TEMPLATE_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'HTML')
WKHTML_PATH=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
TESTS_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')
#-----------------------------------------------------------------------------
# Module Functions
def make_html_element(tag,text=None,**attribute_dictionary):
    """Creates an lxml.html.HtmlElement given a tag, text and attribute dictionary
     <tag key1="value2" key2="value2">text</tag> """
    position_arguments=[tag]
    if text:
        position_arguments.append(text)
    new_tag=lxml.html.builder.E(*position_arguments,**attribute_dictionary)
    return new_tag

def make_html_string(tag,text=None,**attribute_dictionary):
    """Creates the html string for tag, text and attribute dictionary
     <tag key1="value2" key2="value2">text</tag> """
    position_arguments=[tag]
    if text:
        position_arguments.append(text)
    new_tag=lxml.html.builder.E(*position_arguments,**attribute_dictionary)
    out_text=lxml.html.tostring(new_tag)
    return out_text

#-----------------------------------------------------------------------------
# Module Classes
class HTMLBase(object):
    """HTMLBase has standard parsing and printing capabilities, designed so that other HTML models
    can inherit from it"""
    def __init__(self,file_path=None,**options):
        """Intializes the HTMLBase Class"""
        defaults={"specific_descriptor":'HTML',
                  "general_descriptor":'Document',
                  "directory":None,
                  "extension":'html',
                  "path":None,
                  "html_text":None,
                  "body":None,
                  "head":None
                  }
        self.options={}
        for key,value in defaults.items():
            self.options[key]=value
        for key,value in options.items():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is None:
            # create self.document
            if self.options["html_text"]:
                # first priority is just passing the full page in html_text
                self.document=lxml.html.fromstring(self.options["html_text"])
                self.root=self.document

            else:
                self.root=lxml.html.builder.HTML()
                self.document=lxml.etree.ElementTree(self.root)
                elements=["head","body"]
                for element in elements:
                    if self.options[element]:
                        if isinstance(element, StringType):
                            new_element=lxml.html.fragment_fromstring(self.options[element])
                            self.root.append(new_element)
                        elif isinstance(element, lxml.html.Element):
                            self.root.append(self.options[element])
                self.text=str(self)
            if self.options["path"]:
                self.path=self.options["path"]
            else:
                self.path=auto_name(specific_descriptor=self.options["specific_descriptor"],
                                    general_descriptor=self.options["general_descriptor"],
                                    directory=self.options["directory"],
                                    extension=self.options["extension"])
        else:
            self.path=file_path
            self.document=lxml.html.parse(file_path)
            try:
                self.root=self.document.getroot()
            except:pass
            try:
                self.head=self.root.head
            except:pass
            try:
                self.body=self.root.body
            except:pass

    def __str__(self):
        """Defines the response when str() or print() is called"""
        return lxml.html.tostring(self.document,encoding="unicode")

    def save(self,file_path=None,**temp_options):
        """Saves the html file, provide file path to save as, or temp_options"""
        original_options=self.options.copy()
        for key,value in temp_options.items():
            self.options[key]=value
        if file_path is None:
            file_path=self.path
        out_file=open(file_path,"w")
        out_file.write(str(self))
        out_file.close()
        self.options=original_options
        return file_path


    def show(self):
        """Saves html to a temp file and shows it in a browser"""
        lxml.html.open_in_browser(self.document)
    if PDF_CONVERT:
        def to_pdf(self,file_path=None,**options):
            """Converts the file to a pdf and saves it at file_path. If file_path is None, it will auto name
            the resulting file to self.path with pdf as the extension"""
            #todo: add toc and other options in wkhtmltopdf
            if file_path is None:
                file_path=change_extension(self.path,"pdf")
            config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)
            pdfkit.from_string(str(self),file_path,configuration=config)
            return file_path
    def add_head(self):
        """Adds a head tag to the model if it does not exist"""
        head=make_html_element(tag="head",text="")
        if len(self.root.getchildren())==0:
            self.root.append(head)
        elif not re.match("head",self.root.getchildren()[0].tag,re.IGNORECASE) and len(self.root.getchildren())>0:
            self.root.insert(0,head)
        else:
            print("head already exists, tag was not added ")

        self.head=self.root.head

    def add_body(self):
        """Adds a body tag to the model if it does not exist"""
        body=make_html_element(tag="body",text="")
        tags=[x.tag.lower() for x in self.root.getchildren()]
        if not "body" in tags:
            self.root.append(body)
        else:
            print("body already exists, tag was not added ")
            pass
        self.body=self.root.body

    def clear(self):
        """Clears all content in the HTML"""
        element_list=self.root.getchildren()
        for child in element_list:
            self.root.remove(child)

    def append_to_body(self,element):
        """Appends the element to the body of the model, if it is a string it parses first, if it is a
        dictionary it assumes it has the form {"tag":tag_name,"text":text_text,
        "attribute_dictionary":{"attribute_name":"attribute_value"}, and if it is a
        lxml.html.HtmlElement it appends it"""
        try:
            tags = [x.tag.lower() for x in self.root.getchildren()]
            if not "body" in tags:
                body = make_html_element(tag="body", text="")
                print("Body tag was not present adding it")
                self.root.append(body)

            if isinstance(element, StringType):
                new_element=lxml.html.fragment_fromstring(element)
            elif isinstance(element, DictionaryType):
                new_element=make_html_element(**element)
            elif isinstance(element,lxml.html.HtmlElement):
                new_element=element
            self.root.body.append(new_element)
        except:
            print(("Could not add {0} to body".format(element)))

    def append_to_head(self,element):
        """Appends the element to the head of the model, if it is a string it parses first, if it is a
        dictionary it assumes it has the form {"tag":tag_name,"text":text_text,
        "attribute_dictionary":{"attribute_name":"attribute_value"}, and if it is a
        lxml.html.HtmlElement it appends it"""
        try:
            tags = [x.tag.lower() for x in self.root.getchildren()]
            if not "head" in tags:
                head = make_html_element(tag="head", text="")
                print("Head tag was not present adding it")
                self.root.insert(0,head)

            if isinstance(element, StringType):
                new_element=lxml.html.fragment_fromstring(element)
            elif isinstance(element, DictionaryType):
                new_element=make_html_element(**element)
            elif isinstance(element,lxml.html.HtmlElement):
                new_element=element
            self.root.head.append(new_element)
        except:
            print(("Could not add {0} to head".format(element)))

    def to_HTML(self):
        """Convenience function that echos the content updates the attribute self.text"""
        self.text=str(self)
        return str(self.text)

    def __add__(self, other):
        """Adds two html sheets and returns the answer"""
        children_model_1=self.root.getchildren()
        children_model_2=other.root.getchildren()
        tags_model_1=[x.tag for x in children_model_1]
        tags_model_2=[x.tag for x in children_model_2]
        # if the models don't have a head or body add them
        if not "head" in tags_model_1:
            head = make_html_element(tag="head", text="")
            self.root.insert(0,head)
        if not "body" in tags_model_1:
            body=make_html_element(tag="body", text="")
            self.root.append(body)
        if "head" in tags_model_2:
            for child in other.root.head.getchildren():
                copy=child.__copy__()
                self.root.head.append(copy)
        if "body" in tags_model_2:
            for child in other.root.body.getchildren():
                copy=child.__copy__()
                self.root.body.append(copy)
        return self




class HTMLHelpPage(HTMLBase):
    """Model for a HTMLHelp page for a given module, class or function"""
    pass

#-----------------------------------------------------------------------------
# Module Scripts
def test_HTMLBase(file_name="One_Port_Raw_Sparameter_20160307_001.html"):
    """Tests the HTMLBase Class"""
    os.chdir(TESTS_DIRECTORY)
    html=HTMLBase(file_name)
    print(html)
    #html.to_pdf()
    html.show()

def test_HTMLBase_no_file(head=None,body=None):
    """Tests the HTMLBase Class"""
    os.chdir(TESTS_DIRECTORY)
    if head is None:
        head="<head><title> A test page</title></head>"
    if body is None:
        body="<body><h1> A Test </h1></body>"

    html=HTMLBase(None,head=head,body=body)
    print(html)
    # saves a pdf
    #html.to_pdf()
    html.show()

def test_make_html_element():
    """Tests both the make_html_string function
    """
    [tag,text,id_attribute]=["h3","A level 3 heading",{"id":"heading-here"}]
    print(("The input of the function is tag = {0}, text = {1}, attribute dictionary = {2}".format(tag,text,                                                                                               id_attribute)))
    print(("The resulting html string is {0}".format(make_html_string(tag,text,**id_attribute))))

def test_HTMLBase_addition(first="One_Port_Raw_Sparameter_20160307_001.html",second="One_Port_Raw_Sparameter_20160307_001.html"):
    os.chdir(TESTS_DIRECTORY)
    html_1=HTMLBase(first)
    html_2=HTMLBase(second)
    print(("-"*80))
    print(("The first HTML is {0}".format(str(html_1))))
    print(("-"*80))
    print(("The second HTML is {0}".format(str(html_2))))
    print(("-"*80))
    html_3=html_1+html_2
    print(("The addition is {0}".format(str(html_3))))
    html_3.show()
    html_3.save("combined_html.html")


#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_HTMLBase(file_name="One_Port_Raw_Sparameter_20160307_001.html")
    #test_HTMLBase_no_file()
    test_make_html_element()
    test_HTMLBase_addition()