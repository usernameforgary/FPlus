import wx

from pubsub import pub
from models.Product import Product
from models.Topology import Topology
from topics.Topics import ProjectViewTopics 
from topics.Topics import TopologyViewTopics

from .TopologyGUI import TopologyGUI
from .PointListGUI import PointListGUI
from .ProductConfigAction import ProductConfigAction

from controllers.TopologyController import TopologyController

class ProductConfigGUI(wx.Panel):
	def __init__(self, parent, model: Product):
		super().__init__(parent)
		self.parent = parent
		self.model = model
		self.topologyController = None

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.topologySizer = wx.BoxSizer(wx.HORIZONTAL)
		self.pointListAndActionSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.pointListSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.actionSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.mainSizer.Add(self.topologySizer, 1, wx.ALL|wx.EXPAND, 0)
		self.mainSizer.Add(self.pointListAndActionSizer, 1, wx.ALL|wx.EXPAND, 0)	

		self.pointListAndActionSizer.Add(self.pointListSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.pointListAndActionSizer.Add(self.actionSizer, 1, wx.ALL|wx.EXPAND, 0)

		self.initialView()	
		self.SetSizer(self.mainSizer)

		pub.subscribe(self.addRefreshTopologyGUI, TopologyViewTopics.GUI_ADD_REFRESH_TOPOLOGY.value)

	def initialView(self):
		self.topologyController = TopologyController(self.model.topology)
		topologyGUI = self.topologyController.initialView(self)
		self.topologySizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)
		pointListGUI = PointListGUI(self, self.model.topology)
		self.pointListSizer.Add(pointListGUI, 1, wx.ALL|wx.EXPAND, 0)
		productConfigActionGUI = ProductConfigAction(self, self.model)
		self.actionSizer.Add(productConfigActionGUI, 1, wx.ALL|wx.EXPAND, 0)

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