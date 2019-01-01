import wx

from pubsub import pub
from models.Product import Product
from models.Topology import Topology
from topics.Topics import ProjectViewTopics 
from topics.Topics import TopologyViewTopics

from .TopologyGUI import TopologyGUI

class ProductConfigGUI(wx.Panel):
	def __init__(self, parent, model: Product):
		super().__init__(parent)
		self.parent = parent
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.topologySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.mainSizer.Add(self.topologySizer, 1, wx.ALL|wx.EXPAND, 0)
		self.otherSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.mainSizer.Add(self.otherSizer, 1, wx.ALL|wx.EXPAND, 0)		

		self.initialView()	
		self.SetSizer(self.mainSizer)

		pub.subscribe(self.addRefreshTopologyGUI, TopologyViewTopics.GUI_ADD_REFRESH_TOPOLOGY.value)

	def initialView(self):
		# Add topology gui
		if self.model.topology is None:
			self.model.topology = Topology()
		topologyGUI = TopologyGUI(self, self.model.topology)
		self.topologySizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)

	def addRefreshTopologyGUI(self, topologyGUI):
		self.cleanToplogySizer()
		self.topologySizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)
		self.topologySizer.Layout()

	def cleanToplogySizer(self):
		sizerItemList = self.topologySizer.GetChildren()
		if sizerItemList:
			for item in sizerItemList:
				if item.IsWindow():
					window = item.GetWindow()
					window.Destroy()
				else:
					raise Exception('No-window object in rightSizer')