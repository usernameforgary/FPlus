import wx

from controllers.TopologyController import TopologyController

class ProjectConfigGUI(wx.Panel):
	def __init__(self, parent, model):
		super().__init__(parent)
		self.parent = parent
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		topologySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.mainSizer.Add(topologySizer, 1, wx.ALL|wx.EXPAND, 0)
		otherSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.mainSizer.Add(otherSizer, 1, wx.ALL|wx.Execute, 0)		

		self.SetSizer(mainSizer)


	def addTopology(self, model):
		if model is not None:
