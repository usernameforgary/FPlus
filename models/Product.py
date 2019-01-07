from typing import List
from .TuningPhase import TuningPhase
from .Topology import Topology
from .VnaConfig import VnaConfig
from utils.JsonConvert import JsonConvert

@JsonConvert.register
class Product:
	def __init__(self, productName: str = "ProductName", topology: Topology = None, vnaConfig: VnaConfig = None, tuningPhases: List[TuningPhase] = None):
		self.productName: str = productName if productName is not None else'ProductName'
		self.topology: Topology = topology if  topology is not None else Topology() 
		self.tuningPhases: List[TuningPhase] = tuningPhases if tuningPhases is not None else []
		self.vnaConfig: VnaConfig = vnaConfig if vnaConfig is not None else VnaConfig()

	def addTopology(self, topology: Topology = None):
		if(topology is None):
			topology = Topology()
		self.topology = topology