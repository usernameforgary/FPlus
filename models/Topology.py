from typing import List
from .Point import Point
from .Line import Line

class Topology:
	def __init__(self, points: List[Point] = [], lines: List[Line] = []):
		self.points: List[Point] = points
		self.Lines: List[Line] = lines

	def addPoint(self, point: Point = None):
		if point is None:
			raise TypeError('Point can not be None')
		self.points.append(point)