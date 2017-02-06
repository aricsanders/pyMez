#-----------------------------------------------------------------------------
# Name:        WxDialogFunctions
# Purpose:     To store simple wx based dialog functions
# Author:      Aric Sanders
# Created:     2/6/2017
# License:     MIT License
#-----------------------------------------------------------------------------
""" This module contains simple functions for creating wx dialogs and returning
import user choices.
  """

#-----------------------------------------------------------------------------
# Standard Imports
import os
#-----------------------------------------------------------------------------
# Third Party Imports
try:
    import wx
except:
    print("The wx module did not load properly. If it is not installed "
          "see https://wxpython.org/ for installation directions.")
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions
def get_directory():
    """Creates a directory dialog and returns the selected directory"""
    app = wx.App(None)
    dialog = wx.DirDialog(None, 'Select a Directory')
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

def get_path(wildcard='*.*'):
    """Creates a file dialog and returns the selected file"""
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open',wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path
#-----------------------------------------------------------------------------
# Module Classes

#-----------------------------------------------------------------------------
# Module Scripts
#TODO: Write Test Script
#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    pass