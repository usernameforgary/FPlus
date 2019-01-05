import wx

from models.ProjectViewModel import ProjectViewModel
from utils.AnalyzerCommunication import AnalyzerCommunication

class AnalyzerConfigGUI(wx.Frame):
	def __init__(self, model: ProjectViewModel):
		super().__init__(None, -1, "Analyzer Configuration")
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.actionSizer = wx.BoxSizer(wx.HORIZONTAL)
		staticText = wx.StaticText(self, -1, "Analyzer Address: ")
		self.addressTextCtrl = wx.TextCtrl(self)
		self.checkConnectionBtn = wx.Button(self, wx.ID_ANY, "Check Connection")

		self.topSizer.Add(staticText, 1, wx.ALL, 5)
		self.topSizer.Add(self.addressTextCtrl, 1, wx.ALL, 5)
		self.actionSizer.Add(self.checkConnectionBtn, 1, wx.ALL, 5)

		self.mainSizer.Add(self.topSizer, 3, wx.ALL|wx.EXPAND, 0)
		self.mainSizer.Add(self.actionSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)

		self.initialView()

		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_BUTTON, self.checkConnection, self.checkConnectionBtn)

	def initialView(self):
		if self.model.vnaAddress is not None and self.model.vnaAddress is not '':
			self.addressTextCtrl.SetValue(self.model.vnaAddress)

	def checkConnection(self, event):
		address = self.addressTextCtrl.GetValue().strip() if self.addressTextCtrl.GetValue() is not None else ''
		if address is not None and address is not '':
			analyzerCommunication = AnalyzerCommunication.getInstance(address)
			analyzerCommunication.openConnection()
			result = analyzerCommunication.checkAnalyzerConnection()
			if result != "OK":
				wx.MessageBox('Connection Error: {0}'.format(result), 'Error', wx.OK|wx.ICON_ERROR)
			else:
				wx.MessageBox('Connect Successfully!', 'Success', wx.OK | wx.ICON_INFORMATION)
			analyzerCommunication.closeConnection()
		else:
			wx.MessageBox('Please input analyzer address', 'Message', wx.OK)

	# validataion and save config while window close
	def onClose(self, event):	
		address = self.addressTextCtrl.GetValue().strip() if self.addressTextCtrl.GetValue() is not None else ''
		self.model.vnaAddress = address
		self.Destroy()