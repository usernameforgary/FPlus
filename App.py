import wx
from controllers.AppController import AppController


app = wx.App(redirect=True)
appC = AppController()
app.MainLoop()