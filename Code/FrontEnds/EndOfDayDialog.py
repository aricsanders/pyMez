#End of Day Application
#This is needs to be updated. It is Ryan's program that I have turned into a dialog.
# 

#Todo:FIx this !!! it is broken
import wx
import wx.stc
import wx.richtext
import time
#import Frame
from xml.dom.minidom import parse
from os.path import normpath
import os
import sys
# Add pyMez to sys.path (this allows imports that don't go through pyMez/__init__.py
sys.path.append(os.path.join(os.path.dirname( __file__ ), '..','..'))
try:
    import Code.DataHandlers.XMLModels
except:
    print("Cannot find  pyMez.Code.DataHandlers.Logs")

[wxID_EndOfDayDialog, wxID_EndOfDayDialogCLEAR_FILE, wxID_EndOfDayDialogDATA_FLAG, 
 wxID_EndOfDayDialogFILE_CHOOSER, wxID_EndOfDayDialogFILE_CHOOSER2,wxID_EndOfDayDialogFILE_DISP,wxID_EndOfDayDialogFILE_DISP2,wxID_EndOfDayDialogQUEST1, 
 wxID_EndOfDayDialogQUEST2, wxID_EndOfDayDialogQUEST3, wxID_EndOfDayDialogQUEST4, 
 wxID_EndOfDayDialogQUEST5, wxID_EndOfDayDialogQUEST6, wxID_EndOfDayDialogRESP1, 
 wxID_EndOfDayDialogRESP2, wxID_EndOfDayDialogRESP3, wxID_EndOfDayDialogRESP4, 
 wxID_EndOfDayDialogRESP5, wxID_EndOfDayDialogRESP6, wxID_EndOfDayDialogSTATICBOX, 
 wxID_EndOfDayDialogSTATICLINE1, wxID_EndOfDayDialogSUBMIT, 
] = [wx.NewId() for _init_ctrls in range(22)]

TESTS_DIRECTORY=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Tests')

