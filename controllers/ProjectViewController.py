import wx
import copy

from pubsub import pub
from views.ProjectViewGUI import ProjectViewGUI
from topics.Topics import ProjectViewTopics
from topics.Topics import TopologyViewTopics
from models.ProjectViewModel import ProjectViewModel
from models.ProjectTree import ProjectTree
from models.Product import Product
from enumObjs.EnumObjs import ElementType
from enumObjs.EnumObjs import ProjectOperate
from .ProductConfigController import ProductConfigController
from utils.JsonConvert import JsonConvert

class ProjectViewController:
	def __init__(self, model: ProjectViewModel = None):
		self.model = model if model is not None else ProjectViewModel()
		self.gui = ProjectViewGUI(None, self.model)
		self.productController =  None

		# subscibe events
		pub.subscribe(self.newProject, ProjectViewTopics.GUI_NEW_PROJECT.value)
		pub.subscribe(self.newProduct, ProjectViewTopics.GUI_NEW_PRDUCT.value)
		pub.subscribe(self.editProjectOrProductName, ProjectViewTopics.GUI_TREE_ITEM_RENAME.value)
		pub.subscribe(self.duplicateProduct, ProjectViewTopics.GUI_DUPLICATE_PRODUCT.value)
		pub.subscribe(self.saveProjectToFile, ProjectOperate.SAVE_TO_FILE.value)

	def showProjectView(self):
		self.gui.Show()

	def saveProjectToFile(self):
		projectJsonStr = JsonConvert.ToJSON(self.model)
		with open("C:\\Users\\usern\\Desktop\\" + self.model.projectTree.projectName + ".txt", "w") as text_file:
			print(projectJsonStr, file=text_file)

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

	def duplicateProduct(self, data):
		itemType = data.itemType
		itemIndex = data.itemIndex
		itemText = data.itemText
		if itemIndex:
			productIndex = itemIndex[1]
			product = self.model.projectTree.products[productIndex]
			newProduct = copy.deepcopy(product)
			newProduct.productName = newProduct.productName + '_copy'
			self.model.projectTree.products.append(newProduct)
		self.refreshTreeContrl()

	# refresh view tree control with new data
	def refreshTreeContrl(self):
		pub.sendMessage(ProjectViewTopics.MODEL_REFRESH_TREE_CONTRL.value, data=self.model.projectTree)