from pubsub import pub

from models.Topology import Topology 
from topics.Topics import ProjectViewTopics

class TopologyController:
	def __init__(self, model: Topology = None):
		self.topology = model

	def showTopology(self):
		pub.sendMessage(ProjectViewTopics.MODEL_SHOW_TOPOLOGY.value, topology = self.topology)


			