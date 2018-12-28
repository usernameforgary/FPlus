from typing import List
from .Topology import Topology

class TuningPhase:
	def __init__(self, phaseName: str = "phasename", isSubPhase: bool = False, topology: Topology = None):
		self.tuningPhaseName: str = None if phaseName is None else phaseName
		self.isSubPhase: bool = False if isSubPhase is None else isSubPhase
		self.topology: Topology = None if topology is None else topology