#-----------------------------------------------------------------------------
# Name:        pyMezJupyterWidgets
# Purpose:    To hold pyMez specific widgets
# Author:      Aric Sanders
# Created:     1/3/2019
# License:     MIT License
#-----------------------------------------------------------------------------
""" JupyterWidgets provides widgets for the jupyter notebook frontend.

Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../../index.html">API Documentation Home</a> |
<a href="../../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../../Reference_Index.html">Index</a>
</div> """
#-----------------------------------------------------------------------------
# Standard Imports

#-----------------------------------------------------------------------------
# Third Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.FrontEnds.Jupyter.JupyterWidgets import *
except:
    print("The module pyMez.FrontEnds.Jupyter.JupyterWidgets was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
try:
    from Code.InstrumentControl.Instruments import *
except:
    print("The module pyMez.FrontEnds.Jupyter.JupyterWidgets was not found or had an error,"
          "please check module or put it on the python path")
    raise ImportError
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class HtmlFileBrowser(object):
    def __init__(self, directory):
        file_names = os.listdir(directory)
        self.button_list = []
        for file_name in file_names:
            try:
                if os.path.isdir(os.path.join(directory, file_name)):
                    pass
                else:
                    button = JupyterButton(data=os.path.join(directory, file_name),
                                                                               function=lambda x: html_convert_fileview(
                                                                                   x),
                                                                               description=file_name,
                                                                               stlye={'description_width': 'initial'},
                                                                               layout=Layout(width='80%',
                                                                                             height='40px'))
                    self.button_list.append(button)
            except:
                raise

    def show(self):
        display(*self.button_list)

class InstrumentSelectionDropdown(widgets.Dropdown):
    """Creates a dropdown with the availble resources as choices"""
    def __init__(self,**options):
        """"""
        rm=visa.ResourceManager()
        widgets.Dropdown.__init__(self,
            options=rm.list_resources(),
            description='Instrument:',
            disabled=False,
            )
    def show(self):
        display(self)

class InstrumentSelectionRadio(widgets.RadioButtons):
    """Creates a set of radio buttons with avaible resources as choices"""
    def __init__(self,**options):
        """"""
        rm=visa.ResourceManager()
        widgets.RadioButtons.__init__(self,
            options=rm.list_resources(),
            description='Instrument:',
            disabled=False,
            )
    def show(self):
        display(self)

class VisaWidget(object):
    """Jupyter widget that sends and recieves messages from an arbitrary VisaInstrument"""

    def __init__(self, **options):
        defaults = {"instrument_selection_style": "radio", "widget_alignment": "Horizontal", "fake_instrument": True}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        # First we begin by creating the layout widgets
        if re.search("V", self.options["widget_alignment"], re.IGNORECASE):
            self.bounding_box = widgets.VBox()
        else:
            self.bounding_box = widgets.HBox()
            # Next we create an instrument selection widget
        if re.search("radio", self.options["instrument_selection_style"], re.IGNORECASE):
            self.selection = InstrumentSelectionRadio()
        else:
            self.selection = InstrumentSelectionDropdown()
        if self.options["fake_instrument"]:
            self.selection.options = list(self.selection.options) + ["fake_instrument"]
            self.selection.value = "fake_instrument"
        # register a callback for changing the selection
        self.selection.observe(self.set_instrument, names="value")

        # Now we create a write and response text control
        self.write_box = widgets.Textarea(
            value='',
            placeholder='Type something',
            description='Write:',
            disabled=False
        )
        self.read_box = widgets.Textarea(
            value='',
            placeholder='Type something',
            description='Read:',
            disabled=False
        )
        # Now we create the buttons and set their callbacks
        self.write_button = widgets.Button(description="Write")
        self.write_button.on_click(self.write_value)
        self.read_button = widgets.Button(description="Read")
        self.read_button.on_click(self.read_value)
        self.query_button = widgets.Button(description="Query")
        self.query_button.on_click(self.query_instrument)
        box_layout = Layout(border='solid',
                            width="auto", align_items="center")
        self.button_box = widgets.VBox([self.query_button, self.write_button, self.read_button])
        self.button_box.layout = box_layout

        self.bounding_box.children = [self.selection, self.write_box, self.button_box, self.read_box]
        self.bounding_box.layout = box_layout
        self.set_instrument(self.selection)

    def set_instrument(self, selection):
        self.instrument = VisaInstrument(self.selection.value)

    def write_value(self, button):
        self.instrument.write(self.write_box.value)

    def read_value(self, button):
        self.read_box.value = self.instrument.read()

    def query_instrument(self, button):
        read_value = self.instrument.query(self.write_box.value)
        self.read_box.value = read_value

    def show(self):
        display(self.bounding_box)
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    