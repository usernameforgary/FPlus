import wx

from models.VnaConfig import VnaConfig
from models.SweepTable import SweepTable
from enumObjs.EnumObjs import SParameterType
from .ListCtrlNonVirtual import ListCtrlNonVirtual

class VNAConfigGUI(wx.Frame):
	def __init__(self, model: VnaConfig):
		super().__init__(None, -1, "VNA configutation")
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.initWithData()

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 5, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)

		self.Bind(wx.EVT_CLOSE, self.onClose)

	def initWithData(self):
		typeTitle = wx.StaticBox(self, -1, "Select S-Parameter")
		typeBoxSizer = wx.StaticBoxSizer(typeTitle, wx.VERTICAL)
		typeGridSizer = wx.FlexGridSizer(cols = 1)
		self.SParaGroup = []
		s11CB = wx.CheckBox(self, -1, SParameterType.S11.value)
		if SParameterType.S11.value in self.model.SParameter:
			s11CB.SetValue(True)
		s22CB = wx.CheckBox(self, -1, SParameterType.S22.value)
		if SParameterType.S22.value in self.model.SParameter:
			s22CB.SetValue(True)	
		s21CB = wx.CheckBox(self, -1, SParameterType.S21.value)
		if SParameterType.S21.value in self.model.SParameter:
			s21CB.SetValue(True)
		s12CB = wx.CheckBox(self, -1, SParameterType.S12.value)
		if SParameterType.S12.value in self.model.SParameter:
			s12CB.SetValue(True)
		self.SParaGroup.append(s11CB)
		self.SParaGroup.append(s22CB)
		self.SParaGroup.append(s21CB)
		self.SParaGroup.append(s12CB)	
		for typeCB in self.SParaGroup:
			typeGridSizer.Add(typeCB, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5)
			# add event handing for typ radio buttons
			self.Bind(wx.EVT_CHECKBOX, self.onCheckSPara, typeCB)
		typeBoxSizer.Add(typeGridSizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)

		self.leftSizer.Add(typeBoxSizer, 1, wx.ALL|wx.EXPAND, 0)

		self.grid = wx.grid.Grid(self, -1)
		self.grid.CreateGrid(30, 5)
		self.grid.SetColLabelValue(0, "Start Frequency(MHz)")
		self.grid.SetColLabelValue(1, "Stop Frequency(MHz)")
		self.grid.SetColLabelValue(2, "Points")
		self.grid.SetColLabelValue(3, "IF BW")
		self.grid.SetColLabelValue(4, "Power")
		line = 0
		for sweepTable in self.model.sweepTables:
			self.grid.SetCellValue(line, 0, str(sweepTable.startFreq))
			self.grid.SetCellValue(line, 1, str(sweepTable.stopFreq))
			self.grid.SetCellValue(line, 2, str(sweepTable.numberPoints))
			self.grid.SetCellValue(line, 3, str(sweepTable.IFBW))
			self.grid.SetCellValue(line, 4, str(sweepTable.Power))
			line += 1

		self.rightSizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 0)

	def onCheckSPara(self, evt):
		self.model.SParameter = []
		for cb in self.SParaGroup:
			if cb.GetValue():
				self.model.SParameter.append(cb.GetLabel())

	# validataion and save config while window close
	def onClose(self, event):
		SParaLen = len(self.model.SParameter)
		if SParaLen == 0:
			wx.MessageBox("Please select S parameter")
			event.Veto()
			return
		self.model.sweepTables = []				
		rows = self.grid.GetNumberRows()

		for row in range(0, rows - 1):
			startFreq = float(self.grid.GetCellValue(row, 0)) if self.grid.GetCellValue(row, 0) is not '' else 0
			stopFreq = float(self.grid.GetCellValue(row, 1)) if self.grid.GetCellValue(row, 1) is not '' else 0
			pointsNum = int(self.grid.GetCellValue(row, 2)) if self.grid.GetCellValue(row, 2) is not '' else 0
			IFBW = float(self.grid.GetCellValue(row, 3)) if self.grid.GetCellValue(row, 3) is not '' else 0
			power = float(self.grid.GetCellValue(row, 4)) if self.grid.GetCellValue(row, 4) is not '' else 0
			if not (startFreq == 0 and stopFreq == 0 and pointsNum == 0 and IFBW == 0 and power == 0):
				sweepTable = SweepTable(startFreq, stopFreq, pointsNum, IFBW, power)
				self.model.sweepTables.append(sweepTable)

		# if len(self.model.sweepTables) == 0:
		# 	wx.MessageBox("Please input sweep table")
		# 	event.Veto()
		# 	return
		self.Destroy()