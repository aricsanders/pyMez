#-----------------------------------------------------------------------------
# Name:        JupyterWidgets
# Purpose:    To provide widgets for the Jupyter Notebook FrontEnd
# Author:      Aric Sanders
# Created:     12/20/2018
# License:     MIT License
#-----------------------------------------------------------------------------
""" JupyterWidgets provides widgets for the jupyter notebook frontend.

Help
---------------
<a href="../index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../../index.html">API Documentation Home</a> |
<a href="../../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../../Reference_Index.html">Index</a>
</div>"""
#-----------------------------------------------------------------------------
# Standard Imports

#-----------------------------------------------------------------------------
# Third Party Imports
try:
    import ipywidgets as widgets
    from IPython.display import display
except:
    print("The ipywidgets module could not be imported")
    raise
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def plot_data_attribute(b):
    """Routes the button.data element plot"""
    args,kwargs=b.data
    plt.plot(*args,**kwargs)
    plt.show()

def show_data_attribute(button):
    """Executes the show() method of the data attribute"""
    button.data.show()
#-----------------------------------------------------------------------------
# Module Classes
class JupyterButton(widgets.Button):
    """A modified button class with self.data and self.function attributes"""

    def __init__(self, **options):
        def echo(x):
            print(x)
        defaults = {"description":"Button","data":None,"function":echo}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        if self.options["data"]:
            self.data = self.options["data"]
        else:
            self.data = self.options["description"]
        button_parent_options = {}
        button_parent_keys = ["description", "tooltip", "icon", "disabled","style","layout"]
        for key in self.options.keys():
            if key in button_parent_keys:
                button_parent_options[key] = self.options[key]
        widgets.Button.__init__(self, **button_parent_options)
        if self.options["function"]:
            self.function = self.options["function"]
            self.on_click(self.function)

    def show(self):
        display(self)

class PlotButton(JupyterButton):
    """Takes plots the PlotButton.data attribute by passing it to matplotlib"""
    def __init__(self,**options):
        defaults = {"description":"Plot","data":[[[i for i in range(10)]],{}],"function":plot_data_attribute}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        JupyterButton.__init__(self,**self.options)

class ShowButton(JupyterButton):
    """A button to show the data attribute"""
    def __init__(self, **options):
        defaults = {"description": "Show", "data":plt,"function":show_data_attribute}
        self.options = {}
        for key, value in defaults.items():
            self.options[key] = value
        for key, value in options.items():
            self.options[key] = value
        JupyterButton.__init__(self, **self.options)
#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass
    