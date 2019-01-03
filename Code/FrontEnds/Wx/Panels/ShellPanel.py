#-----------------------------------------------------------------------------
# Name:        ShellPanel.py
# Purpose:     Shell panel from updated version of Boa
# Author:      Aric Sanders
# Created:     3/02/2016
# License:     MIT License
#-----------------------------------------------------------------------------

"""This is a shell, modified from the shell in Boa Constructor, updated to work with wx 3 and python 2.7
The shell causes a wxWidgets Debug alert to occur because of the wx.stc module, to avoid it in the
end product import this in the module runner.

Help
---------------
<a href="./index.html">`pyMez.Code.FrontEnds`</a>
<div>
<a href="../../../pyMez_Documentation.html">Documentation Home</a> |
<a href="../../index.html">API Documentation Home</a> |
<a href="../../../Examples/html/Examples_Home.html">Examples Home</a> |
<a href="../../../Reference_Index.html">Index</a>
</div>"""

# A trick to make sure the boa directory is on sys.path
import sys
import os
# This is a little bit of a windows hack, it really requires python/Lib/site-packages/boa-constructor
os_path=os.__file__.replace('\\os.pyc','')

sys.path.append(os_path.replace('lib','Lib/site-packages/boa'))



import wx
# import wx.stc

[wxID_PANEL1, wxID_PANEL1STYLEDTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

#-------------------------------------------------------------------------------
#Begin Cut and Paste of Shell Editor From BOA constructor
#-----------------------------------------------------------------------------
# Name:        ShellEditor.py
# Purpose:     Interactive interpreter
#
# Author:      Riaan Booysen
#
# Created:     2000/06/19
# RCS-ID:      $Id: ShellEditor.py,v 1.29 2007/07/02 15:01:06 riaan Exp $
# Copyright:   (c) 1999 - 2007 Riaan Booysen
# Licence:     GPL
#-----------------------------------------------------------------------------

# XXX Try to handle multi line paste


import sys, keyword, types, time

import wx
import wx.stc
import wx.py.introspect

from boa import Preferences, Utils
from boa.Preferences import keyDefs
from boa.Views import StyledTextCtrls
from boa.Models import EditorHelper

from boa.ExternalLib.PythonInterpreter import PythonInterpreter
from boa.ExternalLib import Signature


echo = True

p2c = 'Type "copyright", "credits" or "license" for more information.'

[wxID_SHELL_HISTORYUP, wxID_SHELL_HISTORYDOWN, wxID_SHELL_ENTER, wxID_SHELL_HOME,
 wxID_SHELL_CODECOMP, wxID_SHELL_CALLTIPS,
] = [wx.NewId() for _init_ctrls in range(6)] 

only_first_block = 1


class IShellEditor:
    def destroy(self):
        pass
    
    def execStartupScript(self, startupfile):
        pass
    
    def debugShell(self, doDebug, debugger):
        pass
    
    def pushLine(self, line, addText=''):
        pass

    def getShellLocals(self):
        return {}


class ShellEditor(wx.stc.StyledTextCtrl,
                  StyledTextCtrls.PythonStyledTextCtrlMix,
                  StyledTextCtrls.AutoCompleteCodeHelpSTCMix,
                  StyledTextCtrls.CallTipCodeHelpSTCMix):
    def __init__(self, parent, wId,):
        wx.stc.StyledTextCtrl.__init__(self, parent, wId,
              style = wx.CLIP_CHILDREN | wx.SUNKEN_BORDER)
        StyledTextCtrls.CallTipCodeHelpSTCMix.__init__(self)
        StyledTextCtrls.AutoCompleteCodeHelpSTCMix.__init__(self)
        StyledTextCtrls.PythonStyledTextCtrlMix.__init__(self, wId, ())

        self.lines = StyledTextCtrls.STCLinesList(self)
        self.interp = PythonInterpreter()
        #This line makes it self aware
        self.interp.locals=locals()
        
        self.lastResult = ''

        self.CallTipSetBackground(wx.Colour(255, 255, 232))
        self.SetWrapMode(1)

        self.bindShortcuts()

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.stc.EVT_STC_CHARADDED, self.OnAddChar, id=wId)

        self.Bind(wx.EVT_MENU, self.OnHistoryUp, id=wxID_SHELL_HISTORYUP)
        self.Bind(wx.EVT_MENU, self.OnHistoryDown, id=wxID_SHELL_HISTORYDOWN)
        #self.Bind(EVT_MENU, self.OnShellEnter, id=wxID_SHELL_ENTER)
        self.Bind(wx.EVT_MENU, self.OnShellHome, id=wxID_SHELL_HOME)
        self.Bind(wx.EVT_MENU, self.OnShellCodeComplete, id=wxID_SHELL_CODECOMP)
        self.Bind(wx.EVT_MENU, self.OnShellCallTips, id=wxID_SHELL_CALLTIPS)


        self.history = []
        self.historyIndex = 1

        self.buffer = []

        self.stdout = PseudoFileOut(self)
        self.stderr = PseudoFileErr(self)
        self.stdin = PseudoFileIn(self, self.buffer)

        self._debugger = None

        if sys.hexversion < 0x01060000:
            copyright = sys.copyright
        else:
            copyright = p2c
        import boa.__version__ as __version__
        self.AddText('# Python %s\n# wxPython %s, Boa Constructor %s\n# %s'%(
              sys.version, wx.__version__, __version__.version, copyright))
        #return so it looks right
        self.pushLine('','\n')
        self.LineScroll(-10, 0)
        self.SetSavePoint()


    def destroy(self):
        if self.stdin.isreading():
            self.stdin.kill()

        del self.lines
        del self.stdout
        del self.stderr
        del self.stdin
        del self.interp

    def bindShortcuts(self):
        # dictionnary of shortcuts: (MOD, KEY) -> function
        self.sc = {}
        self.sc[(keyDefs['HistoryUp'][0], keyDefs['HistoryUp'][1])] = self.OnHistoryUp
        self.sc[(keyDefs['HistoryDown'][0], keyDefs['HistoryDown'][1])] = self.OnHistoryDown
        self.sc[(keyDefs['CodeComplete'][0], keyDefs['CodeComplete'][1])] = self.OnShellCodeComplete
        self.sc[(keyDefs['CallTips'][0], keyDefs['CallTips'][1])] = self.OnShellCallTips

    def execStartupScript(self, startupfile):
        if startupfile:
            startuptext = '## Startup script: ' + startupfile
            self.pushLine('print({0};execfile({0}))'.format(repr(startuptext), repr(startupfile)))
        else:
            self.pushLine('')

    def debugShell(self, doDebug, debugger):
        if doDebug:
            self._debugger = debugger
            self.stdout.write('\n## Debug mode turned on.')
            self.pushLine('print("?")')
        else:
            self._debugger = None
            self.pushLine('print("## Debug mode turned {0}.")'.format (doDebug and 'on' or 'off'))

    def OnUpdateUI(self, event):
        if Preferences.braceHighLight:
            StyledTextCtrls.PythonStyledTextCtrlMix.OnUpdateUI(self, event)

    def getHistoryInfo(self):
        lineNo = self.GetCurrentLine()
        if self.history and self.GetLineCount()-1 == lineNo:
            pos = self.PositionFromLine(lineNo) + 4
            endpos = self.GetLineEndPosition(lineNo)
            return lineNo, pos, endpos
        else:
            return None, None, None

    def OnHistoryUp(self, event):
        lineNo, pos, endpos = self.getHistoryInfo()
        if lineNo is not None:
            if self.historyIndex > 0:
                self.historyIndex = self.historyIndex -1

            self.SetSelection(pos, endpos)
            self.ReplaceSelection((self.history+[''])[self.historyIndex])

    def OnHistoryDown(self, event):
        lineNo, pos, endpos = self.getHistoryInfo()
        if lineNo is not None:
            if self.historyIndex < len(self.history):
                self.historyIndex = self.historyIndex +1

            self.SetSelection(pos, endpos)
            self.ReplaceSelection((self.history+[''])[self.historyIndex])

    def pushLine(self, line, addText=''):
        """ Interprets a line """
        self.AddText(addText+'\n')
        prompt = ''
        try:
            self.stdin.clear()
            tmpstdout,tmpstderr,tmpstdin = sys.stdout,sys.stderr,sys.stdin
            #This line prevents redirection from the shell since everytime you
            #push a line it redefines the stdout, etc. 
            sys.stdout,sys.stderr,sys.stdin = self.stdout,self.stderr,self.stdin
            self.lastResult = ''
            if self._debugger:
                prompt = Preferences.ps3
                val = self._debugger.getVarValue(line)
                if val is not None:
                    print(val)
                return False
            elif self.interp.push(line):
                prompt = Preferences.ps2
                self.stdout.fin(); self.stderr.fin()
                return True
            else:
                # check if already destroyed
                if not hasattr(self, 'stdin'):
                    return False

                prompt = Preferences.ps1
                self.stdout.fin(); self.stderr.fin()
                return False
        finally:
            # This reasigns the stdout and stdin
            sys.stdout,sys.stderr,sys.stdin = tmpstdout,tmpstderr,tmpstdin
            if prompt:
                self.AddText(prompt)
            self.EnsureCaretVisible()
    
    def getShellLocals(self):
        return self.interp.locals

    def OnShellEnter(self, event):
        self.BeginUndoAction()
        try:
            if self.CallTipActive():
                self.CallTipCancel()

            lc = self.GetLineCount()
            cl = self.GetCurrentLine()
            ct = self.GetCurLine()[0]
            line = ct[4:].rstrip()
            self.SetCurrentPos(self.GetTextLength())
            #ll = self.GetCurrentLine()

            # bottom line, process the line
            if cl == lc -1:
                if self.stdin.isreading():
                    self.AddText('\n')
                    self.buffer.append(line)
                    return
                # Auto indent
                if self.pushLine(line):
                    self.doAutoIndent(line, self.GetCurrentPos())

                # Manage history
                if line.strip() and (self.history and self.history[-1] != line or not self.history):
                    self.history.append(line)
                    self.historyIndex = len(self.history)
            # Other lines, copy the line to the bottom line
            else:
                self.SetSelection(self.PositionFromLine(self.GetCurrentLine()), self.GetTextLength())
                #self.lines.select(self.lines.current)
                self.ReplaceSelection(ct.rstrip())
        finally:
            self.EndUndoAction()
            #event.Skip()

    def getCodeCompOptions(self, word, rootWord, matchWord, lnNo):
        if not rootWord:
            return list(self.interp.locals.keys()) + list(__builtins__.keys()) + keyword.kwlist
        else:
            try: obj = eval(rootWord, self.interp.locals)
            except Exception as error: return []
            else:
                try: return recdir(obj)
                except Exception as err: return []

    def OnShellCodeComplete(self, event):
        self.codeCompCheck()

    def getTipValue(self, word, lnNo):
        (name, argspec, tip) = wx.py.introspect.getCallTip(word, self.interp.locals)

        tip = self.getFirstContinousBlock(tip)
        tip = tip.replace('(self, ', '(', 1).replace('(self)', '()', 1)

        return tip

    def OnShellCallTips(self, event):
        self.callTipCheck()

    def OnShellHome(self, event):
        lnNo = self.GetCurrentLine()
        lnStPs = self.PositionFromLine(lnNo)
        line = self.GetCurLine()[0]

        if len(line) >=4 and line[:4] in (Preferences.ps1, Preferences.ps2):
            self.SetCurrentPos(lnStPs+4)
            self.SetAnchor(lnStPs+4)
        else:
            self.SetCurrentPos(lnStPs)
            self.SetAnchor(lnStPs)

    def OnKeyDown(self, event):
        if Preferences.handleSpecialEuropeanKeys:
            self.handleSpecialEuropeanKeys(event, Preferences.euroKeysCountry)

        kk = event.GetKeyCode()
        controlDown = event.ControlDown()
        shiftDown = event.ShiftDown()
        if kk == wx.WXK_RETURN and not (shiftDown or event.HasModifiers()):
            if self.AutoCompActive():
                self.AutoCompComplete()
                return
            self.OnShellEnter(event)
            return
        elif kk == wx.WXK_BACK:
                # don't delete the prompt
            if self.lines.current == self.lines.count -1 and \
              self.lines.pos - self.PositionFromLine(self.lines.current) < 5:
                return
        elif kk == wx.WXK_HOME and not (controlDown or shiftDown):
            self.OnShellHome(event)
            return
        elif controlDown:
            if shiftDown and (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, kk) in self.sc:
                self.sc[(wx.ACCEL_CTRL|wx.ACCEL_SHIFT, kk)](self)
                return
            elif (wx.ACCEL_CTRL, kk) in self.sc:
                self.sc[(wx.ACCEL_CTRL, kk)](self)
                return
        
        if self.CallTipActive():
            self.callTipCheck()
        event.Skip()

    def OnAddChar(self, event):
        if event.GetKey() == 40 and Preferences.callTipsOnOpenParen:
            self.callTipCheck()
        

