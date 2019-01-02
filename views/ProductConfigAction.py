import wx

from pubsub import pub
from topics.Topics import ProductConfigTopics
from models.Product import Product
from .VNAConfigGUI import VNAConfigGUI

class ProductConfigAction(wx.Panel):
	def __init__(self, parent, model: Product):
		super().__init__(parent)
		self.parent = parent
		self.model = model

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		btnCreateTuningPhase = wx.Button(self, label="Create Tuning Phase")
		btnVnaConfig = wx.Button(self, label="VNA Configuration")
		self.leftSizer.Add(btnCreateTuningPhase, 1, wx.ALL|wx.EXPAND, 0)
		self.rightSizer.Add(btnVnaConfig, 1, wx.ALL|wx.EXPAND, 0)

		self.Bind(wx.EVT_BUTTON, self.ShowVNAConfig, btnVnaConfig)
		self.Bind(wx.EVT_BUTTON, self.createTuningPhase, btnCreateTuningPhase)

		self.mainSizer.Add(self.leftSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.mainSizer.Add(self.rightSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(self.mainSizer)

	def ShowVNAConfig(self, evt):
		vnaConfigGUI = VNAConfigGUI(self.model.vnaConfig)
		vnaConfigGUI.Show()

	def createTuningPhase(self, evt):
		pub.sendMessage(ProductConfigTopics.GUI_CREATE_PRODUCT_TUNING_PHASE.value)