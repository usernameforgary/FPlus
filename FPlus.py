# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import wx.dataview

###########################################################################
## Class AppGUI
###########################################################################

class AppGUI ( wx.Frame ):

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

		# Connect Events
		self.Bind( wx.EVT_TOOL, self.viewProject, id = self.toolNewProject.GetId() )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def viewProject( self, event ):
		event.Skip()


###########################################################################
## Class projectViewGUI
###########################################################################

class projectViewGUI ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project", pos = wx.DefaultPosition, size = wx.Size( 1369,824 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.viewProjectMenubar = wx.MenuBar( 0 )
		self.addMenu = wx.Menu()
		self.addMenuItem = wx.MenuItem( self.addMenu, wx.ID_ANY, u"Add Product", wx.EmptyString, wx.ITEM_NORMAL )
		self.addMenu.Append( self.addMenuItem )

		self.viewProjectMenubar.Append( self.addMenu, u"Add" )

		self.SetMenuBar( self.viewProjectMenubar )

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


