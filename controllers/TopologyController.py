from pubsub import pub

from models.Topology import Topology 
from topics.Topics import TopologyViewTopics

from models.view_models.TopologyViewModel import TopologyViewModel
from views.TopologyGUI import TopologyGUI

from models.Point import Point
from models.Line import Line

class TopologyController:
	def __init__(self, model: Topology):
		self.model = model 

		pub.subscribe(self.editTopology, TopologyViewTopics.GUI_EDIT_TOPOLOGY.value)

	def initialView(self, parentGUI):
		return TopologyGUI(parentGUI, self.model)

	def editTopology(self, data, model):
		# TODO
		if model is self.model:
			self.viewModelToModelReplace(data)

	def viewModelToModelReplace(self, viewModel: TopologyViewModel):
		self.model.points = [] 
		self.model.lines = []
		for guiPoint in viewModel.points:
			x0, y0 = guiPoint.center
			pointType = guiPoint.pointType
			modelPoint = Point(pointType, len(self.model.points), x0, y0)
			self.model.points.append(modelPoint)
		for guiLine in viewModel.lines:
			xPos = guiLine.get_xdata()
			yPos = guiLine.get_ydata()
			modelLine = Line(xPos, yPos)
			self.model.lines.append(modelLine)