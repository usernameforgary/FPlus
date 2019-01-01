from typing import List
from .TuningPhase import TuningPhase
from .Topology import Topology

class Product:
	def __init__(self, productName: str = "ProductName", topology: Topology = None, tuningPhases: List[TuningPhase] = []):
		self.productName: str = productName if productName is not None else'ProductName'
		self.topology: Topology = topology if  topology is not None else Topology() 
		self.tuningPhases: List[TuningPhase] = tuningPhases if tuningPhases is not None else []

	def addTopology(self, topology: Topology = None):
		if(topology is None):
			topology = Topology()
		self.topology = topology