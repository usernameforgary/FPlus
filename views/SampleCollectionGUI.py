import wx

from pubsub import pub

from enumObjs.EnumObjs import ProjectOperate
from controllers.SampleCollectionController import SampleCollectionController
from models.TuningPhase import TuningPhase
from .PointListGUI import PointListGUI
from .TopologyGUI import TopologyGUI
from .AnalyzerResponseGUI import AnalyzerResponseGUI

class SampleCollectionGUI(wx.Frame):
	def __init__(self, model: TuningPhase):
		super().__init__(None, -1, "Sample Collection", size = wx.Size(1500, 800), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		self.model = model
		self.sampleCollectionController = SampleCollectionController(self.model)
		# all points
		self.pointListCtrl = None
		# point currently selected
		self.selectedPointIndex = -1
		self.currentStepPostion = 0

		self.readDataTimer = wx.Timer(self)
		self.analyzerCommunication = None

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.startBtn = wx.Button(self, wx.ID_ANY, 'Start')
		self.nextPointBtn = wx.Button(self, wx.ID_ANY, 'Next')
		self.upBtn = wx.Button(self, wx.ID_ANY, 'Up')
		self.downBtn = wx.Button(self, wx.ID_ANY, 'Down')
		self.slider = wx.Slider(self, wx.ID_ANY, 0, -10, 10, style=wx.SL_VERTICAL|wx.SL_LABELS|wx.SL_INVERSE)
		self.stopBtn = wx.Button(self, wx.ID_ANY, 'Stop Read')
	
		self.initalData()

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL | wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 5, wx.ALL | wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)
		self.Centre()

		
		self.leftSizer.Add(self.stopBtn)

		# Read data Timer listener	
		self.Bind(wx.EVT_TIMER, self.readAnalyzerData)
		self.Bind(wx.EVT_BUTTON, self.startReadData, self.startBtn)
		self.Bind(wx.EVT_BUTTON, self.toNextPoint, self.nextPointBtn)
		self.Bind(wx.EVT_BUTTON, self.upCollect, self.upBtn)
		self.Bind(wx.EVT_BUTTON, self.downCollect, self.downBtn)
		#self.Bind(wx.EVT_BUTTON, self.stopReadData, self.stopBtn)
		#self.Bind(wx.EVT_TIMER, self.readAnalyzerData)
		self.Bind(wx.EVT_BUTTON, self.stopReadData, self.stopBtn)

	def initalData(self):
		self.leftSizer.Add(self.startBtn)
		self.leftSizer.Add(self.nextPointBtn)
		self.leftSizer.Add(self.upBtn)
		self.leftSizer.Add(self.downBtn)
		self.leftSizer.Add(self.slider)
		pointListGUI = PointListGUI(self, self.model.topology)
		self.pointListCtrl = pointListGUI.list
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.listItemSelected, self.pointListCtrl)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.listItemDeSelected, self.pointListCtrl)
		
		self.selectedPointIndex = self.pointListCtrl.GetFocusedItem()

		self.leftSizer.Add(pointListGUI, 1, wx.ALL|wx.EXPAND, 0)
		self.anylyzerResponseGUI = AnalyzerResponseGUI(self, None)
		self.rightSizer.Add(self.anylyzerResponseGUI, 3, wx.ALL|wx.EXPAND, 0)
		topologyGUI = TopologyGUI(self, self.model.topology, showDrawnType=False)
		self.rightSizer.Add(topologyGUI, 1, wx.ALL|wx.EXPAND, 0)
	
	def listItemSelected(self, event):
		self.selectedPointIndex = self.pointListCtrl.GetFocusedItem()
	def listItemDeSelected(self, event):
		self.selectedPointIndex = -1
	
	def readAnalyzerData(self, event):	
		xS11, yS11, xS22, yS22, xS21, yS21 = self.sampleCollectionController.readDefaultData()
		if xS11 is None or yS11 is None or xS22 is None or yS22 is None or xS21 is None or yS21 is None:
			self.readDataTimer.Stop()
			wx.MessageBox('Can not get property data from analyzer')
			return
		self.anylyzerResponseGUI.reDrawPlotAll(xS11,yS11,xS22,yS22,xS21,yS21)
	
	def startReadData(self, event):
		if self.selectedPointIndex == -1:
			if self.pointListCtrl is None or self.pointListCtrl.GetItemCount() == 0:
				wx.MessageBox('You have no point to collect')
				return

			itemCount = self.pointListCtrl.GetItemCount()
			self.pointListCtrl.Focus(itemCount-1)
			self.pointListCtrl.Select(itemCount-1)
			self.selectedPointIndex = itemCount - 1	
		self.readDataTimer.Start(100)

	def toNextPoint(self, event):
		if self.selectedPointIndex != -1:
			if self.selectedPointIndex > 0:
				self.selectedPointIndex -= 1
				self.pointListCtrl.Focus(self.selectedPointIndex)
				self.pointListCtrl.Select(self.selectedPointIndex)
				self.currentStepPostion = 0
				self.slider.SetValue(0)
			else:
				wx.MessageBox('Collection finished')
		else:
			wx.MessageBox('Please select point to start')

	def upCollect(self, event):
		self.readDataTimer.Stop()
		if self.currentStepPostion == 0:
			self.sampleCollectionController.readDataSingle(self.selectedPointIndex, self.currentStepPostion)
		if self.currentStepPostion <= 0:
			self.currentStepPostion = 1
		else:
			self.currentStepPostion += 1
		self.sampleCollectionController.readDataSingle(self.selectedPointIndex, self.currentStepPostion)
		self.slider.SetValue(self.currentStepPostion)
		self.readDataTimer.Start(100)

	def downCollect(self, event):
		self.readDataTimer.Stop()
		if self.currentStepPostion == 0:
			self.sampleCollectionController.readDataSingle(self.selectedPointIndex, self.currentStepPostion)
		if self.currentStepPostion >= 0:
			self.currentStepPostion = -1
		else:
			self.currentStepPostion -= 1
		self.sampleCollectionController.readDataSingle(self.selectedPointIndex, self.currentStepPostion)
		self.slider.SetValue(self.currentStepPostion)
		self.readDataTimer.Start(100)

	def stopReadData(self, event):
		self.readDataTimer.Stop()
		if self.analyzerCommunication is not None:
			self.analyzerCommunication.closeConnection()
		self.analyzerCommunication = None
		# Save project to file
		pub.sendMessage(ProjectOperate.SAVE_TO_FILE.value)