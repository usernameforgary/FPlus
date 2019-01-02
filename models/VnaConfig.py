from typing import List

from .SweepTable import SweepTable

class VnaConfig:
	def __init__(self, SParameter: List[str] = None, sweepType: str = None, sweepTables: List[SweepTable] = None):
		self.SParameter: List[str] = SParameter if SParameter is not None else ['S11']
		self.sweepType: str = sweepType if sweepType is not None else 'Linear'
		self.sweepTables: List[SweepTable] = sweepTables if sweepTables is not None else []