class EndOfDayDialog(wx.Dialog):
    # Variables and Constants for the XML file
    file_list = ["None"];
    log_file="End_Of_Day_Log.xml";
    
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_EndOfDayDialog, name='EndOfDayDialog',
              parent=prnt, pos=wx.Point(420, 108), size=wx.Size(545, 842),
              style=wx.DEFAULT_FRAME_STYLE, title='End Of Day')
        self.SetClientSize(wx.Size(537, 808))
        self.SetToolTipString('')
        self.SetBackgroundColour(wx.Colour(192, 192, 192))

        self.quest1 = wx.StaticText(id=wxID_EndOfDayDialogQUEST1,
              label='What did you do today?', name='quest1', parent=self,
              pos=wx.Point(16, 48), size=wx.Size(115, 13), style=0)
        self.quest1.SetToolTipString('')

        self.quest2 = wx.StaticText(id=wxID_EndOfDayDialogQUEST2,
              label='Who was involved?', name='quest2', parent=self,
              pos=wx.Point(16, 168), size=wx.Size(92, 13), style=0)
        self.quest2.SetToolTipString('The people involved')

        self.quest3 = wx.StaticText(id=wxID_EndOfDayDialogQUEST3,
              label='Who suggested it?', name='quest3', parent=self,
              pos=wx.Point(16, 240), size=wx.Size(89, 13), style=0)
        self.quest3.SetToolTipString('')

        self.quest4 = wx.StaticText(id=wxID_EndOfDayDialogQUEST4,
              label='Why was it done?', name='quest4', parent=self,
              pos=wx.Point(16, 304), size=wx.Size(85, 13), style=0)
        self.quest4.SetToolTipString('')

        self.quest5 = wx.StaticText(id=wxID_EndOfDayDialogQUEST5,
              label='What was the conclusion?', name='quest5', parent=self,
              pos=wx.Point(16, 432), size=wx.Size(124, 13), style=0)
        self.quest5.SetToolTipString('')

        self.resp1 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP1,
              parent=self, pos=wx.Point(152, 48), size=wx.Size(368, 88),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp1.SetLabel('text')
        self.resp1.SetName('resp1')

        self.quest6 = wx.StaticText(id=wxID_EndOfDayDialogQUEST6,
              label='Where is the data located?', name='quest6', parent=self,
              pos=wx.Point(16, 528), size=wx.Size(129, 13), style=0)
        self.quest6.SetToolTipString('')

        self.resp2 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP2,
              parent=self, pos=wx.Point(152, 168), size=wx.Size(368, 40),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp2.SetLabel('text')
        self.resp2.SetName('resp2')

        self.resp3 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP3,
              parent=self, pos=wx.Point(152, 240), size=wx.Size(368, 32),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp3.SetLabel('text')
        self.resp3.SetName('resp3')

        self.resp5 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP5,
              parent=self, pos=wx.Point(152, 432), size=wx.Size(368, 72),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp5.SetLabel('text')
        self.resp5.SetName('resp5')

        self.resp4 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP4,
              parent=self, pos=wx.Point(152, 304), size=wx.Size(368, 104),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp4.SetLabel('text')
        self.resp4.SetName('resp4')

        self.resp6 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogRESP6,
              parent=self, pos=wx.Point(152, 528), size=wx.Size(368, 48),
              style=wx.richtext.RE_MULTILINE, value='')
        self.resp6.SetLabel('text')
        self.resp6.SetName('resp6')

        self.data_flag = wx.CheckBox(id=wxID_EndOfDayDialogDATA_FLAG,
              label='New Data', name='data_flag', parent=self, pos=wx.Point(64,
              608), size=wx.Size(70, 13), style=0)
        self.data_flag.SetValue(False)
        self.data_flag.SetToolTipString('Are there new data files?')
        self.data_flag.Bind(wx.EVT_CHECKBOX, self.OnData_flagCheckbox,
              id=wxID_EndOfDayDialogDATA_FLAG)

        self.submit = wx.Button(id=wxID_EndOfDayDialogSUBMIT, label='Submit',
              name='submit', parent=self, pos=wx.Point(280, 608),
              size=wx.Size(240, 23), style=0)
        self.submit.SetToolTipString('Submit Jounral Entry')
        self.submit.Bind(wx.EVT_BUTTON, self.OnSubmitButton,
              id=wxID_EndOfDayDialogSUBMIT)

        self.file_chooser = wx.Button(id=wxID_EndOfDayDialogFILE_CHOOSER,
              label='Add Files', name='file_chooser', parent=self,
              pos=wx.Point(144, 608), size=wx.Size(75, 23), style=0)
        self.file_chooser.SetToolTipString('Add Files')
        self.file_chooser.Enable(False)
        self.file_chooser.Bind(wx.EVT_BUTTON, self.OnFile_chooserButton,
              id=wxID_EndOfDayDialogFILE_CHOOSER)
              
              
        self.file_chooser2 = wx.Button(id=wxID_EndOfDayDialogFILE_CHOOSER2,
              label='Choose Log File', name='file_chooser2', parent=self,
              pos=wx.Point(16, 8), size=wx.Size(120, 23), style=0)
        self.file_chooser2.SetToolTipString('Add Files')
        self.file_chooser2.Enable(True)
        self.file_chooser2.Bind(wx.EVT_BUTTON, self.OnFile_chooserButton2,
              id=wxID_EndOfDayDialogFILE_CHOOSER2)
              
              
        self.clear_file = wx.Button(id=wxID_EndOfDayDialogCLEAR_FILE, label='Clear',
              name='clear_file', parent=self, pos=wx.Point(144, 640),
              size=wx.Size(75, 23), style=0)
        self.clear_file.SetToolTipString('Clear File List')
        self.clear_file.Enable(False)
        self.clear_file.Bind(wx.EVT_BUTTON, self.OnClear_fileButton,
              id=wxID_EndOfDayDialogCLEAR_FILE)
              
        self.staticLine2 = wx.StaticLine(id=wxID_EndOfDayDialogSTATICLINE1,
              name='staticLine2', parent=self, pos=wx.Point(16, 648),
              size=wx.Size(504, 0), style=0)

        self.staticbox = wx.StaticBox(id=wxID_EndOfDayDialogSTATICBOX,
              label='Submit', name='staticbox', parent=self, pos=wx.Point(256,
              592), size=wx.Size(272, 48), style=0)
        self.staticbox.SetToolTipString('')

        self.file_disp = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogFILE_DISP,
              parent=self, pos=wx.Point(40, 672), size=wx.Size(480, 112),
              style=wx.richtext.RE_MULTILINE,
              value='Click New Data to Enable Adding Files')
        self.file_disp.SetName('file_disp')
        self.file_disp.SetToolTipString('')
        self.file_disp.SetEditable(False)
        self.file_disp.Enable(True)
        self.file_disp.SetLabel('text')
        
        
        self.file_disp2 = wx.richtext.RichTextCtrl(id=wxID_EndOfDayDialogFILE_DISP2,
              parent=self, pos=wx.Point(152, 8), size=wx.Size(368, 25),
              style=wx.richtext.RE_MULTILINE,
              value="".join(self.log_file))
        self.file_disp2.SetName('file_disp')
        self.file_disp2.SetToolTipString('')
        self.file_disp2.SetEditable(False)
        self.file_disp2.Enable(True)
        self.file_disp2.SetLabel('text')
        

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.log_File=os.path.join(TESTS_DIRECTORY,"EndOfDay.xml")

    def OnData_flagCheckbox(self, event):
        if self.data_flag.Value == False:
            self.file_chooser.Enable(False)
            self.clear_file.Enable(False)
            self.file_disp.Value="Click New Data to Enable Adding Files"
        else:
            self.file_chooser.Enable(True)
            self.clear_file.Enable(True)
            self.file_disp.Value="Current File List:\n"+"\n".join(self.file_list)
            

    def OnSubmitButton(self, event):
        dbl_check = wx.MessageDialog(self,"Are you sure you want to submit?","Confirm",wx.OK|wx.CANCEL)
        if dbl_check.ShowModal() == wx.ID_OK:
            self.XML_processing(self.log_file)
            self.Destroy()
        dbl_check.Destroy()

    def OnFile_chooserButton(self, event):
        file_dia = wx.FileDialog(self,"Pick your files",".","","*.*",wx.FD_MULTIPLE)
        if file_dia.ShowModal()==wx.ID_OK:
            self.temp_list=file_dia.GetPaths()
        file_dia.Destroy()
        if self.file_list == ["None"]:
            self.file_list = self.temp_list
        else:
            self.file_list.extend(self.temp_list)
        if self.data_flag.Value == True:
            self.file_disp.Value="Current File List:\n" + "\n".join(self.file_list)
            
    def OnFile_chooserButton2(self, event):
        file_dia = wx.FileDialog(self,"Pick your log file",".","","*.*",wx.OPEN)
        if file_dia.ShowModal()==wx.ID_OK:
            self.temp_file=file_dia.GetPath()
        self.log_file=normpath(self.temp_file)
        #file_dia.Destroy()
        self.file_disp2.Value=" ".join(self.log_file)
            
    def OnClear_fileButton(self, event):
        self.file_list = ["None"]
        self.file_disp.Value="Current File List:\n" + "\n".join(self.file_list)
        
    def XML_processing(self,xml_file):
        try:
            log=Code.DataHandlers.XMLModels.EndOfDayXMLLog(xml_file)
        except:
            options={"directory":TESTS_DIRECTORY,
                     "general_descriptor":"Log",
                     "specific_descriptor":"End_Of_Day"
                     }
            log=Code.DataHandlers.XMLModels.EndOfDayXMLLog(None,**options)
            log.path=os.path.join(TESTS_DIRECTORY,log.path)
        doc = log.document
        root = doc.documentElement
        log.add_entry()
        #print(log.path)
        Index=log.current_entry['Index']
        response={'Actions':self.resp1.Value,'Who_Did':self.resp2.Value
    ,'Who_Suggested':self.resp3.Value,'Why':self.resp4.Value,
    'Conclusion':self.resp5.Value,'Data_Location':self.resp6.Value}
        
        log.add_entry_information(Index,**response)
        # Take care of the files
        if self.data_flag.Value==True and self.file_list!=["None"]:
            for url in self.file_list:
                url="file:///"+url.replace('\\','/')
                log.add_entry_information(Index,**{'URL':url})
        
        log.save()

class BoaApp(wx.App):
    def OnInit(self):
        self.main =wx.Frame(None)
        dlg = EndOfDayDialog(self.main)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                result = dlg.GetValue()
                 # Your code
        finally:
            dlg.Destroy()
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
