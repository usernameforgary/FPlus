import wx
from pubsub import pub
from topics import Topics

class View(wx.Frame):

	def __init__(self, parent=None):
		wx.Frame.__init__(self, parent, -1, "Main View")				

		sizer = wx.BoxSizer(wx.VERTICAL)
		text = wx.StaticText(self, -1, "My Money")
		ctrl = wx.TextCtrl(self, -1, "")
		sizer.Add(text, 0, wx.EXPAND | wx.ALL)
		sizer.Add(ctrl, 0, wx.EXPAND | wx.ALL)

		self.moneyCtrl = ctrl
		ctrl.SetEditable(False)
		self.SetSizer(sizer)


		# subsicrbe to all "MONEY CHANED" messages from the Model
		#pub.subscribe(self.setMoney, Topics.money_changed.name)
		pub.subscribe(self.setMoney, "money_changed")

	def setMoney(self, money):
		self.moneyCtrl.SetValue(str(money))