def recdir(obj):
    res = dir(obj)
    if hasattr(obj, '__class__') and obj != obj.__class__:
        if hasattr(obj, '__class__') and not isinstance(obj, types.ModuleType):
            res.extend(recdir(obj.__class__))
        if hasattr(obj, '__bases__'):
            for base in obj.__bases__:
                res.extend(recdir(base))

    unq = {}
    for name in res: unq[name] = None
    return list(unq.keys())

# not used anymore, now using wx.py.introspect
def tipforobj(obj, ccstc):
    # we want to reroute wxPython objects to their doc strings
    # if they are defined
    docs = ''
    if hasattr(obj, '__doc__') and obj.__doc__:
        wxNS = Utils.getEntireWxNamespace()
        if isinstance(obj, type):
            if obj.__name__ in wxNS:
                docs = obj.__init__.__doc__
        elif isinstance(obj, types.InstanceType):
            if obj.__class__.__name__ in wxNS:
                docs = obj.__doc__
        elif isinstance(obj, types.MethodType):
            if obj.__self__.__class__.__name__ in wxNS:
                docs = obj.__doc__
    # Get docs from builtin's docstrings or from Signature module
    if not docs:
        if isinstance(obj, types.BuiltinFunctionType):
            try: docs = obj.__doc__
            except AttributeError: docs = ''
        else:
            try:
                sig = str(Signature.Signature(obj))
                docs = sig.replace('(self, ', '(')
                docs = docs.replace('(self)', '()')
            except (ValueError, TypeError):
                try: docs = obj.__doc__
                except AttributeError: docs = ''

    if docs:
        # Take only the first continuous block from big docstrings
        if only_first_block:
            tip = ccstc.getFirstContinousBlock(docs)
        else:
            tip = docs

        return tip
    return ''


#-----Pipe redirectors--------------------------------------------------------

class PseudoFileIn:
    def __init__(self, output, buffer):
        self._buffer = buffer
        self._output = output
        self._reading = False

    def clear(self):
        self._buffer[:] = []
        self._reading = False

    def isreading(self):
        return self._reading

    def kill(self):
        self._buffer.append(None)

    def readline(self):
        self._reading = True
        self._output.AddText('\n'+Preferences.ps4)
        self._output.EnsureCaretVisible()
        try:
            while not self._buffer:
                # XXX with safe yield once the STC loses focus there is no way
                # XXX to give it back the focus
                # wxSafeYield()
                time.sleep(0.001)
                wx.Yield()
            line = self._buffer.pop()
            if line is None: raise Exception('Terminate')
            if not(line.strip()): return '\n'
            else: return line
        finally:
            self._reading = False

class QuoterPseudoFile(Utils.PseudoFile):
    quotes = '```'
    def __init__(self, output = None, quote=False):
        Utils.PseudoFile.__init__(self, output)
        self._dirty = False
        self._quote = quote

    def _addquotes(self):
        if self._quote:
            self.output.AddText(self.quotes+'\n')

    def write(self, s):
        if not self._dirty:
            self._addquotes()
            self._dirty = True

    def fin(self):
        if self._dirty:
            self._addquotes()
            self._dirty = False

