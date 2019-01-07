from typing import List

from utils.JsonConvert import JsonConvert

@JsonConvert.register
class Line:
	def __init__(self, xPos:List[float] = None, yPos: List[float] = None):
		self.xPos:List[float] = xPos if xPos is not None else []
		self.yPos:List[float] = yPos if yPos is not None else []