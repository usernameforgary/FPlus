import wx

class TuninPhaseList(wx.Panel):
	def __init__(self, parent):
		super().__init__(parent)
		this.parent = parent

		sizer = wx.Sizer(wx.HORIZONTAL)

		self.SetSizer(sizer)
