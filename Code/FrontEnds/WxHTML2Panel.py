#-----------------------------------------------------------------------------
# Name:        WxHTML2Panel
# Purpose:     
# Author:      Aric Sanders
# Created:     1/9/2017
# License:     MIT License
#-----------------------------------------------------------------------------
""" A Wx HTML2 panel for full featured HTML support

 Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

#-----------------------------------------------------------------------------
# Standard Imports
import io
#-----------------------------------------------------------------------------
# Third Party Imports
import wx
import wx.html2
import wx.html2 as webview
#-----------------------------------------------------------------------------
# Module Constants

#-----------------------------------------------------------------------------
# Module Functions

#-----------------------------------------------------------------------------
# Module Classes
class WxHTML2Panel(wx.Panel):
        def __init__(self, parent,id):
                        #(self, parent, log, frame=None):
            self.log = io.StringIO()
            wx.Panel.__init__(self, parent,id)
            self.current = "http://wxPython.org"


            sizer = wx.BoxSizer(wx.VERTICAL)
            btnSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.wv = webview.WebView.New(self)
            self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
            self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)


            btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
            self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
            btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

            btn = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
            self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
            btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
            self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

            btn = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
            self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
            btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
            self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

            btn = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
            self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
            btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

            btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
            self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
            btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

            txt = wx.StaticText(self, -1, "Location:")
            btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

            self.location = wx.ComboBox(
                self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
            self.location.AppendItems(['http://wxPython.org',
                                       'http://wxwidgets.org',
                                       'http://google.com'])
            self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
            self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
            btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)


            sizer.Add(btnSizer, 0, wx.EXPAND)
            sizer.Add(self.wv, 1, wx.EXPAND)
            self.SetSizer(sizer)

            self.wv.LoadURL(self.current)
            # self.write("<h1> Test </h1>")


        def ShutdownDemo(self):
            # put the frame title back
            if self.frame:
                self.frame.SetTitle(self.titleBase)


        # WebView events
        def OnWebViewNavigating(self, evt):
            # this event happens prior to trying to get a resource
            if evt.GetURL() == 'http://www.microsoft.com/':
                if wx.MessageBox("Are you sure you want to visit Microsoft?",
                                 style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                    # This is how you can cancel loading a page.
                    evt.Veto()

        def OnWebViewLoaded(self, evt):
            # The full document has loaded
            self.current = evt.GetURL()
            self.location.SetValue(self.current)


        # Control bar events
        def OnLocationSelect(self, evt):
            url = self.location.GetStringSelection()
            self.log.write('OnLocationSelect: %s\n' % url)
            self.wv.LoadURL(url)

        def OnLocationEnter(self, evt):
            url = self.location.GetValue()
            self.location.Append(url)
            self.wv.LoadURL(url)


        def OnOpenButton(self, event):
            dlg = wx.TextEntryDialog(self, "Open Location",
                                    "Enter a full URL or local path",
                                    self.current, wx.OK|wx.CANCEL)
            dlg.CentreOnParent()

            if dlg.ShowModal() == wx.ID_OK:
                self.current = dlg.GetValue()
                self.wv.LoadURL(self.current)

            dlg.Destroy()

        def OnPrevPageButton(self, event):
            self.wv.GoBack()

        def OnNextPageButton(self, event):
            self.wv.GoForward()

        def OnCheckCanGoBack(self, event):
            event.Enable(self.wv.CanGoBack())

        def OnCheckCanGoForward(self, event):
            event.Enable(self.wv.CanGoForward())

        def OnStopButton(self, evt):
            self.wv.Stop()

        def OnRefreshPageButton(self, evt):
            self.wv.Reload()

        # def write(self,content):
        #     """Writes the HTML content to the display"""
        #     self.wv.SetPage(content)
        #
        # def read(self):
        #     """Returns the current page source"""
        #     return self.wv.GetPageSource()


#-----------------------------------------------------------------------------
# Module Scripts

#-----------------------------------------------------------------------------
# Module Runner
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None,size=wx.Size(900, 800))
    panel=WxHTML2Panel(id=1,
              parent=frame)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()