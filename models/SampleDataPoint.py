from typing import List

from .SampleDataPosition import SampleDataPosition

from utils.JsonConvert import JsonConvert

@JsonConvert.register
class SampleDataPoint:
	def __init__(self, pointNumber:int = None, sampleDataPositions:List[SampleDataPosition] = None):
		self.pointNumber: int = pointNumber
		self.sampleDataPositions: List[SampleDataPosition] = sampleDataPositions if sampleDataPositions is not None else []