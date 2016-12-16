#-----------------------------------------------------------------------------
# Name:        HTMLModels
# Purpose:    Module for the processing of HTML based Models
# Author:      Aric Sanders
# Created:     12/16/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" HTMLModels is a module for the creation and manipulation of HTML based models """
#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys
import lxml.html
import lxml.html.builder
from types import *
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.Utils.Alias import alias
    METHOD_ALIASES=1
except:
    raise
    print("The module pyMeasure.Code.Utils.Alias was not found")
    METHOD_ALIASES=0
    pass
# For Auto-naming of files if path is not specified
try:
    from Code.Utils.Names import auto_name,change_extension
    DEFAULT_FILE_NAME=None
except:
    print("The function auto_name in pyMeasure.Code.Utils.Names was not found")
    print("Setting Default file name to New_XML.xml")
    DEFAULT_FILE_NAME='New_XML.xml'
    pass
try:
    import lxml.html.csselect
except:
    print("The module lxml.html.cssselect was not found or had an error. If it is not installed"
          "Install it with pip install cssselect")
    #raise
    pass
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
def make_html_element(tag,content=None,**attribute_dictionary):
    """Creates an lxml.html.HtmlElement given a tag, content and attribute dictionary
     <tag key1="value2" key2="value2">content</tag> """
    position_arguments=[tag]
    if content:
        position_arguments.append(content)
    new_tag=lxml.html.builder.E(*position_arguments,**attribute_dictionary)
    return new_tag

def make_html_string(tag,content=None,**attribute_dictionary):
    """Creates the html string for tag, content and attribute dictionary
     <tag key1="value2" key2="value2">content</tag> """
    position_arguments=[tag]
    if content:
        position_arguments.append(content)
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
                  "html_content":None,
                  "body":None,
                  "head":None
                  }
        self.options={}
        for key,value in defaults.iteritems():
            self.options[key]=value
        for key,value in options.iteritems():
            self.options[key]=value
        # Define Method Aliases if they are available
        if METHOD_ALIASES:
            for command in alias(self):
                exec(command)
        if file_path is None:
            # create self.document
            if self.options["html_content"]:
                # first priority is just passing the full page in html_content
                self.document=lxml.html.fromstring(self.options["html_content"])
            else:
                self.root=lxml.html.builder.HTML()
                self.document=lxml.etree.ElementTree(self.root)
                elements=["head","body"]
                for element in elements:
                    if self.options[element]:
                        if type(element) is StringType:
                            new_element=lxml.html.fragment_fromstring(self.options[element])
                            self.root.append(new_element)
                        elif type(element) is lxml.html.Element:
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
            self.root=self.document.getroot()
            self.head=self.root.head
            self.body=self.root.body

    def __str__(self):
        """Defines the response when str() or print() is called"""
        return lxml.html.tostring(self.document)

    def save(self,file_path=None,**temp_options):
        """Saves the html file, provide file path to save as, or temp_options"""
        original_options=self.options.copy()
        for key,value in temp_options.iteritems():
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

    def to_pdf(self,file_path=None,**options):
        """Converts the file to a pdf and saves it at file_path. If file_path is None, it will auto name
        the resulting file to self.path with pdf as the extension"""
        if file_path is None:
            file_path=change_extension(self.path,"pdf")
        config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)
        pdfkit.from_string(str(self),file_path,configuration=config)
        return file_path

    def to_HTML(self):
        """Convenience function that echos the content updates the attribute self.text"""
        self.text=str(self)
        return str(self.text)



#-----------------------------------------------------------------------------
# Module Scripts
def test_HTMLBase(file_name="One_Port_Raw_Sparameter_20160307_001.html"):
    """Tests the HTMLBase Class"""
    os.chdir(TESTS_DIRECTORY)
    html=HTMLBase(file_name)
    print html
    html.to_pdf()
    html.show()
def test_HTMLBase_no_file(head=None,body=None):
    """Tests the HTMLBase Class"""
    os.chdir(TESTS_DIRECTORY)
    if head is None:
        head="<head><title> A test page</title></head>"
    if body is None:
        body="<body><h1> A Test </h1></body>"

    html=HTMLBase(None,head=head,body=body)
    print html
    html.to_pdf()
    html.show()
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    #test_HTMLBase(file_name="One_Port_Raw_Sparameter_20160307_001.html")
    test_HTMLBase_no_file()