import wx

from pubsub import pub

from models.TuningPhase import TuningPhase
from .VNAConfigGUI import VNAConfigGUI

class TuningPhaseConfigAction(wx.Panel):
	def __init__(self, parent, model: TuningPhase):
		super().__init__(parent)
		self.parent = parent
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		btnVnaConfig = wx.Button(self, label="VNA Configuration")
		self.rightSizer.Add(btnVnaConfig, 1, wx.ALL|wx.EXPAND, 0)

		self.Bind(wx.EVT_BUTTON, self.ShowVNAConfig, btnVnaConfig)

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)

	def ShowVNAConfig(self, evt):
		vnaConfigGUI = VNAConfigGUI(self.model.vnaConfig)
		vnaConfigGUI.Show()