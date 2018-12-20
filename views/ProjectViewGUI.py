import wx
import wx.dataview

class ProjectViewGUI(wx.Frame):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project", pos = wx.DefaultPosition, size = wx.Size( 1369,824 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		leftSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.projectTreeCtrl = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
		leftSizer.Add( self.projectTreeCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_dataViewTreeCtrl1 = wx.dataview.DataViewTreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		leftSizer.Add( self.m_dataViewTreeCtrl1, 1, wx.ALL|wx.EXPAND, 5 )


		mainSizer.Add( leftSizer, 1, wx.EXPAND, 0 )


		self.SetSizer( mainSizer )
		self.Layout()
		self.projectViewStatusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass