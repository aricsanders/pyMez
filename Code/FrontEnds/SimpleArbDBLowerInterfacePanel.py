#-----------------------------------------------------------------------------
# Name:        SimpleLogLowerInterfacePanel.py
# Purpose:     
#
# Author:      <your name>
#
# Created:     2010/05/11
# RCS-ID:      $Id: SimpleLogLowerInterfacePanel.py $
# Copyright:   (c) 2006
# Licence:     <your licence>
#-----------------------------------------------------------------------------
#Boa:FramePanel:SimpleArbDBLowerInterfacePanel
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
    import pyMez.Code.DataHandlers.XMLModels as Logs
except:
    print("""This module requires  pyMez.Code.DataHandlers.Logs to operate properly,
            add the directory directly above pyMez to sys.path""")  
import wx
import wx.stc

PYMEASURE_ROOT=os.path.dirname(os.path.realpath(pyMez.__file__))
LOGS_DIRECTORY=os.path.join(PYMEASURE_ROOT,'Data','Logs')
IMAGE_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'img')

def convert_datetime(ISO_datetime_string,format_string='%m/%d/%Y at %H:%M:%S'):
    "Converts from long ISO format 2010-05-13T21:54:25.755000 to something reasonable"
    #strip any thing smaller than a second
    time_seconds=ISO_datetime_string.split('.')[0]
    
    #then get it into a datetime format
    time_datetime=datetime.datetime.strptime(time_seconds,"%Y-%m-%dT%H:%M:%S")
    return time_datetime.strftime(format_string)

[wxID_SIMPLEARBDBLOWERINTERFACEPANEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELCONTROLSPANEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTFILEREGISTERCONTROL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTLOGLABEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTMETADATACONTROL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTMETADATLABEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELDATECONTROL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELDATELABEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELDESCRIPTIONBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELENTRY, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELENTRYCONTROLPANEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELIDCONTROL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELIDLABEL, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELNEWENTRYBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELNEXTENTRYBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELOPENBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELPREVIOUSENTRYBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELREMOVEENTRYBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEASBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEBUTTON, 
 wxID_SIMPLEARBDBLOWERINTERFACEPANELTEXTENTRYPANEL, 
] = [wx.NewId() for _init_ctrls in range(21)]

