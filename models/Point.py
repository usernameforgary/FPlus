from typing import List
from enumObjs.EnumObjs import PointType

from .Line import Line

class Point:
	def __init__(self, pointType: PointType, pointIndex: int, guiPositionX: float, guiPositionY: float, pointLabel: str = '',fromMeLines: List[Line] = [], toMeLines:List[Line] = []):
		self.pointType: PointType = None
		self.pointLabel: str = ""
		self.pointIndex: int = None

		self.guiPositionX: float = None
		self.guiPositionY: float = None
		self.fromMeLines: List[Line] = []
		self.toMeLines: List[Line] = []

	def setGUIPosition(self, positionX: float, positionY: float):
		self.guiPositionX = positionX
		self.guiPositionY = positionY