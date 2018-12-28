from pubsub import pub

from models.Topology import Topology 
from topics.Topics import ProjectViewTopics
from topics.Topics import TopoloyViewTopics

from models.view_models.TopologyViewModel import TopologyViewModel

class TopologyController:
	def __init__(self, model: Topology = None):
		self.topology = model

		pub.subscribe(self.editTopology, TopoloyViewTopics.GUI_EDIT_TOPOLOGY.value)

	def showTopology(self):
		pub.sendMessage(ProjectViewTopics.MODEL_SHOW_TOPOLOGY.value, topology = self.topology)

	def editTopology(self, data):
		print('...........View model recieved.....')



			