#-----------------------------------------------------------------------------
# Name:        AdvancedInterfaceFrame.py
# Purpose:     An advanced frame design that includes control and interface areas
# and all of the standard menu,tool and status bars.
#
# Author:      Aric Sanders
#
# Created:     2010/04/20
# RCS-ID:      $Id: AdvancedInterfaceFrame.py $
#-----------------------------------------------------------------------------
#Boa:Frame:AdvancedInterfaceFrame
""" Advanced wx.Frame with standard containers for interface and control this
is meant as a template for GUI design and a test bed for pyMez

Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""
import sys
import os
import wx
from types import *
import re
import copy
# Add pyMez to sys.path (this allows imports that don't go through pyMez/__init__.py
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    #import pyMez
    from Code.FrontEnds.IEPanel import *
    from Code.FrontEnds.EndOfDayDialog import *
    #from Code.FrontEnds.ShellPanel import *
    from Code.FrontEnds.SimpleLogLowerInterfacePanel import *
    from Code.FrontEnds.SimpleArbDBLowerInterfacePanel import *
    from Code.FrontEnds.VisaDialog import *
    from Code.FrontEnds.MatplotlibWxPanel import *
    from Code.FrontEnds.KeithleyIVPanel import *
except:
    print("""Cannot load Shell Panel or IEPanel add The folder above pyMeaure to sys.path
            Also check that the Boa Constructor Source is on sys.path """)
    raise

#-------------------------------------------------------------------------------
#Constants
PYMEASURE_ROOT=os.path.join(os.path.dirname( __file__ ), '..','..')
FRONTENDS_DIRECTORY=os.path.join(PYMEASURE_ROOT,'Code','FrontEnds')
IMAGE_DIRECTORY=os.path.join(PYMEASURE_ROOT,'Code','FrontEnds','img')
JAVASCRIPT_STRING="""<html>
<head>
<script type="text/javascript">
function disp_prompt()
{
var fname=prompt("Please enter your name:","Your name")
document.getElementById("msg").innerHTML="Greetings " + fname
}
</script>
</head>
<body>

<input type="button" onclick="disp_prompt()" value="Display a prompt box" />
<br /><br />

<div id="msg"></div>

</body>
</html> 


