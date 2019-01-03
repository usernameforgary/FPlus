from pubsub import pub
import copy
from models.Product import Product
from views.ProductConfigGUI import ProductConfigGUI
from topics.Topics import ProjectViewTopics
from topics.Topics import ProductConfigTopics

from models.TuningPhase import TuningPhase

class ProductConfigController:
	def __init__(self, model: Product):
		self.model  = model 

		# show toplogy gui
		pub.subscribe(self.createTuningPhase, ProductConfigTopics.GUI_CREATE_PRODUCT_TUNING_PHASE.value)

	def initalView(self, parentGUI):
		productConfigGUI = ProductConfigGUI(parentGUI, self.model)
		return productConfigGUI

	def createTuningPhase(self):
		topology = self.model.topology
		vnaConfig = self.model.vnaConfig
		copyTopology = copy.deepcopy(topology)
		copyVnaConfig = copy.deepcopy(vnaConfig)	
		tuningPhase = TuningPhase(topology=copyTopology, vnaConfig = copyVnaConfig)
		self.model.tuningPhases.append(tuningPhase)
		pub.sendMessage(ProjectViewTopics.MODEL_REFRESH_TREE_CONTRL.value, data=None)