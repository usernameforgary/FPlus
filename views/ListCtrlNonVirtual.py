import wx
import wx.lib.mixins.listctrl as listmix

class ListCtrlNonVirtual(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):
	def __init__(self, parent, ID, pos=wx.DefaultPosition,size=wx.DefaultSize, style=0, editable=False):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		listmix.ListCtrlAutoWidthMixin.__init__(self)
		if editable:
			listmix.TextEditMixin.__init__(self)