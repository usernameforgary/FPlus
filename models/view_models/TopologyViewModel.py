from typing import List
from .DraggablePoint import DraggablePoint
from .DraggableLine import DraggableLine

class TopologyViewModel:
	def __init__(self, points: List[DraggablePoint] = [], lines: List[DraggableLine] = []):
		self.points:List[DraggablePoint] = points
		self.lines:List[DraggableLine] = lines

	def addLine(line: DraggableLine):
		self.lines.append(line)
	def removeLine(line: DraggableLine):
		if line is not None and line in self.lines:
			self.lines.remove(line)
	def addPoint(point: DraggablePoint):
		self.points.append(point)
	def removePoint(point: DraggablePoint):
		if point is not None and point in self.points:
			self.points.remove(point)