import wx

from models.TuningPhase import TuningPhase
from .PointListGUI import PointListGUI
from .TopologyGUI import TopologyGUI
from .AnalyzerResponseGUI import AnalyzerResponseGUI
from utils.AnalyzerCommunication import AnalyzerCommunication
from utils.MockCommunication import mockGetDataBySParameterName

class SampleCollectionGUI(wx.Frame):
	def __init__(self, model: TuningPhase):
		super().__init__(None, -1, "Sample Collection", size = wx.Size(1500, 800), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		self.model = model
		self.readDataTimer = wx.Timer(self)
		self.analyzerCommunication = None

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		btn1 = wx.Button(self, wx.ID_ANY, 'T1\n\r T1\n\r T1 T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1T1\n\r T1')
		btn2 = wx.Button(self, wx.ID_ANY, 'T1')
		self.rightSizer.Add(btn1, 1)
		self.rightSizer.Add(btn2, 2, wx.ALL | wx.EXPAND, 0)
		#self.initalData()

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL | wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 5, wx.ALL | wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)
		self.Centre()

		self.readBtn = wx.Button(self, wx.ID_ANY, 'Read Data from Analyzer')
		self.stopBtn = wx.Button(self, wx.ID_ANY, 'Stop Read')
		self.leftSizer.Add(self.readBtn)
		self.leftSizer.Add(self.stopBtn)

		self.Bind(wx.EVT_BUTTON, self.startReadData, self.readBtn)
		#self.Bind(wx.EVT_BUTTON, self.stopReadData, self.stopBtn)
		#self.Bind(wx.EVT_TIMER, self.readAnalyzerData)
		self.Bind(wx.EVT_BUTTON, self.MockstopReadData, self.stopBtn)
		self.Bind(wx.EVT_TIMER, self.MockreadAnalyzerData)

	def initalData(self):
		pointListGUI = PointListGUI(self, self.model.topology)
		self.leftSizer.Add(pointListGUI, 1, wx.ALL|wx.EXPAND, 0)
		topologyGUI = TopologyGUI(self, self.model.topology, showDrawnType=False)
		self.rightSizer.Add(topologyGUI, 0, wx.ALL|wx.EXPAND, 0)
		self.anylyzerResponseGUI = AnalyzerResponseGUI(self, None)
		self.rightSizer.Add(self.anylyzerResponseGUI, 3, wx.ALL|wx.EXPAND, 0)

	def readAnalyzerData(self, event):
		if self.analyzerCommunication is None:
			self.analyzerCommunication = AnalyzerCommunication.getInstance('192.168.253.253')
			self.analyzerCommunication.openConnection()
		xS11, yS11 = self.analyzerCommunication.mockGetDataBySParameterName("S22")
		# xS22, yS22 = self.analyzerCommunication.getDataBySParameterName("S22")
		# xS21, yS21 = self.analyzerCommunication.getDataBySParameterName("S21")
		self.anylyzerResponseGUI.reDrawPlot(xS11,yS11)
#		self.anylyzerResponseGUI.reDrawPlot(xS11,yS11,xS22,yS22,xS21,yS21)
	
	def MockreadAnalyzerData(self, event):	
		xS11, yS11 = mockGetDataBySParameterName("S11")
		xS22, yS22 = mockGetDataBySParameterName("S22")
		xS21, yS21 = mockGetDataBySParameterName("S21")
		#self.anylyzerResponseGUI.reDrawPlot(xS11,yS11)
		self.anylyzerResponseGUI.reDrawPlotAll(xS11,yS11,xS22,yS22,xS21,yS21)
	
	def MockstopReadData(self, event):
		self.readDataTimer.Stop()

	def startReadData(self, event):
		self.readDataTimer.Start(100)		

	def stopReadData(self, event):
		self.readDataTimer.Stop()
		self.analyzerCommunication.closeConnection()
		self.analyzerCommunication = None