"""

PANELS=['ShellPanel','IEPanel',
    'SimpleLogLowerInterfacePanel','SimpleArbDBLowerInterfacePanel','MatplotlibWxPanel','KeithleyIVPanel']

#-------------------------------------------------------------------------------
#Functions

def get_top_parent(window):
    """Returns the topmost parent window"""
    try:
        parent=window.Parent
        print(parent)
        if parent in [None,''] or not isinstance(parent, InstanceType):
            raise
        get_top_parent(parent)
    except:
        return window
def convert_datetime(ISO_datetime_string,format_string='%m/%d/%Y at %H:%M:%S GMT') :
    "Converts from long ISO format 2010-05-13T21:54:25.755000 to something reasonable"
    #strip any thing smaller than a second
    time_seconds=ISO_datetime_string.split('.')[0]
    
    #then get it into a datetime format
    time_datetime=datetime.datetime.strptime(time_seconds,"%Y-%m-%dT%H:%M:%S")
    return time_datetime.strftime(format_string)



        
        
#-------------------------------------------------------------------------------
# Boa Code

def create(parent):
    return AdvancedInterfaceFrame(parent)

[wxID_BASICINTERFACEFRAME, wxID_BASICINTERFACEFRAMEARBDBPANEL, 
 wxID_BASICINTERFACEFRAMEBUTTON1, wxID_BASICINTERFACEFRAMEBUTTON2, 
 wxID_BASICINTERFACEFRAMEBUTTON3, wxID_BASICINTERFACEFRAMEDISPLAY, 
 wxID_BASICINTERFACEFRAMEENDOFTHEDAYBUTTON, 
 wxID_BASICINTERFACEFRAMEEXECUTEBUTTON, 
 wxID_BASICINTERFACEFRAMEINSTRUMENTSBUTTON, 
 wxID_BASICINTERFACEFRAMEINTERFACESTATUSBAR, 
 wxID_BASICINTERFACEFRAMEINTERFACETOOLBAR, 
 wxID_BASICINTERFACEFRAMELEFTINTERFACEPANEL, 
 wxID_BASICINTERFACEFRAMELOGSPANEL, wxID_BASICINTERFACEFRAMELOWERCONTROLPANEL, 
 wxID_BASICINTERFACEFRAMELOWERINTERFACE, 
 wxID_BASICINTERFACEFRAMELOWERINTERFACEPANEL, 
 wxID_BASICINTERFACEFRAMEMAINPANEL, wxID_BASICINTERFACEFRAMEPANEL1, 
 wxID_BASICINTERFACEFRAMEPLOTPANEL, 
 wxID_BASICINTERFACEFRAMEREPLACERIGHTCONTROLBUTTTON, 
 wxID_BASICINTERFACEFRAMERIGHTCONTROLPANEL, wxID_BASICINTERFACEFRAMESHELL, 
 wxID_BASICINTERFACEFRAMESTATESBUTTON, wxID_BASICINTERFACEFRAMEUPPERINTERFACE, 
 wxID_BASICINTERFACEFRAMEUPPERINTERFACEPANEL, 
 wxID_BASICINTERFACEFRAMEVISADIALOGBUTTON, 
] = [wx.NewId() for _init_ctrls in range(26)]

[wxID_BASICINTERFACEFRAMEINTERFACETOOLBARLAUNCHBOA, 
 wxID_BASICINTERFACEFRAMEINTERFACETOOLBARSAGE, 
] = [wx.NewId() for _init_coll_InterfaceToolBar_Tools in range(2)]

[wxID_BASICINTERFACEFRAMETOOLMENULOADSCRIPTS, 
 wxID_BASICINTERFACEFRAMETOOLMENURUN_PYTHON, 
] = [wx.NewId() for _init_coll_ToolMenu_Items in range(2)]

[wxID_BASICINTERFACEFRAMEFILEMENUNEW, wxID_BASICINTERFACEFRAMEFILEMENUOPEN, 
] = [wx.NewId() for _init_coll_FileMenu_Items in range(2)]

class AdvancedInterfaceFrame(wx.Frame):
    # Needs to have an explicit list for the designer to work 
    _custom_classes = {'wx.Panel':['ShellPanel','IEPanel',
    'SimpleLogLowerInterfacePanel','SimpleArbDBLowerInterfacePanel','MatplotlibWxPanel','KeithleyIVPanel'],'wx.Dialog':'EndOfDayDialog'}
    def _init_coll_boxSizer7_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.StatesButton, 0, border=0, flag=0)
        parent.AddWindow(self.InstrumentsButton, 0, border=0, flag=0)

    def _init_coll_boxSizer6_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button1, 0, border=0, flag=0)
        parent.AddWindow(self.button2, 0, border=0, flag=0)
        parent.AddWindow(self.button3, 0, border=0, flag=0)
        parent.AddWindow(self.ExecuteButton, 0, border=0, flag=0)
        parent.AddWindow(self.ReplaceRightControlButtton, 0, border=0, flag=0)
        parent.AddWindow(self.EndOfTheDayButton, 0, border=0, flag=0)
        parent.AddWindow(self.VisaDialogButton, 0, border=0, flag=0)

    def _init_coll_boxSizer4_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.UpperInterface, 1, border=2,
              flag=wx.EXPAND | wx.ALL)

    def _init_coll_boxSizer5_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.LowerInterface, 1, border=2,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer3_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.UpperInterfacePanel, 4, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.LowerInterfacePanel, 0, border=2,
              flag=wx.ALL | wx.EXPAND)
        parent.AddWindow(self.LowerControlPanel,0, border=2,
              flag=wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.MainPanel, 1, border=1, flag=wx.ALL | wx.EXPAND)

    def _init_coll_boxSizer2_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.LeftInterfacePanel, 1, border=2,
              flag=wx.EXPAND | wx.ALL)
        parent.AddWindow(self.RightControlPanel, 0, border=2,
              flag=wx.ALIGN_RIGHT | wx.ALL | wx.EXPAND)

    def _init_coll_ToolMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Runs a python program as a script',
              id=wxID_BASICINTERFACEFRAMETOOLMENURUN_PYTHON,
              kind=wx.ITEM_NORMAL, text='Run Python Module As a Script')
        parent.Append(help='Load Scripts from a python Module',
              id=wxID_BASICINTERFACEFRAMETOOLMENULOADSCRIPTS,
              kind=wx.ITEM_NORMAL, text='Load Scripts from Module')
        self.Bind(wx.EVT_MENU, self.OnToolMenuRun_pythonMenu,
              id=wxID_BASICINTERFACEFRAMETOOLMENURUN_PYTHON)
        self.Bind(wx.EVT_MENU, self.OnToolMenuLoadscriptsMenu,
              id=wxID_BASICINTERFACEFRAMETOOLMENULOADSCRIPTS)

    def _init_coll_FileMenu_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='Open a file',
              id=wxID_BASICINTERFACEFRAMEFILEMENUOPEN, kind=wx.ITEM_NORMAL,
              text='Open')
        parent.Append(help='Adds a new panel to main notebook',
              id=wxID_BASICINTERFACEFRAMEFILEMENUNEW, kind=wx.ITEM_NORMAL,
              text='New Panel')
        self.Bind(wx.EVT_MENU, self.OnFileMenuOpenMenu,
              id=wxID_BASICINTERFACEFRAMEFILEMENUOPEN)
        self.Bind(wx.EVT_MENU, self.OnFileMenuNewMenu,
              id=wxID_BASICINTERFACEFRAMEFILEMENUNEW)

    def _init_coll_InterfaceMenuBar_Menus(self, parent):
        # generated method, don't edit

        parent.Append(menu=self.FileMenu, title='File')
        parent.Append(menu=self.HelpMenu, title='Help')
        parent.Append(menu=self.ToolMenu, title='Tools')

    def _init_coll_UpperInterface_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.Display, select=True,
              text='Display')
        parent.AddPage(imageId=-1, page=self.PlotPanel, select=False,
              text='Plot')
        parent.AddPage(imageId=-1, page=self.panel1, select=False,
              text='Keithley IV')

    def _init_coll_LowerInterface_Pages(self, parent):
        # generated method, don't edit

        parent.AddPage(imageId=-1, page=self.Shell, select=True, text='Shell')
        parent.AddPage(imageId=-1, page=self.LogsPanel, select=False,
              text='Logs')
        parent.AddPage(imageId=-1, page=self.ArbDBPanel, select=False,
              text='Files')

    def _init_coll_InterfaceStatusBar_Fields(self, parent):
        # generated method, don't edit
        parent.SetFieldsCount(1)

        parent.SetStatusText(number=0, text='Status')

        parent.SetStatusWidths([-1])

    def _init_coll_InterfaceToolBar_Tools(self, parent):
        # generated method, don't edit

        parent.DoAddTool(bitmap=wx.Bitmap(str(os.path.join(IMAGE_DIRECTORY,'Component.png')),
              wx.BITMAP_TYPE_PNG), bmpDisabled=wx.NullBitmap,
              id=wxID_BASICINTERFACEFRAMEINTERFACETOOLBARLAUNCHBOA,
              kind=wx.ITEM_NORMAL, label='Boa',
              longHelp='Launch Boa Constructor',
              shortHelp='Launch Boa Constructor')
        parent.DoAddTool(bitmap=wx.Bitmap(str(os.path.join(IMAGE_DIRECTORY,'jupyter-logo.png')),
              wx.BITMAP_TYPE_PNG), bmpDisabled=wx.NullBitmap,
              id=wxID_BASICINTERFACEFRAMEINTERFACETOOLBARSAGE,
              kind=wx.ITEM_NORMAL, label='',
              longHelp='Launch SAGE and display ', shortHelp='Launch SAGE')
        self.Bind(wx.EVT_TOOL, self.OnInterfaceToolBarLaunchboaTool,
              id=wxID_BASICINTERFACEFRAMEINTERFACETOOLBARLAUNCHBOA)
        self.Bind(wx.EVT_TOOL, self.OnInterfaceToolBarTools1Tool,
              id=wxID_BASICINTERFACEFRAMEINTERFACETOOLBARSAGE)

        parent.Realize()

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer2 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer3 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer4 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer5 = wx.BoxSizer(orient=wx.VERTICAL)

        self.boxSizer6 = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.boxSizer7 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_boxSizer2_Items(self.boxSizer2)
        self._init_coll_boxSizer3_Items(self.boxSizer3)
        self._init_coll_boxSizer4_Items(self.boxSizer4)
        self._init_coll_boxSizer5_Items(self.boxSizer5)
        self._init_coll_boxSizer6_Items(self.boxSizer6)
        self._init_coll_boxSizer7_Items(self.boxSizer7)

        self.SetSizer(self.boxSizer1)
        self.RightControlPanel.SetSizer(self.boxSizer7)
        self.LowerInterfacePanel.SetSizer(self.boxSizer5)
        self.LeftInterfacePanel.SetSizer(self.boxSizer3)
        self.UpperInterfacePanel.SetSizer(self.boxSizer4)
        self.LowerControlPanel.SetSizer(self.boxSizer6)
        self.MainPanel.SetSizer(self.boxSizer2)

    def _init_utils(self):
        # generated method, don't edit
        self.FileMenu = wx.Menu(title='')

        self.HelpMenu = wx.Menu(title='')

        self.InterfaceMenuBar = wx.MenuBar()

        self.ToolMenu = wx.Menu(title='Tools')

        self._init_coll_FileMenu_Items(self.FileMenu)
        self._init_coll_InterfaceMenuBar_Menus(self.InterfaceMenuBar)
        self._init_coll_ToolMenu_Items(self.ToolMenu)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_BASICINTERFACEFRAME,
              name='AdvancedInterfaceFrame', parent=prnt, pos=wx.Point(-5, 106),
              size=wx.Size(1448, 874), style=wx.DEFAULT_FRAME_STYLE,
              title='Advanced Interface')
        self._init_utils()
        self.SetClientSize(wx.Size(1440, 840))
        self.SetMenuBar(self.InterfaceMenuBar)
        self.Bind(wx.EVT_CLOSE, self.OnBasicInterfaceFrameClose)

        self.InterfaceStatusBar = wx.StatusBar(id=wxID_BASICINTERFACEFRAMEINTERFACESTATUSBAR,
              name='InterfaceStatusBar', parent=self, style=0)
        self.InterfaceStatusBar.SetHelpText('Status')
        self.InterfaceStatusBar.SetLabel('')
        self._init_coll_InterfaceStatusBar_Fields(self.InterfaceStatusBar)
        self.SetStatusBar(self.InterfaceStatusBar)

        self.InterfaceToolBar = wx.ToolBar(id=wxID_BASICINTERFACEFRAMEINTERFACETOOLBAR,
              name='InterfaceToolBar', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1440, 40),
              style=wx.TAB_TRAVERSAL | wx.TB_3DBUTTONS | wx.TB_HORIZONTAL | wx.MAXIMIZE_BOX | wx.NO_BORDER)
        self.InterfaceToolBar.SetHelpText('Launch Boa Contstructor')
        self.InterfaceToolBar.SetToolTipString('InterfaceToolBar')
        self.InterfaceToolBar.SetToolBitmapSize(wx.Size(30, 30))
        self.InterfaceToolBar.SetToolPacking(0)
        self.InterfaceToolBar.SetToolSeparation(1)
        self.SetToolBar(self.InterfaceToolBar)

        self.MainPanel = wx.Panel(id=wxID_BASICINTERFACEFRAMEMAINPANEL,
              name='MainPanel', parent=self, pos=wx.Point(1, 1),
              size=wx.Size(1438, 838), style=wx.TAB_TRAVERSAL)

        self.LeftInterfacePanel = wx.Panel(id=wxID_BASICINTERFACEFRAMELEFTINTERFACEPANEL,
              name='LeftInterfacePanel', parent=self.MainPanel, pos=wx.Point(2,
              2), size=wx.Size(1355, 834), style=wx.TAB_TRAVERSAL)

        self.RightControlPanel = wx.Panel(id=wxID_BASICINTERFACEFRAMERIGHTCONTROLPANEL,
              name='RightControlPanel', parent=self.MainPanel,
              pos=wx.Point(1361, 2), size=wx.Size(75, 834),
              style=wx.TAB_TRAVERSAL)
        self.RightControlPanel.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.LowerControlPanel = wx.Panel(id=wxID_BASICINTERFACEFRAMELOWERCONTROLPANEL,
              name='LowerControlPanel', parent=self.LeftInterfacePanel,
              pos=wx.Point(2, 808), size=wx.Size(1351, 24),
              style=wx.TAB_TRAVERSAL)
        self.LowerControlPanel.SetBackgroundColour(wx.Colour(0, 255, 128))

        self.UpperInterfacePanel = wx.Panel(id=wxID_BASICINTERFACEFRAMEUPPERINTERFACEPANEL,
              name='UpperInterfacePanel', parent=self.LeftInterfacePanel,
              pos=wx.Point(2, 2), size=wx.Size(1351, 640),
              style=wx.TAB_TRAVERSAL)
        self.UpperInterfacePanel.SetBackgroundColour(wx.Colour(128, 128, 128))
        self.UpperInterfacePanel.SetHelpText('UpperInterfacePanel')

        self.LowerInterfacePanel = wx.Panel(id=wxID_BASICINTERFACEFRAMELOWERINTERFACEPANEL,
              name='LowerInterfacePanel', parent=self.LeftInterfacePanel,
              pos=wx.Point(2, 646), size=wx.Size(1351, 158),
              style=wx.TAB_TRAVERSAL)
        self.LowerInterfacePanel.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.UpperInterface = wx.Notebook(id=wxID_BASICINTERFACEFRAMEUPPERINTERFACE,
              name='UpperInterface', parent=self.UpperInterfacePanel,
              pos=wx.Point(2, 2), size=wx.Size(1347, 636), style=0)

        self.LowerInterface = wx.Treebook(id=wxID_BASICINTERFACEFRAMELOWERINTERFACE,
              name='LowerInterface', parent=self.LowerInterfacePanel,
              pos=wx.Point(2, 2), size=wx.Size(1347, 154), style=0)
        self.LowerInterface.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED,
              self.OnLowerInterfaceTreebookPageChanged,
              id=wxID_BASICINTERFACEFRAMELOWERINTERFACE)

        self.Display = IEPanel(id=wxID_BASICINTERFACEFRAMEDISPLAY,
              name='Display', parent=self.UpperInterface, pos=wx.Point(0, 0),
              size=wx.Size(1339, 610), style=wx.TAB_TRAVERSAL)

        self.Shell = ShellPanel(id=wxID_BASICINTERFACEFRAMESHELL, name='Shell',
              parent=self.LowerInterface, pos=wx.Point(0, 0), size=wx.Size(1281,
              154), style=wx.TAB_TRAVERSAL)

        self.button1 = wx.Button(id=wxID_BASICINTERFACEFRAMEBUTTON1,
              label='Java Script Example', name='button1',
              parent=self.LowerControlPanel, pos=wx.Point(0, 0),
              size=wx.Size(136, 23), style=0)
        self.button1.Bind(wx.EVT_BUTTON, self.OnButton1Button,
              id=wxID_BASICINTERFACEFRAMEBUTTON1)

        self.button2 = wx.Button(id=wxID_BASICINTERFACEFRAMEBUTTON2,
              label='button2', name='button2', parent=self.LowerControlPanel,
              pos=wx.Point(136, 0), size=wx.Size(75, 23), style=0)
        self.button2.Bind(wx.EVT_BUTTON, self.OnButton2Button,
              id=wxID_BASICINTERFACEFRAMEBUTTON2)

        self.button3 = wx.Button(id=wxID_BASICINTERFACEFRAMEBUTTON3,
              label='button3', name='button3', parent=self.LowerControlPanel,
              pos=wx.Point(211, 0), size=wx.Size(75, 23), style=0)

        self.ExecuteButton = wx.Button(id=wxID_BASICINTERFACEFRAMEEXECUTEBUTTON,
              label='Execute IEPanel.py', name='ExecuteButton',
              parent=self.LowerControlPanel, pos=wx.Point(286, 0),
              size=wx.Size(111, 23), style=0)
        self.ExecuteButton.Bind(wx.EVT_BUTTON, self.OnExecuteButtonButton,
              id=wxID_BASICINTERFACEFRAMEEXECUTEBUTTON)

        self.ReplaceRightControlButtton = wx.Button(id=wxID_BASICINTERFACEFRAMEREPLACERIGHTCONTROLBUTTTON,
              label='Replace Right Control Panel',
              name='ReplaceRightControlButtton', parent=self.LowerControlPanel,
              pos=wx.Point(397, 0), size=wx.Size(180, 24), style=0)
        self.ReplaceRightControlButtton.Bind(wx.EVT_BUTTON,
              self.OnReplaceRightControlButttonButton,
              id=wxID_BASICINTERFACEFRAMEREPLACERIGHTCONTROLBUTTTON)

        self.StatesButton = wx.Button(id=wxID_BASICINTERFACEFRAMESTATESBUTTON,
              label='States', name='StatesButton',
              parent=self.RightControlPanel, pos=wx.Point(0, 0),
              size=wx.Size(75, 23), style=0)
        self.StatesButton.Bind(wx.EVT_BUTTON, self.OnStatesButtonButton,
              id=wxID_BASICINTERFACEFRAMESTATESBUTTON)

        self.InstrumentsButton = wx.Button(id=wxID_BASICINTERFACEFRAMEINSTRUMENTSBUTTON,
              label='Instruments', name='InstrumentsButton',
              parent=self.RightControlPanel, pos=wx.Point(0, 23),
              size=wx.Size(75, 23), style=0)
        self.InstrumentsButton.Bind(wx.EVT_BUTTON,
              self.OnInstrumentsButtonButton,
              id=wxID_BASICINTERFACEFRAMEINSTRUMENTSBUTTON)

        self.LogsPanel = SimpleLogLowerInterfacePanel(id=wxID_BASICINTERFACEFRAMELOGSPANEL,
              name='LogsPanel', parent=self.LowerInterface, pos=wx.Point(0, 0),
              size=wx.Size(1281, 154), style=wx.TAB_TRAVERSAL)

        self.ArbDBPanel = SimpleArbDBLowerInterfacePanel(id=wxID_BASICINTERFACEFRAMEARBDBPANEL,
              name='ArbDBPanel', parent=self.LowerInterface, pos=wx.Point(0,
              0), size=wx.Size(1281, 154), style=wx.TAB_TRAVERSAL)

        self.EndOfTheDayButton = wx.Button(id=wxID_BASICINTERFACEFRAMEENDOFTHEDAYBUTTON,
              label='End of The Day Log', name='EndOfTheDayButton',
              parent=self.LowerControlPanel, pos=wx.Point(577, 0),
              size=wx.Size(103, 23), style=0)
        self.EndOfTheDayButton.Bind(wx.EVT_BUTTON,
              self.OnEndOfTheDayButtonButton,
              id=wxID_BASICINTERFACEFRAMEENDOFTHEDAYBUTTON)

        self.VisaDialogButton = wx.Button(id=wxID_BASICINTERFACEFRAMEVISADIALOGBUTTON,
              label='VISA Communicator', name='VisaDialogButton',
              parent=self.LowerControlPanel, pos=wx.Point(680, 0),
              size=wx.Size(184, 23), style=0)
        self.VisaDialogButton.Bind(wx.EVT_BUTTON, self.OnVisaDialogButtonButton,
              id=wxID_BASICINTERFACEFRAMEVISADIALOGBUTTON)

        self.PlotPanel = MatplotlibWxPanel(id=wxID_BASICINTERFACEFRAMEPLOTPANEL,
              name='PlotPanel', parent=self.UpperInterface, pos=wx.Point(0, 0),
              size=wx.Size(1339, 610), style=wx.TAB_TRAVERSAL)

        self.panel1 = KeithleyIVPanel(id=wxID_BASICINTERFACEFRAMEPANEL1,
              name='panel1', parent=self.UpperInterface, pos=wx.Point(0, 0),
              size=wx.Size(1339, 610), style=wx.TAB_TRAVERSAL)

        self._init_coll_InterfaceToolBar_Tools(self.InterfaceToolBar)
        self._init_coll_UpperInterface_Pages(self.UpperInterface)
        self._init_coll_LowerInterface_Pages(self.LowerInterface)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)
        #make the shell self aware--requires that ShellEditor.interp.locals=locals()
        self.Shell.ShellEditor.pushLine("shell=locals()['self']")
        #This assumes the main frame is exactly 6 levels above
        self.Shell.ShellEditor.pushLine("frame=shell.Parent.Parent.Parent.Parent.Parent.Parent")
        self.Shell.ShellEditor.pushLine("print('\# The object corresponding to the main frame is called frame')")
        #self.Shell.ShellEditor.pushLine("shell=locals()['self']",'\n')
        self.right_control_panels=[self.RightControlPanel]
        self.current_right_control_panel=self.right_control_panels[0]
        
        # TODO Delete this out it is a test
        self.NewPanel=wx.Panel(self.MainPanel,name='Green')
        self.NewPanel.SetBackgroundColour(wx.Colour(0,255,0))
        self.right_control_panels.append(self.NewPanel)
        self.NewPanel2=wx.Panel(self.MainPanel,name='Blue')
        self.NewPanel2.SetBackgroundColour(wx.Colour(0,0,255))
        self.right_control_panels.append(self.NewPanel2)
        self.NewPanel3=wx.Panel(self.MainPanel,name='Red')
        self.NewPanel3.SetBackgroundColour(wx.Colour(255,0,0))
        self.right_control_panels.append(self.NewPanel3)
        
        self.NewPanel.Show(False)
        self.NewPanel2.Show(False)
        self.NewPanel3.Show(False)
        
        
        # This initializes the locals dictionary, needed to get output from 
        # execfile command. This attribute needs to be asigned to locals() at 
        # the time that the frame is created. See Module Runner
        self.locals={}
        
        
        # This passes the button event from the log panel to the main frame
        self.LogsPanel.Bind(wx.EVT_BUTTON,self.update_display)
        self.ScriptsMenu=wx.Menu()
        self.ToolMenu.AppendMenu(-1,'Scripts',self.ScriptsMenu)
        
        #Added these for script handling
        self.loaded_script_menu_items=[]
        self.event_handlers={}
        
        self.tool_menu_number=0
        
        #This adds panels to the FileMenu->Add Panel item
        self.panels_menu()
    
    def panels_menu(self):
        """ Creates the Add Panels Menu"""
        # First we select only files of the for *Panel.py
        FrontEnds_files=os.listdir(FRONTENDS_DIRECTORY)
        self.panel_files=[]
        for file in FrontEnds_files:
            if re.search('Panel.py',file) and not re.search('.pyc|pyo',file):
                self.panel_files.append(file)
        
         
        #This adds panels to the FileMenu->Add Panel item
        self.add_panel_menu=wx.Menu()
        self.panel_dictionary={}
        for panel in self.panel_files:
            new_id=wx.NewId()
            self.panel_dictionary[new_id]=panel
            self.add_panel_menu.Append(new_id,panel,'Add the Panel %s'%panel)
            self.Bind(wx.EVT_MENU, lambda evt: self.OnAddPanel(evt,new_id),id=new_id)
            #print(new_id,panel)
        #print(self.panel_dictionary)
        self.FileMenu.AppendMenu(0,'Add a Panel',self.add_panel_menu)   
    def OnAddPanel(self,event,id):
        """ Adds a panel"""
        sys.path.append(FRONTENDS_DIRECTORY)
        #print(dir(event),event.Id)
        panel_name=self.panel_dictionary[event.Id].replace('.py','')
        exec('from %s import *'%panel_name)
        exec('self.%s_%s=%s(id=%s,name="%s_%s", parent=self.UpperInterface, pos=wx.Point(0, 0),size=wx.Size(1339, 610), style=wx.TAB_TRAVERSAL)'%(panel_name,id,panel_name,id,panel_name,id))
        exec("self.UpperInterface.AddPage(imageId=-1, page=self.%s_%s, select=True,text='%s')"%(panel_name,id,panel_name))
                  

    def OnFileMenuOpenMenu(self, event):
        event.Skip()

    def OnReplaceRightControlButttonButton(self, event):
        try:
            new=self.right_control_panels.index(
            self.current_right_control_panel)%len(self.right_control_panels)+1
            new_panel=self.right_control_panels[new]
        except:
            new=0
            new_panel=self.right_control_panels[new]
            
        self.swap_panel(self.current_right_control_panel,new_panel,self.boxSizer2)

    def swap_panel(self,old_panel,new_panel,sizer):
        "Swaps a panel and places the new one in the sizer"
        new_panel.SetPosition(old_panel.Position)
        new_panel.SetSize(old_panel.Size)
        old_panel.Show(False)
        sizer.Replace(old_panel,new_panel)
        new_panel.Show(True)
        self.current_right_control_panel=new_panel
        self.Update()

    def OnInterfaceToolBarLaunchboaTool(self, event):
        os.system(r'start python C:\Anaconda2\Lib\site-packages\boa\Boa.py')
        event.Skip()

    def OnExecuteButtonButton(self, event):
        path=str(os.path.join(PYMEASURE_ROOT,'Code/FrontEnds/IEPanel.py'))
        exec(compile(open(path).read(), path, 'exec'))

    def OnLowerInterfaceTreebookPageChanged(self, event):
        self.update_display()
        event.Skip()

    def update_display(self,event=None):
        "Updates the display"
        if self.LowerInterface.GetCurrentPage() is self.LogsPanel:
            self.Display.ie.Navigate(self.LogsPanel.current_log.path)
        else: 
            self.Display.Refresh()       

    def OnInterfaceToolBarTools1Tool(self, event):
        #sage_script=r'C:\"Program Files"\AutoIt3\Examples\SAGE_NOIE2.exe'
        #os.system('jupyter notebook')
        self.Display.ie.Navigate('http://localhost:8888/tree')
        pass
    
    def OnBasicInterfaceFrameClose(self, event):
        """ What to do when the frame is closed, needed to avoid memory leaks"""
        try:
            app=wx.GetApp()
            app.stdioWin.close()
        except:pass
        
        self.Destroy()
        
        event.Skip()

    def OnButton1Button(self, event):
        self.Display.write(JAVASCRIPT_STRING)
        event.Skip()

    def OnToolMenuRun_pythonMenu(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', '.', '', '*.py', wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                

                try:
                    exec(compile(open(filename).read(), filename, 'exec'),self.locals)
                except:
                    pass

               
        finally:
            dlg.Destroy()
        event.Skip()

    def OnToolMenuLoadscriptsMenu(self, event):
        " Loads Scripts to run"
        dlg = wx.FileDialog(self, 'Choose a Python Module', '.', '', '*.py', wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                module_scripts=self.import_scripts(filename)
                module=module_scripts['module']
                
                try:

                    for index,script in enumerate(module_scripts['scripts']):
                        new_id=wx.NewId()
                        menu_item=wx.MenuItem(self.ToolMenu,id=new_id,
                        kind=wx.ITEM_NORMAL, text='Run %s '%script,
                        help='Run %s  from the %s module'%(script,module))
                        self.ScriptsMenu.AppendItem(menu_item)
                        self.loaded_script_menu_items.append(menu_item)
                        
                        
                        #event_handler=(lambda event: self.execute_script(event))
                        #eval('def event\_handler%s(event):return self.execute_script(event,module\_scripts["%s"],"%s")'%(index,script,script),locals())
                        
                        
                        #event_handler.func_name='%s'%index
                        self.event_handlers[menu_item.GetId()]=module_scripts[script]
                        #print(self.event_handlers)
                        self.Bind(wx.EVT_MENU,self.execute_script,id=menu_item.GetId())
                    #print(self.event_handlers)
                    #self.bind_menu()        
              
                except:
                    print(('Could Not Import {0}'.format(module)))
                    raise
        finally:
            dlg.Destroy()
            event.Skip()
            #print(self.event_handlers)

##    def bind_menu(self): 
##        for index,menu_item in enumerate(self.loaded_script_menu_items):
##            print(self.event_handlers[menu_item.GetId()],menu_item,menu_item.GetId())
##            self.Bind(wx.EVT_MENU,self.event_handlers[menu_item.GetId()],id=menu_item.GetId())       
   
   
   
   
   
    def import_scripts(self,file_name):
        "Loads a module given a path and returns a dictionary of things recognized as scripts"""
        #added file path to sys.path
        output={}
        scripts=[]
        module_directory=os.path.split(file_name)[0]
        module_name=os.path.split(file_name)[1].replace('.py','')
        sys.path.append(module_directory)
        exec('import {0}'.format(module_name))
        attributes=eval('dir({0})'.format(module_name))
        for item in attributes:
            if re.search('test_|_robot|_script',item,re.IGNORECASE):
                scripts.append(item)
                output[item]=eval('{0}.{1}'.format(module_name,item))
            
        output['module']=module_name
        output['scripts']=scripts
        
        return output

    def execute_script(self,event):

        #print(self.event_handlers)
        #print(event.Id)
        return self.event_handlers[event.Id]()

    def add_notebook_page(self):
        """ Adds a page to the InterfaceNotebook"""
        pass    
        
        

        
    def OnButton2Button(self, event):
        self.tool_menu_number=self.tool_menu_number+1
        if self.tool_menu_number is 1:
            self.ScriptsMenu=wx.Menu()
            self.ToolMenu.AppendMenu(-1,'Scripts',self.ScriptsMenu)
        self.ScriptsMenu.Append(help='Runs the {0} script'.format(self.tool_menu_number),
                            id=-1,kind=wx.ITEM_NORMAL, text='Run the {0} script'.format(self.tool_menu_number))
        event.Skip()
    def OnStatesButtonButton(self, event):
        states_directory=os.path.join(PYMEASURE_ROOT,'Data/States')
        
        self.Display.ie.Navigate(states_directory)
        event.Skip()

    def OnInstrumentsButtonButton(self, event):
        instruments_directory=os.path.join(PYMEASURE_ROOT,'Instruments')
        
        self.Display.ie.Navigate(instruments_directory)
        event.Skip()

    def OnEndOfTheDayButtonButton(self, event):
        dlg = EndOfDayDialog(self)
        try:
            result = dlg.ShowModal()
        finally:
            dlg.Destroy()
        event.Skip
        
    def OnVisaDialogButtonButton(self, event):
        dlg = VisaDialog(self)
        try:
            result = dlg.Show()
        finally:
            pass
        event.Skip

    def OnFileMenuNewMenu(self, event):
        
##        dlg = wx.FileDialog(self, 'Choose a file', '.', '', '*.*', wx.OPEN)
##        try:
##            if dlg.ShowModal() == wx.ID_OK:
##                filename = dlg.GetPath()
##                # Your code
##        finally:
##            dlg.Destroy()
##        self.upper_Interface.AddPage(
##        event.Skip()
        pass
##    def OnAddPanel(self, event):
##        exec('self.%s'+'_%s'+'=%s(self.UpperInterface)'%(panel_name,panel_number,panel_name))
        
def test_AdvancedInterfaceFrame():
    """ Tests the AdvancedInterfaceFrame Class"""
    app = wx.App(False)
    app.RedirectStdio()

    frame = create(None)
    frame.Show()
    # This is needed for the execfile command to output properly--can't redirect
    frame.locals=locals()
    
    
    app.MainLoop()



if __name__ == '__main__':
    app = wx.App(False)
    app.RedirectStdio()
    # The import here stops the Error wx Debug Alert
    from Code.FrontEnds.ShellPanel import *
    frame = create(None)
    frame.Show()
    # This is needed for the execfile command to output properly--can't redirect
    frame.locals=locals()
    
    
    app.MainLoop()
