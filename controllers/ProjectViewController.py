import wx

from pubsub import pub
from .TopologyController import TopologyController
from views.ProjectViewGUI import ProjectViewGUI
from topics.Topics import ProjectViewTopics
from models.ProjectViewModel import ProjectViewModel
from models.ProjectTree import ProjectTree
from models.Product import Product
from enumObjs.EnumObjs import ElementType

class ProjectViewController:
	def __init__(self):
		self.gui = ProjectViewGUI(None)
		self.model = ProjectViewModel()
		self.topologyController = None

		# subscibe events
		pub.subscribe(self.newProject, ProjectViewTopics.GUI_NEW_PROJECT.value)
		pub.subscribe(self.newProduct, ProjectViewTopics.GUI_NEW_PRDUCT.value)
		pub.subscribe(self.editProjectOrProductName, ProjectViewTopics.GUI_TREE_ITEM_RENAME.value)
		pub.subscribe(self.switchProjectItem, ProjectViewTopics.GUI_TREE_ITEM_SELECTED.value)

	def showProjectView(self):
		self.gui.Show()

	def newProject(self):
		projectTree = ProjectTree()
		self.model.projectTree = projectTree
		pub.sendMessage(ProjectViewTopics.MODEL_NEW_PROJECT.value, modelData = projectTree)

	def newProduct(self):
		product = Product()	
		self.model.projectTree.products.append(product)
		pub.sendMessage(ProjectViewTopics.MODEL_NEW_PRODUCT.value, newProduct = product)

	def editProjectOrProductName(self, modelData):	
		itemType = modelData.itemType
		itemIndex = modelData.itemIndex
		itemText = modelData.itemText
		if(itemType is ElementType.PROJECT):
			self.model.projectTree.projectName = itemText
		elif(itemType is ElementType.PRODUCT):
			productIndex = itemIndex[1]
			self.model.projectTree.products[productIndex].productName = itemText

	def switchProjectItem(self, modelData):
		itemType = modelData.itemType
		itemIndex = modelData.itemIndex
		itemText = modelData.itemText
		if(itemType is ElementType.PROJECT):
			# TODO currentlly do noting
			pass
		elif(itemType is ElementType.PRODUCT):
			productIndex = itemIndex[1]
			selectedProduct = self.model.projectTree.products[productIndex]
			topology = selectedProduct.topology
			if(topology is None):
				selectedProduct.addTopology()

			self.topologyController = TopologyController(selectedProduct.topology)
			self.topologyController.showTopology()	