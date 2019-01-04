#-----------------------------------------------------------------------------
# Name:        VisaDialog.py
# Purpose:     To communicate with visa compatible instruments
# Author:      Aric Sanders
# Created:     3/02/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" VisaDialog is a very simple dialog for writing and reading commands over GPIB and RS232
Help        box_layout = Layout(align_items='stretch',
                    border='solid',
                    width='50%')
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
#Boa:Dialog:VisaDialog
try:
    import wx
except:
    raise

try:
    import visa
except:
    raise

def create(parent):
    return VisaDialog(parent)

[wxID_VISADIALOG, wxID_VISADIALOGASKBUTTON, wxID_VISADIALOGCOMMANDPANEL, 
 wxID_VISADIALOGINPUTLABEL, wxID_VISADIALOGINSTRUMENTCHOICE, 
 wxID_VISADIALOGINSTRUMENTCHOOSERPANEL, wxID_VISADIALOGINSTRUMENTLABEL, 
 wxID_VISADIALOGREADBUTTON, wxID_VISADIALOGRESPONSELABEL, 
 wxID_VISADIALOGRESPONSETEXT, wxID_VISADIALOGTEXTINPUT, 
 wxID_VISADIALOGTEXTPANEL, wxID_VISADIALOGWRITEBUTTON, 
] = [wx.NewId() for _init_ctrls in range(13)]

