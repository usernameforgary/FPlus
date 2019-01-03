import wx

from models.TuningPhase import TuningPhase
from .TopologyGUI import TopologyGUI
from .PointListGUI import PointListGUI
from .TuningPhaseConfigAction import TuningPhaseConfigAction
from controllers.TopologyController import TopologyController

class TuningPhaseConfigGUI(wx.Panel):
	def __init__(self, parent, model: TuningPhase):
		super().__init__(parent)
		self.parent = parent
		self.model = model

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

	def initialView(self):
		self.topologyController = TopologyController(self.model.topology)
		topologyGUI =  self.topologyController.initialView(self)
		self.topologySizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)
		pointListGUI = PointListGUI(self, self.model.topology)
		self.pointListSizer.Add(pointListGUI, 1, wx.ALL|wx.EXPAND, 0)
		tuningPhaseActionGUI = TuningPhaseConfigAction(self, self.model)
		self.actionSizer.Add(tuningPhaseActionGUI, 1, wx.ALL|wx.EXPAND, 0)