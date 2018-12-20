import wx
from Controllers.AppController import AppController


app = wx.App(None)
appC = AppController()
app.MainLoop()