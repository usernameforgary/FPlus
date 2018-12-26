from typing import List
from .Points import Points

class Topology:
	def __init__(self):
		self.points: List[Points] = []

	def addPoint(self, point: Points = None):
		if point is None:
			raise TypeError('Point can not be None')

		self.points.append(point)