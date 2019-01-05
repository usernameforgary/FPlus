import wx
from .ListCtrlNonVirtual import ListCtrlNonVirtual

from models.Topology import Topology
from enumObjs.EnumObjs import PointType

class PointListGUI(wx.Panel):
	def __init__(self, parent, model: Topology):
		wx.Panel.__init__(self, parent)
		self.parent = parent
		self.model = model
		
		tID = wx.NewIdRef()
		self.list = ListCtrlNonVirtual(self, tID, style=wx.LC_REPORT|wx.BORDER_NONE|wx.LC_HRULES|wx.LC_VRULES)

		self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.listSizer = wx.BoxSizer(wx.VERTICAL)
		self.mainSizer.Add(self.listSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.listSizer.Add(self.list, 1, wx.ALL|wx.EXPAND, 0)

		self.initalData()
		
		self.SetSizer(self.mainSizer)
	def initalData(self):
		self.list.InsertColumn(0, "No.")
		self.list.InsertColumn(1, "Point Type")

		for point in self.model.points:
			if point.pointType != PointType.PORT.value:
				index = self.list.InsertItem(self.list.GetItemCount(), point.pointIndex)
				self.list.SetItem(index, 0, str(point.pointIndex))
				self.list.SetItem(index, 1, str(point.pointType))
		itemCount = self.list.GetItemCount()
		if itemCount > 0:
			self.list.Focus(itemCount-1)
			self.list.Select(itemCount-1)
		# items = listctrldata.items()
		# for key, data in items:
		# 	index = self.list.InsertItem(self.list.GetItemCount(), data[0])
		# 	self.list.SetItem(index, 1, data[1])

		# self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
		# self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)