class VisaDialog(wx.Dialog):
    def _init_coll_LabelSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.InputLabel, 1, border=2, flag=wx.GROW | wx.EXPAND)
        parent.Add(self.ResponseLabel, 1, border=2,
              flag=wx.GROW | wx.EXPAND)

    def _init_coll_InstrumentChooserSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.InstrumentLabel, 1, border=1,
              flag=wx.ALIGN_CENTER_VERTICAL | wx.GROW | wx.EXPAND | wx.ALIGN_RIGHT)
        parent.Add(self.InstrumentChoice, 1, border=4,
              flag=wx.EXPAND | wx.LEFT)
        parent.Add(self.LabelSizer, 1, border=0,
              flag=wx.BOTTOM | wx.EXPAND)

    def _init_coll_CommandSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.ButtonSizer1, 0, border=0, flag=wx.ALIGN_CENTER)
        parent.Add(self.AskButton, 0, border=0, flag=wx.ALIGN_CENTER)

    def _init_coll_TextPanelSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.TextInput, 1, border=0, flag=wx.EXPAND)
        parent.Add(self.ResponseText, 1, border=1, flag=wx.EXPAND)

    def _init_coll_ButtonSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.WriteButton, 0, border=0, flag=0)
        parent.Add(self.ReadButton, 0, border=0, flag=0)

    def _init_coll_DialogSizer_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.InstrumentChooserPanel, 4, border=1,
              flag=wx.ALL | wx.EXPAND)
        parent.Add(self.TextPanel, 9, border=1, flag=wx.GROW | wx.EXPAND)
        parent.Add(self.CommandPanel, 3, border=2,
              flag=wx.GROW | wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.DialogSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.TextPanelSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.InstrumentChooserSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.CommandSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.ButtonSizer1 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.LabelSizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self._init_coll_DialogSizer_Items(self.DialogSizer)
        self._init_coll_TextPanelSizer_Items(self.TextPanelSizer)
        self._init_coll_InstrumentChooserSizer_Items(self.InstrumentChooserSizer)
        self._init_coll_CommandSizer_Items(self.CommandSizer)
        self._init_coll_ButtonSizer1_Items(self.ButtonSizer1)
        self._init_coll_LabelSizer_Items(self.LabelSizer)

        self.SetSizer(self.DialogSizer)
        self.TextPanel.SetSizer(self.TextPanelSizer)
        self.InstrumentChooserPanel.SetSizer(self.InstrumentChooserSizer)
        self.CommandPanel.SetSizer(self.CommandSizer)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_VISADIALOG, name='VisaDialog',
              parent=prnt, pos=wx.Point(366, 357), size=wx.Size(966, 336),
              style=wx.DEFAULT_DIALOG_STYLE,
              title='Visa Communication Window')
        self.SetClientSize(wx.Size(958, 302))
        self.SetHelpText('')

        self.InstrumentChooserPanel = wx.Panel(id=wxID_VISADIALOGINSTRUMENTCHOOSERPANEL,
              name='InstrumentChooserPanel', parent=self, pos=wx.Point(1, 1),
              size=wx.Size(956, 73), style=wx.TAB_TRAVERSAL)

        self.TextPanel = wx.Panel(id=wxID_VISADIALOGTEXTPANEL,
              name='TextPanel', parent=self, pos=wx.Point(0, 75),
              size=wx.Size(958, 170), style=wx.TAB_TRAVERSAL)

        self.CommandPanel = wx.Panel(id=wxID_VISADIALOGCOMMANDPANEL,
              name='CommandPanel', parent=self, pos=wx.Point(0, 245),
              size=wx.Size(958, 57), style=wx.TAB_TRAVERSAL)

        self.InstrumentChoice = wx.Choice(choices=[],
              id=wxID_VISADIALOGINSTRUMENTCHOICE, name='InstrumentChoice',
              parent=self.InstrumentChooserPanel, pos=wx.Point(4, 24),
              size=wx.Size(952, 21), style=wx.SUNKEN_BORDER)
        self.InstrumentChoice.SetHelpText('Choose Instrument')
        self.InstrumentChoice.Bind(wx.EVT_CHOICE, self.OnInstrumentChoiceChoice,
              id=wxID_VISADIALOGINSTRUMENTCHOICE)

        self.TextInput = wx.TextCtrl(id=wxID_VISADIALOGTEXTINPUT,
              name='TextInput', parent=self.TextPanel, pos=wx.Point(0, 0),
              size=wx.Size(479, 170), style=wx.RAISED_BORDER ,
              value='Input Command Here')
        self.TextInput.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.ResponseText = wx.TextCtrl(id=wxID_VISADIALOGRESPONSETEXT,
              name='ResponseText', parent=self.TextPanel, pos=wx.Point(479, 0),
              size=wx.Size(479, 170),
              style=wx.RAISED_BORDER  | wx.TE_MULTILINE,
              value='Instrument Response')
        self.ResponseText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.WriteButton = wx.Button(id=wxID_VISADIALOGWRITEBUTTON,
              label='Write', name='WriteButton', parent=self.CommandPanel,
              pos=wx.Point(404, 0), size=wx.Size(75, 23), style=0)
        self.WriteButton.Bind(wx.EVT_BUTTON, self.OnWriteButtonButton,
              id=wxID_VISADIALOGWRITEBUTTON)

        self.ReadButton = wx.Button(id=wxID_VISADIALOGREADBUTTON, label='Read',
              name='ReadButton', parent=self.CommandPanel, pos=wx.Point(479,
              0), size=wx.Size(75, 23), style=0)
        self.ReadButton.Bind(wx.EVT_BUTTON, self.OnReadButtonButton,
              id=wxID_VISADIALOGREADBUTTON)

        self.AskButton = wx.Button(id=wxID_VISADIALOGASKBUTTON, label='Ask',
              name='AskButton', parent=self.CommandPanel, pos=wx.Point(441,
              23), size=wx.Size(75, 23), style=0)
        self.AskButton.Bind(wx.EVT_BUTTON, self.OnAskButtonButton,
              id=wxID_VISADIALOGASKBUTTON)

        self.InputLabel = wx.StaticText(id=wxID_VISADIALOGINPUTLABEL,
              label='Command Written to Instrument', name='InputLabel',
              parent=self.InstrumentChooserPanel, pos=wx.Point(0, 48),
              size=wx.Size(478, 25), style=0)
        self.InputLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.ResponseLabel = wx.StaticText(id=wxID_VISADIALOGRESPONSELABEL,
              label='Response', name='ResponseLabel',
              parent=self.InstrumentChooserPanel, pos=wx.Point(478, 48),
              size=wx.Size(478, 25), style=0)
        self.ResponseLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'MS Shell Dlg 2'))

        self.InstrumentLabel = wx.StaticText(id=wxID_VISADIALOGINSTRUMENTLABEL,
              label='Instrument', name='InstrumentLabel',
              parent=self.InstrumentChooserPanel, pos=wx.Point(0, 0),
              size=wx.Size(956, 24), style=0)
        self.InstrumentLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD,
              False, 'MS Shell Dlg 2'))

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        # Look for visa instruments
        self.resource_manager=visa.ResourceManager()

        self.instrument_list=self.resource_manager.list_resources()
        for instrument in self.instrument_list:
            self.InstrumentChoice.Append(instrument)

    def OnInstrumentChoiceChoice(self, event):
        
        address=self.InstrumentChoice.GetStringSelection()
        #print address
        self.active_instrument=self.resource_manager.open_resource(address)
        event.Skip()

    def OnWriteButtonButton(self, event):
        self.active_instrument.write(self.TextInput.GetValue())
        event.Skip()

    def OnReadButtonButton(self, event):
        text=self.active_instrument.read()
        self.ResponseText.SetValue(text)
        event.Skip()

    def OnAskButtonButton(self, event):
        input=self.TextInput.GetValue()
        output=self.active_instrument.query(input)
        self.ResponseText.SetValue(output)
        event.Skip()


if __name__ == '__main__':
    app = wx.App()
    dlg = create(None)
    try:
        dlg.ShowModal()
    finally:
        dlg.Destroy()
    app.MainLoop()
