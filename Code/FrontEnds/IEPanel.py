#-----------------------------------------------------------------------------
# Name:        IEPanel.py
# Purpose:     To create a gui interface for html using internet explorer widget.
# Author:      Aric Sanders
# Created:     3/02/2016
# License:     MIT License
#-----------------------------------------------------------------------------
""" A binding to internet explorer through the Wx iewin.IEHtmlWindow,
derived in no small part from the work of
11/18/2003 - Jeff Grimmett (grimmtooth@softhome.net)

Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>
"""
# Todo: replace this with wx.html2.Webview
import  wx
import wx.html2 as iewin
#if wx.Platform == '__WXMSW__':
#    import wx.lib.iewin_old as iewin
wxID_CONTROL_PANEL=-1
#----------------------------------------------------------------------
# Todo: sizer does not respond in y direction
class IEPanel(wx.Panel):
    def __init__(self, parent, id, pos, size, style, name):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
            
        log=[]    
        self.log = log
        self.history=[]
        self.current = "http://wxPython.org/"

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ie = iewin.WebView.New(self)
        self.ie.SetPage(overview,"")

        btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Home", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnHomeButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        #self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        btn = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        #self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

        btn = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Search", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnSearchPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Location:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)
        
        self.location = wx.ComboBox(
                            self, -1, self.current, style=wx.CB_DROPDOWN
                            )
        
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.ie, 1, wx.EXPAND)

        self.ie.LoadURL(self.current)
        self.location.Append(self.current)
        
        self.SetSizer(sizer)
        # Since this is a wx.Window we have to call Layout ourselves
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        
        #Added this to make address bar work correctly
        self.Bind(iewin.EVT_WEBVIEW_LOADED, self.after_navigate)

        ## Hook up the event handlers for the IE window.  Using
        ## AddEventSink is how we tell the COM system to look in this
        ## object for method names matching the COM Event names.  They
        ## are automatically looked for in the ActiveXCtrl class, (so
        ## deriving a new class from IEHtmlWindow would also have been
        ## a good appraoch) and now they will be looked for here too.
        #self.ie.AddEventSink(self)

    def after_navigate(self,event):
        """ After a file is navigated to updates the location bar"""
        self.UpdateLocation()
        
    def write(self,string=None):
        """Writes test to the ie window"""
        self.ie.SetPage(str(string),"")

    def read(self):
        return self.ie.GetText()
        
    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)


    def OnSize(self, evt):
        self.Layout()

    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.log.append('OnLocationSelect: %s\n' % url)
        self.ie.LoadURL(url)
        self.current=url
        self.UpdateLocation()
    def OnLocationKey(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            URL = self.location.GetValue()
            self.ie.LoadURL(URL)
            self.current=URL
            self.UpdateLocation()
        else:
            evt.Skip()


    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        
        dlg = wx.FileDialog(self, 'Choose a file', '.', '', '*.*', wx.FD_OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.current = dlg.GetPath()
                self.ie.LoadURL(self.current)

        finally:
            dlg.Destroy()
        
   
    def OnHomeButton(self, event):
        self.ie.LoadURL("https://aricsanders.github.io/")    ## ET Phone Home!
        
        self.UpdateLocation()
        
    def OnPrevPageButton(self, event):
        try:
            self.ie.GoBack()
            self.UpdateLocation()
        except:pass
		
    def OnNextPageButton(self, event):
        self.ie.GoForward()
        self.UpdateLocation()
    def UpdateLocation(self):
        """Updates the location bar with up to self.history_max"""
        #There is something wierd about this I think it needs to check if it is busy
        self.current=self.ie.GetCurrentURL()
        self.current=str(self.current)
        if not self.current in self.history:
            self.location.Append(self.current)
            self.history.append(self.current)
        self.location.SetValue(self.current)
        
        
##
##    def OnCheckCanGoBack(self, event):
##        event.Enable(self.ie.CanGoBack())
##        
##    def OnCheckCanGoForward(self, event):
##        event.Enable(self.ie.CanGoForward())

    def OnStopButton(self, evt):
        self.ie.Stop()

    def OnSearchPageButton(self, evt):
        self.ie.LoadURL("https://www.google.com")
        self.UpdateLocation()

    def OnRefreshPageButton(self, evt):
        self.ie.Reload()


    # Here are some of the event methods for the IE COM events.  See
    # the MSDN docs for DWebBrowserEvents2 for details on what events
    # are available, and what the parameters are.
    
    def BeforeNavigate2(self, this, pDisp, URL, Flags, TargetFrameName,
                        PostData, Headers, Cancel):
        self.log.write('BeforeNavigate2: %s\n' % URL[0])
        if URL[0] == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.  The
                # Cancel parameter is defined as an [in,out] type and
                # so setting the value means it will be returned and
                # checked in the COM control.
                Cancel[0] = True
                

    def NewWindow3(self, this, pDisp, Cancel, Flags, urlContext, URL):
        self.log.write('NewWindow3: %s\n' % URL)
        Cancel[0] = True   # Veto the creation of a  new window.

    #def ProgressChange(self, this, progress, progressMax):
    #    self.log.write('ProgressChange: %d of %d\n' % (progress, progressMax))
        
    def DocumentComplete(self, this, pDisp, URL):
        self.current = URL[0]
        self.location.SetValue(self.current)

    def TitleChange(self, this, Text):
        if self.frame:
            self.frame.SetTitle(self.titleBase + ' -- ' + Text)

    def StatusTextChange(self, this, Text):
        if self.frame:
            self.frame.SetStatusText(Text)

        

#----------------------------------------------------------------------
overview = """\
<html><body>
<h2>wx.lib.iewin.IEHtmlWindow</h2>

The wx.lib.iewin.IEHtmlWindow class is one example of using ActiveX
controls from wxPython using the new wx.activex module.  This allows
you to use an ActiveX control as if it is a wx.Window, you can call
its methods, set/get properties, and receive events from the ActiveX
control in a very intuitive way.

<p> Using this class is simpler than ActiveXWrapper, doesn't rely on
the win32all extensions, and is more "wx\'ish", meaning that it uses
events and etc. as would be expected from any other wx window.

</body></html>
"""

def test_panel():
    app = wx.App(False)
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=IEPanel(id=1, name='IEPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(200, 800),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()


#----------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=IEPanel(id=1, name='IEPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(200, 800),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()