#-----------------------------------------------------------------------------
# Name:        IPythonPanel
# Purpose:     
# Author:      Aric Sanders
# Created:     4/14/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" Example integrating an IPython kernel into a GUI App.

This trivial GUI application internally starts an IPython kernel, to which Qt
consoles can be connected either by the user at the command line or started
from the GUI itself, via a button.  The GUI can also manipulate one variable in
the kernel's namespace, and print the namespace to the console.

Play with it by running the script and then opening one or more consoles, and
pushing the 'Counter++' and 'Namespace' buttons.

Upon exit, it should automatically close all consoles opened from the GUI.

Consoles attached separately from a terminal will not be terminated, though
they will notice that their kernel died.

Ref: Modified from wxPython source code wxPython/samples/simple/simple.py
"""

#-----------------------------------------------------------------------------
# Standard Imports
import sys

import wx
# This import is broken!! don't know how to fix it yet
from ipykernel.ipkernel import IPythonKernel
#-----------------------------------------------------------------------------
# Third Party Imports

#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import sys

from IPython.lib.kernel import connect_qtconsole
from IPython.kernel.zmq.kernelapp import IPKernelApp


# -----------------------------------------------------------------------------
# Functions and classes
# -----------------------------------------------------------------------------
def mpl_kernel(gui):
    """Launch and return an IPython kernel with matplotlib support for the desired gui
    """
    kernel = IPKernelApp.instance()
    kernel.initialize(['python', '--matplotlib=%s' % gui,
                       # '--log-level=10'
                       ])
    return kernel


class InternalIPKernel(object):
    def init_ipkernel(self, backend):
        # Start IPython kernel with GUI event loop and mpl support
        self.ipkernel = mpl_kernel(backend)
        # To create and track active qt consoles
        self.consoles = []

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

        # Example: a variable that will be seen by the user in the shell, and
        # that the GUI modifies (the 'Counter++' button increments it):
        self.namespace['app_counter'] = 0
        # self.namespace['ipkernel'] = self.ipkernel  # dbg

    def print_namespace(self, evt=None):
        print("\n***Variables in User namespace***")
        for k, v in self.namespace.items():
            if not k.startswith('_'):
                print('%s -> %r' % (k, v))
        sys.stdout.flush()

    def new_qt_console(self, evt=None):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(self.ipkernel.connection_file, profile=self.ipkernel.profile)

    def count(self, evt=None):
        self.namespace['app_counter'] += 1

    def cleanup_consoles(self, evt=None):
        for c in self.consoles:
            c.kill()

class MyFrame(wx.Frame, InternalIPKernel):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(350, 285))

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(panel, -1, "Hello World!")
        text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        qtconsole_btn = wx.Button(panel, -1, "Qt Console")
        ns_btn = wx.Button(panel, -1, "Namespace")
        count_btn = wx.Button(panel, -1, "Count++")
        close_btn = wx.Button(panel, -1, "Quit")

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.new_qt_console, qtconsole_btn)
        self.Bind(wx.EVT_BUTTON, self.print_namespace, ns_btn)
        self.Bind(wx.EVT_BUTTON, self.count, count_btn)
        self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, close_btn)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        for ctrl in [text, qtconsole_btn, ns_btn, count_btn, close_btn]:
            sizer.Add(ctrl, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
        panel.Layout()

        # Start the IPython kernel with gui support
        self.init_ipkernel('wx')

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print("See ya later!")
        sys.stdout.flush()
        self.cleanup_consoles(evt)
        self.Close()
        # Not sure why, but our IPython kernel seems to prevent normal WX
        # shutdown, so an explicit exit() call is needed.
        sys.exit()


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Simple wxPython App")
        self.SetTopWindow(frame)
        frame.Show(True)
        self.ipkernel = frame.ipkernel
        return True



#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    app = MyApp(redirect=False, clearSigInt=False)

    # Very important, IPython-specific step: this gets GUI event loop
    # integration going, and it replaces calling app.MainLoop()
    app.ipkernel.start()