class SimpleArbDBLowerInterfacePanel(wx.Panel):
    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.PreviousEntryButton, 0, border=0, flag=0)
        parent.Add(self.NextEntryButton, 0, border=0, flag=0)
        parent.Add(self.IdLabel, 0, border=0, flag=0)
        parent.Add(self.IdControl, 0, border=0, flag=0)
        parent.Add(self.DateLabel, 0, border=0, flag=0)
        parent.Add(self.DateControl, 0, border=0, flag=0)
        parent.Add(self.CurrentLogLabel, 0, border=0, flag=0)
        parent.Add(self.CurrentFileRegisterControl, 1, border=0,
              flag=wx.EXPAND)
        parent.Add(self.CurrentMetadatLabel, 0, border=0, flag=0)
        parent.Add(self.CurrentMetadataControl, 1, border=0,
              flag=wx.EXPAND)

    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.OpenButton, 1, border=0, flag=wx.ALL | wx.EXPAND)
        parent.Add(self.SaveAsButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)
        parent.Add(self.NewEntryButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)
        parent.Add(self.RemoveEntryButton, 1, border=0,
              flag=wx.ALL | wx.EXPAND)
        parent.Add(self.SaveButton, 1, border=0,
              flag=wx.LEFT | wx.ALL | wx.EXPAND)
        parent.Add(self.DescriptionButton, 1, border=0,
              flag=wx.ALIGN_LEFT | wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.ControlsPanel, 0, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.Add(self.TextEntryPanel, 5, border=2,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.Entry, 1, border=2, flag=wx.ALL | wx.EXPAND)
        parent.Add(self.EntryControlPanel, 0, border=2,
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
        wx.Panel.__init__(self, id=wxID_SIMPLEARBDBLOWERINTERFACEPANEL,
              name='SimpleArbDBLowerInterfacePanel', parent=prnt,
              pos=wx.Point(199, 316), size=wx.Size(1277, 374),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(1269, 340))

        self.ControlsPanel = wx.Panel(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELCONTROLSPANEL,
              name='ControlsPanel', parent=self, pos=wx.Point(2, 2),
              size=wx.Size(80, 336), style=wx.TAB_TRAVERSAL)

        self.TextEntryPanel = wx.Panel(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELTEXTENTRYPANEL,
              name='TextEntryPanel', parent=self, pos=wx.Point(86, 2),
              size=wx.Size(1181, 336), style=wx.TAB_TRAVERSAL)

        self.EntryControlPanel = wx.Panel(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELENTRYCONTROLPANEL,
              name='EntryControlPanel', parent=self.TextEntryPanel,
              pos=wx.Point(2, 310), size=wx.Size(1177, 24),
              style=wx.TAB_TRAVERSAL)

        self.PreviousEntryButton = wx.BitmapButton(bitmap=wx.Bitmap(str(os.path.join(IMAGE_DIRECTORY,'Previous.png')),
              wx.BITMAP_TYPE_PNG),
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELPREVIOUSENTRYBUTTON,
              name='PreviousEntryButton', parent=self.EntryControlPanel,
              pos=wx.Point(0, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.PreviousEntryButton.SetHelpText('Previous Entry')
        self.PreviousEntryButton.Bind(wx.EVT_BUTTON,
              self.OnPreviousEntryButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELPREVIOUSENTRYBUTTON)

        self.NextEntryButton = wx.BitmapButton(bitmap=wx.Bitmap(str(os.path.join(IMAGE_DIRECTORY,'Next.png')),
              wx.BITMAP_TYPE_PNG),
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELNEXTENTRYBUTTON,
              name='NextEntryButton', parent=self.EntryControlPanel,
              pos=wx.Point(24, 0), size=wx.Size(24, 24), style=wx.BU_AUTODRAW)
        self.NextEntryButton.SetHelpText('Next Entry')
        self.NextEntryButton.Bind(wx.EVT_BUTTON, self.OnNextEntryButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELNEXTENTRYBUTTON)

        self.IdLabel = wx.StaticText(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELIDLABEL,
              label='Id:', name='IdLabel', parent=self.EntryControlPanel,
              pos=wx.Point(48, 0), size=wx.Size(55, 24), style=wx.ALIGN_CENTRE)
        self.IdLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.IdLabel.SetHelpText('')

        self.IdControl = wx.TextCtrl(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELIDCONTROL,
              name='IdControl', parent=self.EntryControlPanel,
              pos=wx.Point(103, 0), size=wx.Size(97, 24), style=0, value='Id')
        self.IdControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.DateLabel = wx.StaticText(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELDATELABEL,
              label='Date:', name='DateLabel', parent=self.EntryControlPanel,
              pos=wx.Point(200, 0), size=wx.Size(55, 24),
              style=wx.ALIGN_CENTRE)
        self.DateLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.DateControl = wx.TextCtrl(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELDATECONTROL,
              name='DateControl', parent=self.EntryControlPanel,
              pos=wx.Point(255, 0), size=wx.Size(190, 21), style=0,
              value='Date Code of Entry')
        self.DateControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.OpenButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELOPENBUTTON,
              label='Open Files', name='OpenButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 0), size=wx.Size(80,
              56), style=wx.CAPTION)
        self.OpenButton.SetHelpText('')
        self.OpenButton.SetToolTipString('OpenButton')
        self.OpenButton.Bind(wx.EVT_BUTTON, self.OnOpenButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELOPENBUTTON)

        self.SaveAsButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEASBUTTON,
              label='Save As', name='SaveAsButton', parent=self.ControlsPanel,
              pos=wx.Point(0, 56), size=wx.Size(80, 56), style=0)
        self.SaveAsButton.SetHelpText('Save the current log as a different name')
        self.SaveAsButton.Bind(wx.EVT_BUTTON, self.OnSaveAsButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEASBUTTON)

        self.NewEntryButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELNEWENTRYBUTTON,
              label='New Log Entry', name='NewEntryButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 112), size=wx.Size(80,
              56), style=0)
        self.NewEntryButton.SetHelpText('Add a new entry to the current log')
        self.NewEntryButton.Bind(wx.EVT_BUTTON, self.OnNewEntryButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELNEWENTRYBUTTON)

        self.RemoveEntryButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELREMOVEENTRYBUTTON,
              label='Remove Entry', name='RemoveEntryButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 168), size=wx.Size(80,
              56), style=0)
        self.RemoveEntryButton.SetHelpText('Remove the current entry')
        self.RemoveEntryButton.Bind(wx.EVT_BUTTON,
              self.OnRemoveEntryButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELREMOVEENTRYBUTTON)

        self.SaveButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEBUTTON,
              label='Save', name='SaveButton', parent=self.ControlsPanel,
              pos=wx.Point(0, 224), size=wx.Size(80, 56), style=0)
        self.SaveButton.SetHelpText('Save the current entry')
        self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSaveButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELSAVEBUTTON)

        self.DescriptionButton = wx.Button(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELDESCRIPTIONBUTTON,
              label='Description', name='DescriptionButton',
              parent=self.ControlsPanel, pos=wx.Point(0, 280), size=wx.Size(80,
              56), style=0)
        self.DescriptionButton.SetHelpText('Show the log description')
        self.DescriptionButton.Bind(wx.EVT_BUTTON,
              self.OnDescriptionButtonButton,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELDESCRIPTIONBUTTON)

        self.CurrentLogLabel = wx.StaticText(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTLOGLABEL,
              label='Current File Registry:', name='CurrentLogLabel',
              parent=self.EntryControlPanel, pos=wx.Point(445, 0),
              size=wx.Size(185, 19), style=wx.ALIGN_CENTRE)
        self.CurrentLogLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'MS Shell Dlg 2'))

        self.CurrentFileRegisterControl = wx.TextCtrl(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTFILEREGISTERCONTROL,
              name='CurrentFileRegisterControl', parent=self.EntryControlPanel,
              pos=wx.Point(630, 0), size=wx.Size(178, 24), style=0,
              value='Name of File Registry ')
        self.CurrentFileRegisterControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'MS Shell Dlg 2'))

        self.Entry = wx.TextCtrl(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELENTRY,
              name='Entry', parent=self.TextEntryPanel, pos=wx.Point(2, 2),
              size=wx.Size(1177, 304),
              value='')
        self.Entry.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False,
              'MS Shell Dlg 2'))
        self.Entry.Bind(wx.EVT_TEXT_ENTER, self.OnEntryTextEnter,
              id=wxID_SIMPLEARBDBLOWERINTERFACEPANELENTRY)

        self.CurrentMetadatLabel = wx.StaticText(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTMETADATLABEL,
              label='Current Metadata File: ', name='CurrentMetadatLabel',
              parent=self.EntryControlPanel, pos=wx.Point(808, 0),
              size=wx.Size(190, 19), style=0)
        self.CurrentMetadatLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL,
              wx.BOLD, False, 'MS Shell Dlg 2'))

        self.CurrentMetadataControl = wx.TextCtrl(id=wxID_SIMPLEARBDBLOWERINTERFACEPANELCURRENTMETADATACONTROL,
              name='CurrentMetadataControl', parent=self.EntryControlPanel,
              pos=wx.Point(998, 0), size=wx.Size(179, 24), style=0,
              value='Name of Metadata File')
        self.CurrentMetadataControl.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'MS Shell Dlg 2'))

        self._init_sizers()

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.current_log=Logs.XMLLog()
        self.update_controls()
        
    def update_controls(self):
        "Updates the controls with values from the current log"
        try:
            name=os.path.basename(self.current_log.path)
            self.CurrentLogControl.SetValue(name)
            self.IdControl.SetValue(self.current_log.current_entry['Id'])
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
                self.current_log=Logs.XMLLog(filename)
        finally:
            dlg.Destroy()
        try:
            self.current_log.set_current_entry(-1)
        except: pass
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
        self.current_log.remove_entry(self.current_log.current_entry['Id'])
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
        self.current_log.edit_entry(self.current_log.current_entry['Id'],
        new_value=text)
        event.Skip() 
        
 
        
                  
        
        
        
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=SimpleArbDBLowerInterfacePanel(id=1, name='IEPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(200, 800),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()
