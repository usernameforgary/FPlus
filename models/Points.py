from typing import List
from enumObjs.EnumObjs import PointType

class Points:
	def __init__(self):
		self.pointType: PointType = None
		self.pointLabel: str = ""
		self.pointIndex: int = None

		self.siblingPointsIndex: List[int] = []
		self.guiPositionX: float = None
		self.guiPositionY: float = None

	def addSibling(self, siblinIndex: int):
		self.siblingPointsIndex.append(siblinIndex)

	def setGUIPosition(self, positionX: float, positionY: float):
		self.guiPositionX = positionX
		self.guiPositionY = positionY