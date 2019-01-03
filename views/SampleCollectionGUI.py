import wx

from models.TuningPhase import TuningPhase
from .PointListGUI import PointListGUI
from .TopologyGUI import TopologyGUI
from .AnalyzerResponseGUI import AnalyzerResponseGUI
from utils.AnalyzerCommunication import AnalyzerCommunication

class SampleCollectionGUI(wx.Frame):
	def __init__(self, model: TuningPhase):
		super().__init__(None, -1, "Sample Collection", size = wx.Size(1500, 800), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL | wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 5, wx.ALL | wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)
		self.Centre()

		self.initalData()

		self.readBtn = wx.Button(self, wx.ID_ANY, 'Read Data from Analyzer')
		self.leftSizer.Add(self.readBtn)

		self.Bind(wx.EVT_BUTTON, self.readAnalyzerData, self.readBtn)

	def initalData(self):
		pointListGUI = PointListGUI(self, self.model.topology)
		self.leftSizer.Add(pointListGUI, 1, wx.ALL|wx.EXPAND, 0)
		topologyGUI = TopologyGUI(self, self.model.topology)
		self.rightSizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)
		anylyzerResponseGUI = AnalyzerResponseGUI(self, None)
		self.rightSizer.Add(anylyzerResponseGUI, 1, wx.ALL|wx.EXPAND, 0)

	def readAnalyzerData(self, event):
		communication = AnalyzerCommunication.getInstance()
		communication.getDataTest()