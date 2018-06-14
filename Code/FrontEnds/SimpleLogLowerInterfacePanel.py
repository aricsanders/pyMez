#-----------------------------------------------------------------------------
# Name:        SimpleLogLowerInterfacePanel.py
# Purpose:     
#
# Author:      <your name>
#
# Created:     2010/05/11
# RCS-ID:      $Index: SimpleLogLowerInterfacePanel.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
#Boa:FramePanel:SimpleLogLowerInterfacePanel
""" An interface panel for simple editing of logs, plugs into lower interface container
Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

import os
import datetime
# This determines PYMEASURE_ROOT below and checks if everything is installed properly 
try: 
    import pyMez
except:
    print("The topmost pyMez folder was not found please make sure that the directory directly above it is on sys.path") 
    raise
try:
    import pyMez.Code.DataHandlers.XMLModels as XMLModels
except:
    print """This module requires  pyMez.Code.DataHandlers.XMLModels to operate properly,
            add the directory directly above pyMez to sys.path"""  
import wx
import wx.stc

PYMEASURE_ROOT=os.path.dirname(os.path.realpath(pyMez.__file__))
LOGS_DIRECTORY=os.path.join(PYMEASURE_ROOT,'Data','Logs')

def convert_datetime(ISO_datetime_string,format_string='%m/%d/%Y at %H:%M:%S'):
    "Converts from long ISO format 2010-05-13T21:54:25.755000 to something reasonable"
    #strip any thing smaller than a second
    time_seconds=ISO_datetime_string.split('.')[0]
    
    #then get it into a datetime format
    time_datetime=datetime.datetime.strptime(time_seconds,"%Y-%m-%dT%H:%M:%S")
    return time_datetime.strftime(format_string)

[wxID_SIMPLELOGLOWERINTERFACEPANEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELCONTROLSPANEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELCURRENTLOGCONTROL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELCURRENTLOGLABEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELDATECONTROL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELDATELABEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELDESCRIPTIONBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELENTRY, 
 wxID_SIMPLELOGLOWERINTERFACEPANELENTRYCONTROLPANEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELIDCONTROL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELIDLABEL, 
 wxID_SIMPLELOGLOWERINTERFACEPANELNEWENTRYBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELNEXTENTRYBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELOPENBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELPREVIOUSENTRYBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELREMOVEENTRYBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELSAVEASBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELSAVEBUTTON, 
 wxID_SIMPLELOGLOWERINTERFACEPANELTEXTENTRYPANEL, 
] = [wx.NewId() for _init_ctrls in range(19)]

class SimpleLogLowerInterfacePanel(wx.Panel):
    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.PreviousEntryButton, 0, border=0, flag=0)
        parent.AddWindow(self.NextEntryButton, 0, border=0, flag=0)
        parent.AddWindow(self.IndexLabel, 0, border=0, flag=0)
        parent.AddWindow(self.IndexControl, 0, border=0, flag=0)
        parent.AddWindow(self.DateLabel, 0, border=0, flag=0)
        parent.AddWindow(self.DateControl, 0, border=0, flag=0)
        parent.AddWindow(self.CurrentLogLabel, 0, border=0, flag=0)
        parent.AddWindow(self.CurrentLogControl, 1, border=0, flag=wx.EXPAND)

    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.OpenButton, 1, border=0, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.SaveAsButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)
        parent.AddWindow(self.NewEntryButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)
        parent.AddWindow(self.RemoveEntryButton, 1, border=0,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.SaveButton, 1, border=0,
              flag=wx.LEFT | wx.ALL | wx.EXPAND)
        parent.AddWindow(self.DescriptionButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.ControlsPanel, 0, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.TextEntryPanel, 5, border=2,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.Entry, 1, border=2, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.EntryControlPanel, 0, border=2,
              flag=wx.ALIGN_BOTTOM | wx.EXPAND | wx.ALL)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer4 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)
        self._init_coll_boxSizer4_Items(self.boxSizer4)

        self.SetSizer(self.boxSizer1)
        self.EntryControlPanel.SetSizer(self.boxSizer3)
        self.TextEntryPanel.SetSizer(self.boxSizer2)
        self.ControlsPanel.SetSizer(self.boxSizer4)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_SIMPLELOGLOWERINTERFACEPANEL,
              name=u'SimpleLogLowerInterfacePanel', parent=prnt,
              pos=wx.Point(1610, 283), size=wx.Size(1277, 374),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(1269, 340))

        self.ControlsPanel = wx.Panel(id=wxID_SIMPLELOGLOWERINTERFACEPANELCONTROLSPANEL,
              name=u'ControlsPanel', parent=self, pos=wx.Point(2, 2),
              size=wx.Size(80, 336), style=wx.TAB_TRAVERSAL)

        self.TextEntryPanel = wx.Panel(id=wxID_SIMPLELOGLOWERINTERFACEPANELTEXTENTRYPANEL,
              name=u'TextEntryPanel', parent=self, pos=wx.Point(86, 2),
              size=wx.Size(1181, 336), style=wx.TAB_TRAVERSAL)

        self.EntryControlPanel = wx.Panel(id=wxID_SIMPLELOGLOWERINTERFACEPANELENTRYCONTROLPANEL,
              name=u'EntryControlPanel', parent=self.TextEntryPanel,
              pos=wx.Point(2, 310), size=wx.Size(1177, 24),
              style=wx.TAB_TRAVERSAL)

        self.PreviousEntryButton = wx.BitmapButton(bitmap=wx.Bitmap(str(os.path.join(PYMEASURE_ROOT,'Code/FrontEnds/img/Previous.png')),
              wx.BITMAP_TYPE_PNG),
              id=wxID_SIMPLELOGLOWERINTERFACEPANELPREVIOUSENTRYBUTTON,
              name=u'PreviousEntryButton', parent=self.EntryControlPanel,
              pos=wx.Point(0, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.PreviousEntryButton.SetHelpText(u'Previous Entry')
        self.PreviousEntryButton.Bind(wx.EVT_BUTTON,
              self.OnPreviousEntryButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELPREVIOUSENTRYBUTTON)

        self.NextEntryButton = wx.BitmapButton(bitmap=wx.Bitmap(str(os.path.join(PYMEASURE_ROOT,'Code/FrontEnds/img/Next.png')),
              wx.BITMAP_TYPE_PNG),
              id=wxID_SIMPLELOGLOWERINTERFACEPANELNEXTENTRYBUTTON,
              name=u'NextEntryButton', parent=self.EntryControlPanel,
              pos=wx.Point(24, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.NextEntryButton.SetHelpText(u'Next Entry')
        self.NextEntryButton.Bind(wx.EVT_BUTTON, self.OnNextEntryButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELNEXTENTRYBUTTON)

        self.IndexLabel = wx.StaticText(id=wxID_SIMPLELOGLOWERINTERFACEPANELIDLABEL,
              label=u'Index:', name=u'IndexLabel', parent=self.EntryControlPanel,
              pos=wx.Point(48, 0), size=wx.Size(55, 24), style=wx.ALIGN_CENTRE)
        self.IndexLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'MS Shell Dlg 2'))
        self.IndexLabel.SetHelpText(u'')

        self.IndexControl = wx.TextCtrl(id=wxID_SIMPLELOGLOWERINTERFACEPANELIDCONTROL,
              name=u'IndexControl', parent=self.EntryControlPanel,
              pos=wx.Point(103, 0), size=wx.Size(57, 24), style=0,
              value=u'Entry Number')
        self.IndexControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        self.DateLabel = wx.StaticText(id=wxID_SIMPLELOGLOWERINTERFACEPANELDATELABEL,
              label=u'Date:', name=u'DateLabel', parent=self.EntryControlPanel,
              pos=wx.Point(160, 0), size=wx.Size(55, 24),
              style=wx.ALIGN_CENTRE)
        self.DateLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              u'MS Shell Dlg 2'))

        self.DateControl = wx.TextCtrl(id=wxID_SIMPLELOGLOWERINTERFACEPANELDATECONTROL,
              name=u'DateControl', parent=self.EntryControlPanel,
              pos=wx.Point(215, 0), size=wx.Size(190, 21), style=0,
              value=u'Date Code of Entry')
        self.DateControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, u'MS Shell Dlg 2'))

        self.OpenButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELOPENBUTTON,
              label=u'Open A log', name=u'OpenButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 0), size=wx.Size(80,
              56), style=wx.CAPTION)
        self.OpenButton.SetHelpText(u'')
        self.OpenButton.SetToolTipString(u'OpenButton')
        self.OpenButton.Bind(wx.EVT_BUTTON, self.OnOpenButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELOPENBUTTON)

        self.SaveAsButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELSAVEASBUTTON,
              label=u'Save As', name=u'SaveAsButton', parent=self.ControlsPanel,
              pos=wx.Point(0, 56), size=wx.Size(80, 56), style=0)
        self.SaveAsButton.SetHelpText(u'Save the current log as a different name')
        self.SaveAsButton.Bind(wx.EVT_BUTTON, self.OnSaveAsButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELSAVEASBUTTON)

        self.NewEntryButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELNEWENTRYBUTTON,
              label=u'New Log Entry', name=u'NewEntryButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 112), size=wx.Size(80,
              56), style=0)
        self.NewEntryButton.SetHelpText(u'Add a new entry to the current log')
        self.NewEntryButton.Bind(wx.EVT_BUTTON, self.OnNewEntryButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELNEWENTRYBUTTON)

        self.RemoveEntryButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELREMOVEENTRYBUTTON,
              label=u'Remove Entry', name=u'RemoveEntryButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 168), size=wx.Size(80,
              56), style=0)
        self.RemoveEntryButton.SetHelpText(u'Remove the current entry')
        self.RemoveEntryButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveEntryButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELREMOVEENTRYBUTTON)

        self.SaveButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELSAVEBUTTON,
              label=u'Save', name=u'SaveButton', parent=self.ControlsPanel,
              pos=wx.Point(0, 224), size=wx.Size(80, 56), style=0)
        self.SaveButton.SetHelpText(u'Save the current entry')
        self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSaveButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELSAVEBUTTON)

        self.DescriptionButton = wx.Button(id=wxID_SIMPLELOGLOWERINTERFACEPANELDESCRIPTIONBUTTON,
              label=u'Description', name=u'DescriptionButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 280), size=wx.Size(80,
              56), style=0)
        self.DescriptionButton.SetHelpText(u'Show the log description')
        self.DescriptionButton.Bind(wx.EVT_BUTTON,
              self.OnDescriptionButtonButton,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELDESCRIPTIONBUTTON)

        self.CurrentLogLabel = wx.StaticText(id=wxID_SIMPLELOGLOWERINTERFACEPANELCURRENTLOGLABEL,
              label=u'Current Log:', name=u'CurrentLogLabel',
              parent=self.EntryControlPanel, pos=wx.Point(405, 0),
              size=wx.Size(121, 24), style=wx.ALIGN_CENTRE)
        self.CurrentLogLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, u'MS Shell Dlg 2'))

        self.CurrentLogControl = wx.TextCtrl(id=wxID_SIMPLELOGLOWERINTERFACEPANELCURRENTLOGCONTROL,
              name=u'CurrentLogControl', parent=self.EntryControlPanel,
              pos=wx.Point(526, 0), size=wx.Size(651, 24), style=0,
              value=u'Name of Current Log')
        self.CurrentLogControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, u'MS Shell Dlg 2'))

        self.Entry = wx.TextCtrl(id=wxID_SIMPLELOGLOWERINTERFACEPANELENTRY,
              name=u'Entry', parent=self.TextEntryPanel, pos=wx.Point(2, 2),
              size=wx.Size(1177, 304),
              style=wx.TE_MULTILINE | wx.VSCROLL | wx.TE_LINEWRAP | wx.TE_WORDWRAP,
              value=u'')
        self.Entry.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              u'MS Shell Dlg 2'))
        self.Entry.Bind(wx.EVT_TEXT_ENTER, self.OnEntryTextEnter,
              id=wxID_SIMPLELOGLOWERINTERFACEPANELENTRY)

        self._init_sizers()

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.current_log=XMLModels.XMLLog()
        self.update_controls()
        
    def update_controls(self):
        "Updates the controls with values from the current log"
        try:
            name=os.path.basename(self.current_log.path)
            self.CurrentLogControl.SetValue(name)
            self.IndexControl.SetValue(self.current_log.current_entry['Index'])
            date=self.current_log.current_entry['Date']
            
            self.DateControl.SetValue(convert_datetime(date))
            self.Entry.SetValue(self.current_log.current_entry['Value'])
        except:
            #raise
            pass

    def OnPreviousEntryButtonButton(self, event):
        self.current_log.previous_entry()
        self.update_controls()           
        event.Skip()    

    def OnNextEntryButtonButton(self, event):
        self.current_log.next_entry()
        self.update_controls()  
        event.Skip()             
    def OnOpenButtonButton(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', LOGS_DIRECTORY, '', '*.*', wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                self.current_log=XMLModels.XMLLog(filename)
                #print("{0} is {1}".format('self.current_log',self.current_log))
        finally:
            dlg.Destroy()
        try:
            self.current_log.set_current_entry(-1)
        except: raise
        self.update_controls()
        event.Skip() 
    def OnSaveAsButtonButton(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', LOGS_DIRECTORY, self.current_log.path, '*.*', wx.SAVE)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                self.current_log.save(filename)
               
        finally:
            dlg.Destroy()
        event.Skip() 
    def OnNewEntryButtonButton(self, event):
        self.current_log.add_entry()
        self.update_controls()
        event.Skip() 
    def OnRemoveEntryButtonButton(self, event):
        self.current_log.remove_entry(self.current_log.current_entry['Index'])
        self.current_log.previous_entry()
        self.update_controls()     
        event.Skip() 
    def OnSaveButtonButton(self, event):
        self.current_log.save()
        event.Skip() 
    def OnDescriptionButtonButton(self, event):
        try:
            self.current_log.set_current_entry(-1)
            self.update_controls()
        except KeyError:pass
        event.Skip() 


    def OnEntryTextEnter(self, event):
        text=self.Entry.GetValue()
        self.current_log.edit_entry(self.current_log.current_entry['Index'],
        new_value=text)
        event.Skip() 
        
 
        
                  
        
        
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=SimpleLogLowerInterfacePanel(id=1, name=u'IEPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(200, 800),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()
