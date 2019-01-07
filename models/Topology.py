from typing import List
from .Point import Point
from .Line import Line

from utils.JsonConvert import JsonConvert

@JsonConvert.register
class Topology:
	def __init__(self, points: List[Point] = None, lines: List[Line] = None):
		self.points: List[Point] = points if points is not None else []
		self.lines: List[Line] = lines if lines is not None else [] 

	def addPoint(self, point: Point = None):
		if point is None:
			raise TypeError('Point can not be None')
		self.points.append(point)