from pubsub import pub
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

		# subscibe events
		pub.subscribe(self.newProject, ProjectViewTopics.GUI_NEW_PROJECT.value)
		pub.subscribe(self.newProduct, ProjectViewTopics.GUI_NEW_PRDUCT.value)
		pub.subscribe(self.editProjectOrProductName, ProjectViewTopics.GUI_TREE_ITEM_RENAME.value)

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
		print('------recevied data')
		itemType = modelData.itemType
		itemIndex = modelData.itemIndex
		itemText = modelData.itemText
		print(itemType)
		print(itemIndex)
		print(itemText)