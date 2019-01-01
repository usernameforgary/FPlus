from pubsub import pub
from models.Product import Product
from views.ProductConfigGUI import ProductConfigGUI
from topics.Topics import ProjectViewTopics
from controllers.TopologyController import TopologyController

class ProductConfigController:
	def __init__(self, model: Product):
		self.model  = model 
		self.toplogyController = TopologyController(self.model.topology)

		# show toplogy gui
		pub.subscribe(self.showTopology, ProjectViewTopics.GUI_SHOW_TOPOLOGY.value)

	# parentGUI should be instanse of GUI where ProductConfigGUI placed
	def showGUI(self, parentGUI):
		productConfigGUI = ProductConfigGUI(parentGUI, self.model)
		pub.sendMessage(ProjectViewTopics.GUI_ADD_REFRESH_PROJECT_CONFIG.value, productConfigGUI=productConfigGUI)

	def showTopology(self, parentGUI, topology):
		print("...........this called.")
		self.toplogyController.showGUI(parentGUI)