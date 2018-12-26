from typing import List
from .TuningPhase import TuningPhase
from .Topology import Topology

class Product:
	def __init__(self):
		self.productName: str = 'Product1'
		self.topology: Topology = None
		self.tuningPhases: List[TuningPhase] = []

	def addTopology(self, topology: Topology = None):
		if(topology is None):
			topology = Topology()
		self.topology = topology