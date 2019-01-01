from typing import List
from .DraggablePoint import DraggablePoint
from .DraggableLine import DraggableLine

class TopologyViewModel:
	def __init__(self, points: List[DraggablePoint] = None, lines: List[DraggableLine] = None):
		self.points:List[DraggablePoint] = points if points is not None else []
		self.lines:List[DraggableLine] = lines if lines is not None else []

	def addLine(self, line: DraggableLine):
		self.lines.append(line)
	def removeLine(self, line: DraggableLine):
		if line is not None and line in self.lines:
			self.lines.remove(line)
	def addPoint(self, point: DraggablePoint):
		self.points.append(point)
	def removePoint(self, point: DraggablePoint):
		if point is not None and point in self.points:
			self.points.remove(point)