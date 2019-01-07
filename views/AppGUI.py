import wx
import wx.aui

from pubsub import pub

from topics.Topics import AppGUITopics

class AppGUI(wx.Frame):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FPlus", pos = wx.DefaultPosition, size = wx.Size( 970,689 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.menuBar = wx.MenuBar( 0 )
		self.fileMenu = wx.Menu()
		self.newMenuItem = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
		self.newMenuItem.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_MENU ) )
		self.fileMenu.Append( self.newMenuItem )

		self.fileMenu.AppendSeparator()

		self.loadMenuItem = wx.MenuItem( self.fileMenu, wx.ID_ANY, u"Load", wx.EmptyString, wx.ITEM_NORMAL )
		self.loadMenuItem.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ) )
		self.fileMenu.Append( self.loadMenuItem )

		self.menuBar.Append( self.fileMenu, u"File" )

		self.SetMenuBar( self.menuBar )

		mainSizer = wx.BoxSizer( wx.VERTICAL )

		self.auiToolBar = wx.aui.AuiToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.aui.AUI_TB_HORZ_LAYOUT )
		self.toolNewProject = self.auiToolBar.AddTool( wx.ID_ANY, u"New", wx.ArtProvider.GetBitmap( wx.ART_NEW, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.auiToolBar.AddSeparator()

		self.toolLoadProject = self.auiToolBar.AddTool( wx.ID_ANY, u"Load", wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_TOOLBAR ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )

		self.auiToolBar.Realize()

		mainSizer.Add( self.auiToolBar, 0, wx.ALL, 5 )


		self.SetSizer( mainSizer )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# connect events
		self.Bind(wx.EVT_TOOL, self.showProjectViewGUI, self.toolNewProject)
		self.Bind(wx.EVT_TOOL, self.loadProject, self.toolLoadProject)

	def __del__( self ):
		pass

	def showProjectViewGUI(self, event):
		pub.sendMessage(AppGUITopics.SHOW_PROEJCT_VIEW_GUI.value)

	def loadProject(self, event):
		with wx.FileDialog(self, "Select project", wildcard="txt files (*.txt)|*.txt", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			filePath = fileDialog.GetPath()
			pub.sendMessage(AppGUITopics.LOAD_PROJECT.value, projectFilePath = filePath)