from typing import List
from .Line import Line

class Point:
	def __init__(self, pointType: str, pointIndex: int, guiPositionX: float, guiPositionY: float, pointLabel: str = ''):
		self.pointType: str = pointType
		self.pointLabel: str = pointLabel 
		self.pointIndex: int = pointIndex 

		self.guiPositionX: float = guiPositionX 
		self.guiPositionY: float = guiPositionY

	def setGUIPosition(self, positionX: float, positionY: float):
		self.guiPositionX = positionX
		self.guiPositionY = positionY