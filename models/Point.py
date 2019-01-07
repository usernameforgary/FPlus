from typing import List
from .Line import Line

from utils.JsonConvert import JsonConvert

@JsonConvert.register
class Point:
	def __init__(self, pointType: str = None, pointIndex: int = None, guiPositionX: float = None, guiPositionY: float = None, pointLabel: str = ''):
		self.pointType: str = pointType
		self.pointLabel: str = pointLabel 
		self.pointIndex: int = pointIndex 

		self.guiPositionX: float = guiPositionX 
		self.guiPositionY: float = guiPositionY

	def setGUIPosition(self, positionX: float, positionY: float):
		self.guiPositionX = positionX
		self.guiPositionY = positionY