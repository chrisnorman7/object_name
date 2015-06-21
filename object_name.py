"""
object_name.py: Put the text of the current NVDA navigator object into a new window.

To install, place this file in the globalPlugins folder. You can get to this folder by typing the following into your run box (windows key + r):
%appdata%\nvda\globalPlugins
Once this is done, simply reload NVDA.

To use, focus the object you want to view the text for, then press NVDA+CTRL+N.

This file written by Chris Norman for use in Coventry Samaritans.

Feel free to distribute, use, learn from, edit or whatever. I only ask that if you do use or modify it, you send me an email just so I can feel good about myself! :-)

My email address, should you want to stroke my ego, complain or get help is
chris.norman2@googlemail.com
"""

from globalPluginHandler import GlobalPlugin
from api import getFocusObject
from ui import message

frame = None # The frame when it opens. Gets reset upon close.

class GlobalPlugin(GlobalPlugin):
 """The plugin required to make this whole thing work."""
 
 def script_objectName(self, gesture):
  """Pops up the text of the current object in a new window."""
  text = getattr(getFocusObject(), 'windowText', None)
  if text != None:
   while text[0] == '\n':
    text = text[1:] # Strip out leading blank lines.
  if not text:
   message('No text.')
  else:
   global frame
   if frame:
    frame.setText(text)
   else:
    frame = ObjectNameFrame(text)
 
 __gestures = {
  'kb:NVDA+control+n': 'objectName'
 }

import wx

class ObjectNameFrame(wx.Frame):
 """The frame to show."""
 def __init__(self, text):
  """Text is the text to populate the frame with."""
  super(ObjectNameFrame, self).__init__(None, title = 'Object Text')
  p = wx.Panel(self)
  s = wx.BoxSizer(wx.HORIZONTAL)
  s1 = wx.BoxSizer(wx.VERTICAL)
  s1.Add(wx.StaticText(p, label = '&Object Text'), 0, wx.GROW)
  self.text = wx.TextCtrl(p, style = wx.TE_MULTILINE)
  s1.Add(self.text, 1, wx.GROW)
  self.setText(text)
  s.Add(s1, 1, wx.GROW)
  s2 = wx.BoxSizer(wx.VERTICAL)
  self.closeButton = wx.Button(p, label = 'Close &Window')
  s2.Add(self.closeButton, 1, wx.GROW)
  self.closeButton.Bind(wx.EVT_BUTTON, lambda event: self.Close(True))
  self.findText = '' # The text that the user searched for last time.
  self.findButton = wx.Button(p, label = '&Find...')
  s2.Add(self.findButton, 1, wx.GROW)
  self.findButton.Bind(wx.EVT_BUTTON, self.find)
  self.findAgainButton = wx.Button(p, label = 'Find A&gain')
  s2.Add(self.findAgainButton, 1, wx.GROW)
  self.findAgainButton.Bind(wx.EVT_BUTTON, lambda event: self.find(text = self.findText))
  s.Add(s2, 0, wx.GROW)
  p.SetSizerAndFit(s)
  self.menu = wx.MenuBar()
  self.editMenu = wx.Menu()
  self.Bind(wx.EVT_MENU, self.find, self.editMenu.Append(wx.ID_FIND, '&Find...\tCTRL+F', 'Search for a string.'))
  self.Bind(wx.EVT_MENU, lambda event: self.find(text = self.findText), self.editMenu.Append(wx.ID_ANY, 'Find A&gain', 'Search again.'))
  self.menu.Append(self.editMenu, '&Edit')
  self.SetMenuBar(self.menu)
  self.Bind(wx.EVT_CLOSE, self.onClose)
  self.Raise()
  self.Show(True)
 
 def Show(self, value = True):
  """Show the window, maximizing in the process."""
  res = super(ObjectNameFrame, self).Show(value)
  self.Maximize(True)
  return res
 
 def find(self, event = None, text = None):
  """Find function."""
  if text == None:
   dlg = wx.TextEntryDialog(self, 'Enter a string to search for', 'Find', self.findText)
   if dlg.ShowModal() == wx.ID_OK:
    text = dlg.GetValue()
   dlg.Destroy()
  if text:
   self.findText = text
   text = text.lower()
   i = self.text.GetInsertionPoint()
   v = self.text.GetValue()[i:].lower()
   if text in v:
    self.text.SetInsertionPoint(v.index(text) + i)
   else:
    wx.Bell()
    return self.find()
 
 def setText(self, text):
  """Set the text field to the provided text."""
  self.text.SetValue(text)
 def onClose(self, event):
  """Close the window, clearing frame first."""
  global frame
  frame = None
  event.Skip()