class PseudoFileOut(QuoterPseudoFile):
    tags = 'stdout'
    quotes = '"""'
    def write(self, s):
        QuoterPseudoFile.write(self, s)
        self.output.AddText(s)
        self.output.lastResult = self.tags

class PseudoFileErr(QuoterPseudoFile):
    tags = 'stderr'
    quotes = "'''"
    def write(self, s):
        QuoterPseudoFile.write(self, s)
        self.output.AddText(s)
        self.output.EnsureCaretVisible()
        self.output.lastResult = self.tags

class PseudoFileOutTC(Utils.PseudoFile):
    tags = 'stderr'
    def write(self, s):
        self.output.AppendText(s)
        if echo: sys.__stdout__.write(s)

class PseudoFileErrTC(Utils.PseudoFile):
    tags = 'stdout'
    def write(self, s):
        self.output.AppendText(s)
        if echo: sys.__stderr__.write(s)


#-------------------------------------------------------------------------------

EditorHelper.imgPyCrust = EditorHelper.addPluginImgs('Images\Editor\PyCrust.png')

class PyCrustShellEditor(wx.SplitterWindow):
    def __init__(self, parent, wId):
        wx.SplitterWindow.__init__(self, parent, wId)

        from wx.py.crust import Shell, Filling

        # XXX argh! PyCrust records the About box pseudo file objs from 
        # XXX sys.in/err/out
        o, i, e = sys.stdout, sys.stdin, sys.stderr
        sys.stdout, sys.stdin, sys.stderr = \
              sys.__stdout__, sys.__stdin__, sys.__stderr__
        try:
            self.shellWin = Shell(self, -1)
        finally:
            sys.stdout, sys.stdin, sys.stderr = o, i, e
            
        self.fillingWin = Filling(self, -1, style=wx.SP_3DSASH,
              rootObject=self.shellWin.interp.locals, rootIsNamespace=True)
        
        height = Preferences.screenHeight / 2
        #int(self.GetSize().y * 0.75)
        self.SplitHorizontally(self.shellWin, self.fillingWin, height)
        self.SetMinimumPaneSize(5)

        self.lastResult = 'stdout'
        self._debugger = None

    def destroy(self):
        pass
    
    def execStartupScript(self, startupfile):
        pass
    
    def debugShell(self, doDebug, debugger):
        if doDebug:
            self._debugger = debugger
            self.shellWin.stdout.write('\n## Debug mode turned on.')
            self.pushLine('print("?")')
        else:
            self._debugger = None
            self.pushLine('print("## Debug mode turned {0}.")'.format(doDebug and 'on' or 'off'))
    
    def pushLine(self, line, addText=''):
        if addText:
            self.shellWin.write(addText)

        self.shellWin.push(line)

    def getShellLocals(self):
        return self.shellWin.interp.locals


