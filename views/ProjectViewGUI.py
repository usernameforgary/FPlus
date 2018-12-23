import wx
import wx.dataview
import wx.grid
import wx.lib.agw.customtreectrl as customtreectrl

from pubsub import pub

from topics.Topics import ProjectViewTopics
from enumObjs.EnumObjs import ElementType
from models.view_models.TreeItem import TreeItem

class ProjectViewGUI(wx.Frame):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Project Viewer", size = wx.Size( 600,400 ), pos = wx.DefaultPosition, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		#Font
		self.SetFont( wx.Font( 9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )	
		self.viewProjectMenubar = wx.MenuBar( 0 )
		self.viewProjectMenubar.SetFont( wx.Font( 9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Consolas" ) )

		# Menubar settings
		self.viewProjectMenu = wx.Menu()
		self.newProjectMenuItem = wx.MenuItem( self.viewProjectMenu, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
		self.viewProjectMenu.Append( self.newProjectMenuItem )
		self.viewProjectMenu.AppendSeparator()
		self.openProjectMenuItem = wx.MenuItem( self.viewProjectMenu, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.viewProjectMenu.Append( self.openProjectMenuItem )
		self.viewProjectMenubar.Append( self.viewProjectMenu, u"Project" )
		self.projectViewProductMenu = wx.Menu()
		self.addProductMenuItem = wx.MenuItem( self.projectViewProductMenu, wx.ID_ANY, u"Add Product", wx.EmptyString, wx.ITEM_NORMAL )
		self.projectViewProductMenu.Append( self.addProductMenuItem )
		self.viewProjectMenubar.Append( self.projectViewProductMenu, u"Product" )

		self.SetMenuBar( self.viewProjectMenubar )

		# Sizer
		mainSizer = wx.BoxSizer( wx.VERTICAL )
		leftSizer = wx.BoxSizer( wx.HORIZONTAL )

		# Project tree
		self.projectTreeCtrl = customtreectrl.CustomTreeCtrl( self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, 
																													style=0, agwStyle=wx.TR_DEFAULT_STYLE | wx.TR_EDIT_LABELS, validator=wx.DefaultValidator)

		leftSizer.Add( self.projectTreeCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		rightGridSizer = wx.GridBagSizer(hgap=1, vgap=1)

		self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid1.CreateGrid( 5, 5 )
		self.m_grid1.EnableEditing( False )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )

		# Columns
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		rightGridSizer.Add( self.m_grid1, pos=(0,0) )


		leftSizer.Add( rightGridSizer, 1, wx.EXPAND, 5 )


		mainSizer.Add( leftSizer, 1, wx.EXPAND, 5 )


		self.SetSizerAndFit(mainSizer)
		self.Layout()
		self.projectViewStatusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.HORIZONTAL)

		# connect event
		self.Bind(wx.EVT_TOOL, self.newProject ,self.newProjectMenuItem)
		self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnProjectTreeLabelBeginEdit, self.projectTreeCtrl)
		self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnProjectTreeLabelEndEdit, self.projectTreeCtrl)
		self.projectTreeCtrl.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)
		self.projectTreeCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

		# subscribe topics
		pub.subscribe(self.modelNewProject, ProjectViewTopics.MODEL_NEW_PROJECT.value)
		pub.subscribe(self.modelNewProduct, ProjectViewTopics.MODEL_NEW_PRODUCT.value)

	def newProject(self, event):
		pub.sendMessage(ProjectViewTopics.GUI_NEW_PROJECT.value)

	def modelNewProject(self, modelData):
		rootItem = self.projectTreeCtrl.GetRootItem()
		if(rootItem is None):
			treeItemViewModel = TreeItem(ElementType.PROJECT, [0], modelData.projectName)	
			root = self.projectTreeCtrl.AddRoot(modelData.projectName, data = treeItemViewModel)
		else:
			self.projectViewStatusBar.SetStatusText('Project already exists')

	def onRightDown(self, event):
		pt = event.GetPosition()
		item, flags = self.projectTreeCtrl.HitTest(pt)
		if item:
			self.projectTreeCtrl.SelectItem(item)

	def OnRightUp(self, event):
		menu = wx.Menu()
		pt = event.GetPosition();
		item, flags = self.projectTreeCtrl.HitTest(pt)
		# itemPyData is an instance of TreeItem
		if item is not None:
			itemPyData = self.projectTreeCtrl.GetPyData(item)
			itemType = itemPyData.itemType
			if itemType is ElementType.PROJECT:
				addProcutRightMenu = menu.Append(wx.ID_ANY,"Add Product")
				self.Bind(wx.EVT_MENU, self.menuAddNewProduct, addProcutRightMenu)
			elif itemType is ElementType.PRODUCT:
				addTuningPhaseMenu = menu.Append(wx.ID_ANY, "Duplicate")
				self.Bind(wx.EVT_MENU, self.menuDuplicate, addTuningPhaseMenu)

			self.PopupMenu(menu)

	def OnProjectTreeLabelBeginEdit(self, event):
		item = event.GetItem()
		#print(self.projectTreeCtrl.GetItemText(item))


	def OnProjectTreeLabelEndEdit(self, event):
		item = event.GetItem()
		itemText = item.GetText()
		itemPyData = self.projectTreeCtrl.GetPyData(item)

		itemPyData.itemText = itemText
		pub.sendMessage(ProjectViewTopics.GUI_TREE_ITEM_RENAME.value, modelData=itemPyData)

	def menuAddNewProduct(self, event):
		pub.sendMessage(ProjectViewTopics.GUI_NEW_PRDUCT.value)

	def menuDuplicate(self, event):
		item = event.GetEventObject()
		print(dir(self.projectTreeCtrl.GetItemData(item)))
		pub.sendMessage(ProjectViewTopics.GUI_DUPLICATE_TUNNING_PAHSE.value)

	def modelNewProduct(self, newProduct):
		root = self.projectTreeCtrl.GetRootItem()
		existProductCount = self.projectTreeCtrl.GetChildrenCount(root, recursively=False)
		treeItemViewModel = TreeItem(ElementType.PRODUCT, [0, existProductCount])
		self.projectTreeCtrl.AppendItem(root, newProduct.productName, data = treeItemViewModel)