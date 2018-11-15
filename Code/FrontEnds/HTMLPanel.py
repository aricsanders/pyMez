#-----------------------------------------------------------------------------
# Name:        HTMLTestPanel.py
# Purpose:     To test using an XSL tranform and a custom HYPERLINK handler
# Author:      Aric Sanders
# Created:     3/02/2016
# License:     MIT License
#-----------------------------------------------------------------------------
#Boa:FramePanel:Panel1
"""
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
import wx
import wx.html
import re
TEST_HTML="<h1>This is a Test String<h1>"

class LinkError(Exception):
    pass
class HTMLWindow(wx.html.HtmlWindow):
    """ speciallized Html window """
    # Overloading the method is deprecated, just intercept the event
    def OnLinkClicked(self,link_info):
        """This is the href handler"""
        
        try:
            function_id=link_info.split(',')[0]
            
            if re.search('edit',function_id):
                passdlg = wx.TextEntryDialog(self, 'Edit Value', 'Value', 
                'test')
                try:
                    if passdlg.ShowModal() == wx.ID_OK:
                        result = passdlg.GetValue()
                            # Your code
                finally:
                    passdlg.Destroy()
            else:
                raise LinkError
        except LinkError:
            # This behavior is deprecated ...
            self.base_OnLinkedClicked(link_info)
[wxID_PANEL1, wxID_PANEL1HTMLWINDOW1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Panel1(wx.Panel):
    _custom_classes = {'wx.html.HtmlWindow': ['HTMLWindow']}
    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.Add(self.htmlWindow1, 1, border=0, flag=wx.EXPAND)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              pos=wx.Point(299, 165), size=wx.Size(1110, 547),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(1102, 513))
        self.SetForegroundColour(wx.Colour(128, 0, 64))

        self.htmlWindow1 = HTMLWindow(id=wxID_PANEL1HTMLWINDOW1,
              name='htmlWindow1', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1102, 513), style=wx.html.HW_SCROLLBAR_AUTO)

        self._init_sizers()

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None,size=wx.Size(762, 502))
    panel=Panel1(id=1, name='HTMLPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(762, 502),
              style=wx.TAB_TRAVERSAL)
    panel.htmlWindow1.LoadPage("http://www.example.com")
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))

    frame.Show()
    app.MainLoop()
