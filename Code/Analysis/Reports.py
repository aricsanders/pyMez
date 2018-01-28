#-----------------------------------------------------------------------------
# Name:        Reports
# Purpose:    
# Author:      Aric Sanders
# Created:     1/26/2018
# License:     MIT License
#-----------------------------------------------------------------------------
"""Reports is a module dedicated to generating reports after data collection or analysis

  Examples
--------
    #!python


Requirements
------------
+ [sys](https://docs.python.org/2/library/sys.html)
+ [os](https://docs.python.org/2/library/os.html)
+ [re](https://docs.python.org/2/library/re.html)
+ [math](https://docs.python.org/2/library/math.html)
+ [pyMez](https://github.com/aricsanders/pyMez)

Help
---------------
<a href="./index.html">`pyMez.Code.Analysis`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/Html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>

 """
#-----------------------------------------------------------------------------
# Standard Imports
import os
import sys
import math
import re
#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.DataHandlers.NISTModels import *
except:
    print("Code.DataHandlers.NISTModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.XMLModels import *
except:
    print("Code.DataHandlers.XMLModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.HTMLModels import *
except:
    print("Code.DataHandlers.HTMLModels did not import correctly")
    raise ImportError
try:
    from Code.DataHandlers.GraphModels import *
except:
    print("Code.DataHandlers.GraphModels did not import correctly")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants
DEFAULT_TOGGLE_SCRIPT="""<script type="text/javascript">
    function toggleId(id,$link){
    $node = document.getElementById(id);
    if (!$node)
    return;
    if (!$node.style.display || $node.style.display == 'none') {
    $node.style.display = 'block';
    $link.value = '-';
    } else {
    $node.style.display = 'none';
    $link.value = '+';
    }
  }
  </script>"""

DEFAULT_TOGGLE_STYLE="""<style>
  .toggleButton {
      background-color: white;
      border: 2px solid black;
       border-radius: 8px;
       color:red;
	   }
   .toggleButton:hover {
    box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
	}
    </stlye>"""
ONE_PORT_DTYPE={'Frequency':'float',
                 'Direction':'str',
                 'Connect':'str',
                 'System_Id':'str',
                 'System_Letter':'str',
                 'Connector_Type_Calibration':'str',
                 'Connector_Type_Measurement':'str',
                 'Measurement_Type':'str',
                 'Measurement_Date':'str',
                 'Measurement_Time':'str',
                 'Program_Used':'str',
                 'Program_Revision':'str',
                 'Operator':'str',
                 'Calibration_Name':'str',
                 'Calibration_Date':'str',
                 'Port_Used':'int',
                 'Number_Connects':'str',
                 'Number_Repeats':'str',
                 'Nbs':'str',
                 'Number_Frequencies':'str',
                 'Start_Frequency':'float',
                 'Device_Description':'str',
                 'Device_Id':'str',
                 'Measurement_Timestamp':'str',
                }
#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class HTMLReport(HTMLBase):
    def add_toggle_script(self, script=DEFAULT_TOGGLE_SCRIPT):
        """Adds a javascript template toggle script to the body of the HTML"""
        self.append_to_body(script)

    def add_toggle_style(self, style=DEFAULT_TOGGLE_STYLE):
        """Adds a css to format the javascript template, should be done once"""
        self.append_to_head(style)

    def add_toggle(self, tag_id=None):
        """Adds a toggle button that toggles the element with id tag_id. This can be used many times """
        toggle = '<input type="button" class="toggleButton"  value="+" onclick="toggleId(\'{0}\',this)">'.format(tag_id)
        self.append_to_body(toggle)

    def embedd_image(self, image, image_mode="MatplotlibFigure", **options):
        """Embedds an image in the report. image_mode can be  MatplotlibFigure (a reference to the figure class),
        Image (the PIL class),
        Base64 (a string of the values),
        Png, Jpg, Bmp Tiff(the file name),
        or a Ndarray of the image values"""
        # might change this to self.ImageGraph and use it elsewhere
        image_graph = ImageGraph()
        image_graph.set_state(image_mode, image)
        image_graph.move_to_node("embeddedHTML")
        self.append_to_body(image_graph.data)

    def embedd_image_figure(self, image, image_mode="MatplotlibFigure", figure_id="image", caption="", **options):
        """Embedds an image in the report. image_mode can be  MatplotlibFigure (a reference to the figure class),
        Image (the PIL class),
        Base64 (a string of the values),
        Png, Jpg, Bmp Tiff(the file name),
        or a Ndarray of the image values. The image is in a <figure id=figure_id> tag"""
        # might change this to self.ImageGraph and use it elsewhere
        image_graph = ImageGraph()
        image_graph.set_state(image_mode, image)
        image_graph.move_to_node("embeddedHTML")
        self.append_to_body("<figure id='{0}'>{1}<figcaption>{2}</figcaption></figure>".format(figure_id,
                                                                                               image_graph.data,
                                                                                               caption))

    def add_download_link(self, content_string, text="Download File", suggested_name="test.txt",
                          mime_type="text/plain"):
        """Adds a download link to the report"""
        self.append_to_body(String_to_DownloadLink(content_string, text=text,
                                                   suggested_name=suggested_name,
                                                   mime_type=mime_type))


class CheckStandardReport(object):
    """CheckStandardReport generates an HTML report based on a raw calibrated measurement of a checkstandard """
    pass
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    