#-------------------------------------------------------------------------------


shellReg = {'Shell':   (ShellEditor, EditorHelper.imgShell),
            'PyCrust': (PyCrustShellEditor, EditorHelper.imgPyCrust)}
            
#-------------------------------------------------------------------------------
# End Cut and Paste of Shell From BOA        
class ShellPanel(wx.Panel):
    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self._init_coll_boxSizer1_Items(self.boxSizer1)

        self.SetSizer(self.boxSizer1)


    def _init_coll_boxSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.ShellEditor, 1, border=0,
              flag=wx.ALL | wx.EXPAND)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Panel.__init__(self, id=wxID_PANEL1, name='', parent=prnt,
              pos=wx.Point(155, 388), size=wx.Size(529, 364),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(521, 330))

        self.ShellEditor = ShellEditor(self,-1)

        self._init_sizers()

    def __init__(self, parent, id, pos, size, style, name):
        self._init_ctrls(parent)
        


if __name__ == '__main__':
    app = wx.App(False)

    frame = wx.Frame(None,size=wx.Size(762, 502))
    panel=ShellPanel(id=1, name='ShellPanel',
              parent=frame, pos=wx.Point(350, 204), size=wx.Size(762, 502),
              style=wx.TAB_TRAVERSAL)
    sizer=wx.BoxSizer()
    sizer.Add(panel,1,wx.EXPAND,2)
    frame.SetSizerAndFit(sizer)
    frame.SetSize(wx.Size(800, 600))
    frame.Show()

    app.MainLoop()