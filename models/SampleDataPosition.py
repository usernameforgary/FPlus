from typing import List

from utils.JsonConvert import JsonConvert

@JsonConvert.register
class SampleDataPosition:
	def __init__(self, position:int = None, markerValues:List[str] = None):
		self.position:int = position
		self.markerValues:List[str] = markerValues if markerValues is not None else []