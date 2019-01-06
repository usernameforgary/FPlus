from typing import List
from .Topology import Topology
from .VnaConfig import VnaConfig
from .SampleDataSParameter import SampleDataSParameter

class TuningPhase:
	def __init__(self, phaseName: str = "phasename", isSubPhase: bool = None, topology: Topology = None, vnaConfig: VnaConfig = None, sampleDataSParameters: List[SampleDataSParameter] = None):
		self.tuningPhaseName: str = None if phaseName is None else phaseName
		self.isSubPhase: bool = False if isSubPhase is None else isSubPhase
		self.topology: Topology = None if topology is None else topology
		self.vnaConfig: VnaConfig = vnaConfig if vnaConfig is not None else None
		self.sampleDataSParameters: List[SampleDataSParameter] = sampleDataSParameters if sampleDataSParameters is not None else []
