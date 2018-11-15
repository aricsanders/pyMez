#Boa:FramePanel:KeithleyIVPanel



#-----------------------------------------------------------------------------
# Name:        KeithleyIVPanel.py
# Purpose:     A Front End for taking IV's with the Keithley
#
# Author:      Aric Sanders
#
# Created:     2016/06/27
# RCS-ID:      $Id: KeithleyIVPanel.py $
# Licence:     MIT
#-----------------------------------------------------------------------------


""" KeithleyIVPanel is a GUI class for taking IV's with the Keithley piccoammeter
Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-------------------------------------------------------------------------------
# Standard Imports
import wx
import sys
import os

#-------------------------------------------------------------------------------
#Thid Party Imports
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    from Code.InstrumentControl.Experiments import *
except:
    print('There was an error importing pyMez')
IMAGE_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'img')

[wxID_KEITHLEYIVPANEL, wxID_KEITHLEYIVPANELACTIONPANEL, 
 wxID_KEITHLEYIVPANELAQUISTIONCONTROLPANEL, 
 wxID_KEITHLEYIVPANELAQUISTIONLABELPANEL, 
 wxID_KEITHLEYIVPANELAQUISTIONPARAMETERPANEL, 
 wxID_KEITHLEYIVPANELBOWTIECONTROL, wxID_KEITHLEYIVPANELBOWTIELABEL, 
 wxID_KEITHLEYIVPANELINFORMATIONPANEL, wxID_KEITHLEYIVPANELIVBUTTON, 
 wxID_KEITHLEYIVPANELNOTESCONTROL, wxID_KEITHLEYIVPANELNOTESLABEL, 
 wxID_KEITHLEYIVPANELNOTESPANEL, wxID_KEITHLEYIVPANELNUMBEROFPOINTSCONTROL, 
 wxID_KEITHLEYIVPANELNUMBEROFPOINTSLABEL, wxID_KEITHLEYIVPANELPANEL1, 
 wxID_KEITHLEYIVPANELPLOTBUTTON, wxID_KEITHLEYIVPANELRESISTANCECONTROL, 
 wxID_KEITHLEYIVPANELRESISTANCELABEL, wxID_KEITHLEYIVPANELSAMPLENAMECONTROL, 
 wxID_KEITHLEYIVPANELSAMPLENAMELABEL, wxID_KEITHLEYIVPANELSAVEBUTTON, 
 wxID_KEITHLEYIVPANELSETTLETIMECONTROL, wxID_KEITHLEYIVPANELSETTLETIMELABEL, 
 wxID_KEITHLEYIVPANELSTARTCONTROL, wxID_KEITHLEYIVPANELSTARTLABEL, 
 wxID_KEITHLEYIVPANELSTOPCONTROL, wxID_KEITHLEYIVPANELSTOPLABEL, 
] = [wx.NewId() for _init_ctrls in range(27)]

class KeithleyIVPanel(wx.Panel):
    def _init_coll_AquistionLabelSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.StartLabel, 1, border=1,
              flag=wx.EXPAND | wx.ALIGN_CENTER)
        parent.AddWindow(self.StopLabel, 1, border=1,
              flag=wx.EXPAND | wx.ALIGN_CENTER)
        parent.AddWindow(self.NumberOfPointsLabel, 1, border=1,
              flag=wx.ALIGN_CENTER | wx.EXPAND)
        parent.AddWindow(self.SettleTimeLabel, 1, border=1,
              flag=wx.ALIGN_CENTER | wx.EXPAND)
        parent.AddWindow(self.BowtieLabel, 1, border=1,
              flag=wx.EXPAND | wx.ALIGN_CENTER)

    def _init_coll_AquistionControlSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.StartControl, 1, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.StopControl, 1, border=0, flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.NumberOfPointsControl, 1, border=0,
              flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.SettleTimeControl, 1, border=0,
              flag=wx.ALIGN_CENTER)
        parent.AddWindow(self.BowtieControl, 1, border=0, flag=wx.ALIGN_CENTER)

    def _init_coll_AquistionParameterSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.AquistionLabelPanel, 1, border=1,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.AquistionControlPanel, 1, border=1,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_PanelSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.InformationPanel, 2, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.AquistionParameterPanel, 1, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.ActionPanel, 1, border=2, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.NotesPanel, 4, border=2, flag=wx.ALL | wx.EXPAND)

    def _init_coll_ActionSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.IVButton, 1, border=5, flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.SaveButton, 1, border=5, flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.PlotButton, 1, border=5, flag=wx.ALL | wx.EXPAND)

    def _init_coll_NotesSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.NotesLabel, 0, border=0, flag=0)
        parent.AddWindow(self.NotesControl, 1, border=2,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_InformationSizer_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.SampleNameLabel, 0, border=0, flag=0)
        parent.AddWindow(self.SampleNameControl, 0, border=0, flag=0)
        parent.AddWindow(self.panel1, 0, border=0, flag=0)
        parent.AddWindow(self.ResistanceLabel, 0, border=0, flag=0)
        parent.AddWindow(self.ResistanceControl, 0, border=0, flag=0)

    def _init_sizers(self):
        # generated method, don't edit
        self.PanelSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.InformationSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.AquistionParameterSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.ActionSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.NotesSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.AquistionLabelSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.AquistionControlSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_PanelSizer_Items(self.PanelSizer)
        self._init_coll_InformationSizer_Items(self.InformationSizer)
        self._init_coll_AquistionParameterSizer_Items(self.AquistionParameterSizer)
        self._init_coll_ActionSizer_Items(self.ActionSizer)
        self._init_coll_NotesSizer_Items(self.NotesSizer)
        self._init_coll_AquistionLabelSizer_Items(self.AquistionLabelSizer)
        self._init_coll_AquistionControlSizer_Items(self.AquistionControlSizer)

        self.SetSizer(self.PanelSizer)
        self.InformationPanel.SetSizer(self.InformationSizer)
        self.NotesPanel.SetSizer(self.NotesSizer)
        self.AquistionControlPanel.SetSizer(self.AquistionControlSizer)
        self.AquistionLabelPanel.SetSizer(self.AquistionLabelSizer)
        self.ActionPanel.SetSizer(self.ActionSizer)
        self.AquistionParameterPanel.SetSizer(self.AquistionParameterSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_KEITHLEYIVPANEL,
              name='KeithleyIVPanel', parent=prnt, pos=wx.Point(341, 397),
              size=wx.Size(768, 643), style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(760, 609))
        self.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.InformationPanel = wx.Panel(id=wxID_KEITHLEYIVPANELINFORMATIONPANEL,
              name='InformationPanel', parent=self, pos=wx.Point(2, 2),
              size=wx.Size(756, 148), style=wx.TAB_TRAVERSAL)

        self.AquistionParameterPanel = wx.Panel(id=wxID_KEITHLEYIVPANELAQUISTIONPARAMETERPANEL,
              name='AquistionParameterPanel', parent=self, pos=wx.Point(2,
              154), size=wx.Size(756, 72), style=wx.TAB_TRAVERSAL)

        self.ActionPanel = wx.Panel(id=wxID_KEITHLEYIVPANELACTIONPANEL,
              name='ActionPanel', parent=self, pos=wx.Point(2, 230),
              size=wx.Size(756, 72), style=wx.TAB_TRAVERSAL)
        self.ActionPanel.SetBackgroundColour(wx.Colour(143, 133, 69))

        self.NotesPanel = wx.Panel(id=wxID_KEITHLEYIVPANELNOTESPANEL,
              name='NotesPanel', parent=self, pos=wx.Point(2, 306),
              size=wx.Size(756, 300), style=wx.TAB_TRAVERSAL)

        self.NotesLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELNOTESLABEL,
              label='Notes:', name='NotesLabel', parent=self.NotesPanel,
              pos=wx.Point(0, 0), size=wx.Size(35, 13), style=0)
        self.NotesLabel.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))

        self.NotesControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELNOTESCONTROL,
              name='NotesControl', parent=self.NotesPanel, pos=wx.Point(2, 15),
              size=wx.Size(752, 283), style=wx.VSCROLL | wx.TE_MULTILINE,
              value='')

        self.IVButton = wx.Button(id=wxID_KEITHLEYIVPANELIVBUTTON,
              label='Take IV', name='IVButton', parent=self.ActionPanel,
              pos=wx.Point(5, 5), size=wx.Size(242, 62), style=0)
        self.IVButton.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.IVButton.Bind(wx.EVT_BUTTON, self.OnIVButtonButton,
              id=wxID_KEITHLEYIVPANELIVBUTTON)

        self.SaveButton = wx.Button(id=wxID_KEITHLEYIVPANELSAVEBUTTON,
              label='Save Data', name='SaveButton', parent=self.ActionPanel,
              pos=wx.Point(257, 5), size=wx.Size(242, 62), style=0)
        self.SaveButton.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.SaveButton.Bind(wx.EVT_BUTTON, self.OnSaveButtonButton,
              id=wxID_KEITHLEYIVPANELSAVEBUTTON)

        self.PlotButton = wx.Button(id=wxID_KEITHLEYIVPANELPLOTBUTTON,
              label='Plot Data', name='PlotButton', parent=self.ActionPanel,
              pos=wx.Point(509, 5), size=wx.Size(242, 62), style=0)
        self.PlotButton.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD, False,
              'MS Shell Dlg 2'))
        self.PlotButton.Bind(wx.EVT_BUTTON, self.OnPlotButtonButton,
              id=wxID_KEITHLEYIVPANELPLOTBUTTON)

        self.SampleNameLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELSAMPLENAMELABEL,
              label='Sample Name:', name='SampleNameLabel',
              parent=self.InformationPanel, pos=wx.Point(0, 0),
              size=wx.Size(104, 19), style=0)
        self.SampleNameLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.SampleNameControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELSAMPLENAMECONTROL,
              name='SampleNameControl', parent=self.InformationPanel,
              pos=wx.Point(104, 0), size=wx.Size(344, 21), style=0, value='')

        self.AquistionLabelPanel = wx.Panel(id=wxID_KEITHLEYIVPANELAQUISTIONLABELPANEL,
              name='AquistionLabelPanel', parent=self.AquistionParameterPanel,
              pos=wx.Point(1, 1), size=wx.Size(754, 34),
              style=wx.TAB_TRAVERSAL)

        self.AquistionControlPanel = wx.Panel(id=wxID_KEITHLEYIVPANELAQUISTIONCONTROLPANEL,
              name='AquistionControlPanel',
              parent=self.AquistionParameterPanel, pos=wx.Point(1, 37),
              size=wx.Size(754, 34), style=wx.TAB_TRAVERSAL)
        self.AquistionControlPanel.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.StartLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELSTARTLABEL,
              label='Start', name='StartLabel',
              parent=self.AquistionLabelPanel, pos=wx.Point(0, 0),
              size=wx.Size(150, 34), style=wx.SIMPLE_BORDER | wx.ALIGN_CENTRE)
        self.StartLabel.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.StartLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.StopLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELSTOPLABEL,
              label='Stop', name='StopLabel', parent=self.AquistionLabelPanel,
              pos=wx.Point(150, 0), size=wx.Size(150, 34),
              style=wx.SIMPLE_BORDER | wx.ALIGN_CENTRE)
        self.StopLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.NumberOfPointsLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELNUMBEROFPOINTSLABEL,
              label='Number of Points', name='NumberOfPointsLabel',
              parent=self.AquistionLabelPanel, pos=wx.Point(300, 0),
              size=wx.Size(150, 34), style=wx.ALIGN_CENTRE | wx.SIMPLE_BORDER)
        self.NumberOfPointsLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL,
              wx.NORMAL, False, 'MS Shell Dlg 2'))
        self.NumberOfPointsLabel.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.SettleTimeLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELSETTLETIMELABEL,
              label='Settle Time', name='SettleTimeLabel',
              parent=self.AquistionLabelPanel, pos=wx.Point(450, 0),
              size=wx.Size(150, 34), style=wx.ALIGN_CENTRE | wx.SIMPLE_BORDER)
        self.SettleTimeLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.BowtieLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELBOWTIELABEL,
              label='Bowtie Sweep', name='BowtieLabel',
              parent=self.AquistionLabelPanel, pos=wx.Point(600, 0),
              size=wx.Size(150, 34), style=wx.ALIGN_CENTRE | wx.SIMPLE_BORDER)
        self.BowtieLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.StartControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELSTARTCONTROL,
              name='StartControl', parent=self.AquistionControlPanel,
              pos=wx.Point(0, 6), size=wx.Size(150, 21), style=wx.CAPTION,
              value='-.1')

        self.StopControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELSTOPCONTROL,
              name='StopControl', parent=self.AquistionControlPanel,
              pos=wx.Point(150, 6), size=wx.Size(150, 21), style=0,
              value='.1')

        self.NumberOfPointsControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELNUMBEROFPOINTSCONTROL,
              name='NumberOfPointsControl', parent=self.AquistionControlPanel,
              pos=wx.Point(300, 6), size=wx.Size(150, 21), style=0,
              value='10')

        self.SettleTimeControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELSETTLETIMECONTROL,
              name='SettleTimeControl', parent=self.AquistionControlPanel,
              pos=wx.Point(450, 6), size=wx.Size(150, 21), style=0,
              value='.2')

        self.BowtieControl = wx.CheckBox(id=wxID_KEITHLEYIVPANELBOWTIECONTROL,
              label='Bowtie', name='BowtieControl',
              parent=self.AquistionControlPanel, pos=wx.Point(600, 10),
              size=wx.Size(150, 13), style=0)
        self.BowtieControl.SetValue(False)

        self.ResistanceLabel = wx.StaticText(id=wxID_KEITHLEYIVPANELRESISTANCELABEL,
              label='Resistance', name='ResistanceLabel',
              parent=self.InformationPanel, pos=wx.Point(544, 0),
              size=wx.Size(73, 19), style=0)
        self.ResistanceLabel.Enable(True)
        self.ResistanceLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.ResistanceControl = wx.TextCtrl(id=wxID_KEITHLEYIVPANELRESISTANCECONTROL,
              name='ResistanceControl', parent=self.InformationPanel,
              pos=wx.Point(617, 0), size=wx.Size(100, 21), style=0, value='')

        self.panel1 = wx.Panel(id=wxID_KEITHLEYIVPANELPANEL1, name='panel1',
              parent=self.InformationPanel, pos=wx.Point(448, 0),
              size=wx.Size(96, 24), style=wx.TAB_TRAVERSAL)

        self._init_sizers()

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        self.experiment=KeithleyIV()

    def OnIVButtonButton(self, event):
        try:
            [start,stop,number_points,settling_time,bowtie]=[float(self.StartControl.GetValue()),
            float(self.StopControl.GetValue()),int(self.NumberOfPointsControl.GetValue()),
            float(self.SettleTimeControl.GetValue()),self.BowtieControl.GetValue()]
            #print(start,stop,number_points,settle_time,bowtie)
            voltage_list=self.experiment.make_voltage_list(start,stop,number_points,bowtie)
            #print(voltage_list)
            try:
                self.experiment.initialize_keithley()
                if self.experiment.instrument.fake_mode:
                    raise
                self.experiment.take_IV(voltage_list,settle_time=settling_time)
            except:
                text='Entering fake mode, keithley did not respond fake R=12000.1'
                print(text)
                self.NotesControl.SetValue(text)
                self.NotesControl.SetBackgroundColour(wx.Colour(192, 0, 0))
                fake_list=voltage_list
                for index,voltage in enumerate(fake_list):
                    current=voltage/12000.1
                    self.experiment.data_list.append({'Index':index,'Voltage':voltage,'Current':current})      
            self.experiment.calculate_resistance()
            self.ResistanceControl.SetValue(str(self.experiment.resistance))
            dlg = wx.MessageDialog(self, 'IV is Done!', 'IV Finished', wx.OK | wx.ICON_INFORMATION)
            try:
                result = dlg.ShowModal()
            finally:
                dlg.Destroy()
 
        except:
            raise
            print("IV Button Failure")
        
        
        event.Skip()

    def OnSaveButtonButton(self, event):
        self.experiment.notes=self.NotesControl.GetValue()
        self.experiment.name=self.SampleNameControl.GetValue()
        self.experiment.save_data()
        event.Skip()

    def OnPlotButtonButton(self, event):
        self.experiment.plot_data()
        event.Skip()



def test_KeithleyIVPanel():
    app = wx.PySimpleApp()
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=KeithleyIVPanel(id=1, name='IV Panel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(200, 800),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()    
    
    
    
if __name__ == '__main__':
    test_KeithleyIVPanel()
