import wx
from pubsub import pub

import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from models.Topology import Topology
from enumObjs.EnumObjs import DrawElementType
from enumObjs.EnumObjs import PointType

from models.view_models.DraggableLine import DraggableLine
from models.view_models.DraggablePoint import DraggablePoint
from models.view_models.TopologyViewModel import TopologyViewModel

from topics.Topics import ProjectViewTopics
from topics.Topics import TopologyViewTopics

class TopologyGUI(wx.Panel):
	topoloyFigure = plt.figure()
	def __init__(self, parent, model: Topology, showDrawnType = True):
		super().__init__(parent)
		self.parent = parent
		self.model = model 
		# draw type selected, default value is SELECT ELEMENT type	
		self.drawTypeSelected: str = ''
		# stored all points(DraggablePoint)
		self.viewModel =  TopologyViewModel()
		# start position of DarggableLine while drawing, type tuble
		self.drawingLineStart = None
		self.selectedDraggableLine = None
		self.selectedDraggablePoint = None
		# main sizer, contains every thing		
		sizer = wx.BoxSizer(wx.VERTICAL)
		# topology sizer
		topologySizer = wx.BoxSizer(wx.HORIZONTAL)

		# draw type gui config: start
		typeTitle = wx.StaticBox(self, -1, "Draw Type")
		typeBoxSizer = wx.StaticBoxSizer(typeTitle, wx.VERTICAL)
		typeGridSizer = wx.FlexGridSizer(cols = 1)
		self.typeRadioGroup = []
		selectRadioBtn = wx.RadioButton(self, -1, DrawElementType.SELECT.value)
		cavityRadioBtn = wx.RadioButton(self, -1, DrawElementType.CAVITY.value)
		couplingRadioBtn = wx.RadioButton(self, -1, DrawElementType.COUPLING.value)
		portRadioBtn = wx.RadioButton(self, -1, DrawElementType.PORT.value)
		lineRadioBtn = wx.RadioButton(self, -1, DrawElementType.LINE.value)
		self.typeRadioGroup.append(selectRadioBtn)		
		self.typeRadioGroup.append(cavityRadioBtn)		
		self.typeRadioGroup.append(couplingRadioBtn)	
		self.typeRadioGroup.append(portRadioBtn)		
		self.typeRadioGroup.append(lineRadioBtn)	
		for typeRadio in self.typeRadioGroup:
			typeGridSizer.Add(typeRadio, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT|wx.TOP, 5)
			# add event handing for typ radio buttons
			self.Bind(wx.EVT_RADIOBUTTON, self.onDrawTypeSelect, typeRadio)
		typeBoxSizer.Add(typeGridSizer, 0, wx.ALIGN_LEFT|wx.ALL, 5)
		# draw type gui config: end

		if TopologyGUI is None:
			TopologyGUI.topoloyFigure = plt.figure()
		else:
			TopologyGUI.topoloyFigure.clear()
			
		self.figure = TopologyGUI.topoloyFigure
		self.axes = self.figure.add_axes([0., 0., 1., 1.])
		self.axes.set_xlim([0, 120])
		self.axes.set_ylim([0, 80])
		self.axes.set_aspect(aspect='auto')
		#self.axes.get_xaxis().set_visible(False)
		#self.axes.get_yaxis().set_visible(False)
		self.canvas = FigureCanvas(self, -1, self.figure)
		# figure canvas connect
		self.connect()

		# initial gui and viewModel with points and lines in model data
		self.initialViewAndViewModel()

		if showDrawnType:
			topologySizer.Add(typeBoxSizer, 1, wx.ALL|wx.EXPAND, 0)
			topologySizer.Add(self.canvas, 6, wx.ALL | wx.EXPAND, 0)
		else:
			topologySizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 0)

		sizer.Add(topologySizer, 1, wx.ALL|wx.EXPAND, 0)

		self.SetSizer(sizer)	

	# draw type radio button event handler
	def onDrawTypeSelect(self, event):
		typeRadioSelected = event.GetEventObject()
		self.drawTypeSelected = typeRadioSelected.GetLabel()
		#DraggablePoint
		DraggablePoint.selectedDrawType = typeRadioSelected.GetLabel()

	def connect(self):
		# mouse button click event
		self.cidpress = self.canvas.mpl_connect('button_press_event', self.onPress)
		# mouse button release event
		self.cidrelease = self.canvas.mpl_connect('button_release_event', self.onRelease)
		# mouse button moving event
		self.cidmotion = self.canvas.mpl_connect('motion_notify_event', self.onMotion)
		# canvas pick up pickable element event
		self.pick = self.canvas.mpl_connect('pick_event', self.onPick)
		# canvas key press event
		self.onKeyPress = self.canvas.mpl_connect('key_press_event', self.onKey)

	# canvas key press event handler
	def onKey(self, event):
		if event.key == 'delete':
			if self.drawTypeSelected == DrawElementType.SELECT.value:
				if self.selectedDraggableLine is not None:
					deleteLine = self.selectedDraggableLine
					# remove reference in points which this line connected.
					self.removeLine(deleteLine)
					# remove line in view model
					self.addOrRemovePointOrLine(self.viewModel.lines, deleteLine, False)
					deleteLine.remove()
					self.canvas.draw()
					# This set vary important. Other wise, can not select other line
					DraggableLine.picking = None
					self.selectedDraggableLine = None
				elif self.selectedDraggablePoint is not None:
					deletePoint = self.selectedDraggablePoint
					# remove lines in siblings connected with this point
					self.removePoint(deletePoint)
					# remove points in viewModel
					self.addOrRemovePointOrLine(self.viewModel.points, deletePoint, False)
					DraggableLine.picking = None
					deletePoint.remove()
					# This set vary important. Other wise, can not select other point 
					self.canvas.draw()
					DraggablePoint.picking = None
					self.selectedDraggablePoint = None

	# remove reference to this point, in Two connected Point
	def removeLine(self, deleteLine):
		for connectP in deleteLine.points:
			for line in connectP.toMeLines:
				if line is deleteLine:
					connectP.toMeLines.remove(line)
			for line in connectP.fromMeLines:
				if line is deleteLine:
					connectP.fromMeLines.remove(line)

	def removePoint(self, deletePoint):
		for line in deletePoint.toMeLines:
			for connectP in line.points:
				if connectP is not deletePoint:
					for toPLine in connectP.toMeLines:
						if toPLine is line:
							connectP.toMeLines.remove(line)
					for fromPLine in connectP.fromMeLines:
						if fromPLine is line:
							connectP.fromMeLines.remove(line)
			# view model remove this line
			self.addOrRemovePointOrLine(self.viewModel.lines, line, False)
			line.remove()
		for line in deletePoint.fromMeLines:
			for connectP in line.points:
				if connectP is not deletePoint:
					for toPLine in connectP.toMeLines:
						if toPLine is line:
							connectP.toMeLines.remove(line)
					for fromPLine in connectP.fromMeLines:
						if fromPLine is line:
							connectP.fromMeLines.remove(line)
			# view model remove this line
			self.addOrRemovePointOrLine(self.viewModel.lines, line, False)
			line.remove()

	def onPick(self, event):
		if event.artist:
			# Select draw element allowed
			if self.drawTypeSelected == DrawElementType.SELECT.value:
				# change selected Point and Line
				if(isinstance(event.artist, DraggablePoint)):
					self.selectedDraggablePoint = event.artist
					if self.selectedDraggableLine is not None:
						self.selectedDraggableLine.switchSeletedStyle(toDefault=True)
						self.selectedDraggableLine = None
				elif (isinstance(event.artist, DraggableLine)):
					self.selectedDraggableLine = event.artist
					if self.selectedDraggablePoint is not None:
						self.selectedDraggablePoint.switchSeletedStyle(toDefault=True)
						self.selectedDraggablePoint = None
				event.artist.onPick(event)
			elif self.drawTypeSelected == DrawElementType.LINE.value:
				# draw line
				pickedArtist = event.artist	
				if isinstance(pickedArtist, DraggablePoint):
					self.drawingLineStart = event.artist.center
				
	def onMotion(self, event):
		pass

	def onPress(self, event):
			xdata = event.xdata
			ydata = event.ydata
			if xdata and ydata:
				# ADD new Point
				if event.dblclick:
					if self.drawTypeSelected is None or self.drawTypeSelected is '':
						# do nothing
						return	
					circle = None
					if self.drawTypeSelected == DrawElementType.CAVITY.value:
						circle = DraggablePoint(self, (xdata, ydata), 2.5, facecolor='black', edgecolor="black", alpha=None, pointType=PointType.CAVITY.value)
					elif self.drawTypeSelected == DrawElementType.COUPLING.value:
						circle = DraggablePoint(self, (xdata, ydata), 1.5, facecolor='black', edgecolor="black", alpha=None, pointType=PointType.COUPLING.value)
					elif self.drawTypeSelected == DrawElementType.PORT.value:
						circle = DraggablePoint(self, (xdata, ydata), 2.5, facecolor='none', edgecolor="black", alpha=None, pointType=PointType.PORT.value)

					if circle is not None:
						self.axes.add_patch(circle)
						circle.connect()	
						# Add new Point
						self.addOrRemovePointOrLine(self.viewModel.points, circle, True)
						self.canvas.draw()
				else:
					pass

	def onRelease(self, event):
		if (self.drawTypeSelected == DrawElementType.LINE.value) and (self.drawingLineStart is not None):
			xStart, yStart = self.drawingLineStart
			newLine = DraggableLine(self, [xStart, event.xdata], [yStart, event.ydata])	
			self.addNewLine((xStart, yStart), (event.xdata, event.ydata))
			self.drawingLineStart = None
	
	# startPos, stopPos are type of cuble. (xPos, yPos)
	def addNewLine(self, startPos, stopPos):
		startX, startY = startPos
		stopX, stopY = stopPos
		# find point closest to the stop postion
		startPoint = None
		stopClosestPoint = None
		closestDistance = None
		for point in self.viewModel.points:
			pCenterX, pCenterY = point.center
			if pCenterX == startX and pCenterY == startY:
				startPoint = point	
			else:
				curDistance = abs(pCenterX - stopX)	+ abs(pCenterY - stopY)
				if closestDistance is None or closestDistance > curDistance:
					closestDistance = curDistance
					stopClosestPoint = point
		if stopClosestPoint is not None:
			pCenteX, pCenterY = stopClosestPoint.center
			if pCenterX != startX and pCenterY != startY:
				newLine = DraggableLine(self, [startX, pCenteX], [startY, pCenterY])	
				#new line add two points it connected. COMMENT start
				newLine.points.append(startPoint)
				newLine.points.append(stopClosestPoint)
				#new line add two points it connected. COMMENT stop 
				# viewModel add new line
				self.addOrRemovePointOrLine(self.viewModel.lines, newLine, True)
				self.axes.add_line(newLine)
				self.canvas.draw()	
				startPoint.fromMeLines.append(newLine)
				stopClosestPoint.toMeLines.append(newLine)

	# Add(remove) points or lines to view model
	def addOrRemovePointOrLine(self, lists, element, isAdd=True):
		if lists is not None and element is not None:
			if lists is self.viewModel.points:
				if isAdd:
					self.viewModel.addPoint(element)
				else:
					self.viewModel.removePoint(element)
				pub.sendMessage(TopologyViewTopics.GUI_EDIT_TOPOLOGY.value, data = self.viewModel, model = self.model)
			elif lists is self.viewModel.lines:
				if isAdd:
					self.viewModel.addLine(element)
				else:
					self.viewModel.removeLine(element)
				pub.sendMessage(TopologyViewTopics.GUI_EDIT_TOPOLOGY.value, data = self.viewModel, model = self.model)

	def initialViewAndViewModel(self):
		# index of latest point, not PORT type Point
		latestNonPortPointIndex = -1
		pointIndex = 0
		for modelPoint in self.model.points:
			guiPositionX = modelPoint.guiPositionX
			guiPositionY = modelPoint.guiPositionY
			pointType = modelPoint.pointType
			guiPoint = None
			if pointType == PointType.CAVITY.value:
				guiPoint = DraggablePoint(self, (guiPositionX, guiPositionY), 2.5, facecolor='black', edgecolor="black", alpha=None, pointType=PointType.CAVITY.value)
				latestNonPortPointIndex += 1
			elif pointType == PointType.COUPLING.value:
				guiPoint = DraggablePoint(self, (guiPositionX, guiPositionY), 1.5, facecolor='black', edgecolor="black", alpha=None, pointType=PointType.COUPLING.value)
				latestNonPortPointIndex += 1
			elif pointType == PointType.PORT.value:
				guiPoint = DraggablePoint(self, (guiPositionX, guiPositionY), 2.5, facecolor='none', edgecolor="black", alpha=None, pointType=PointType.PORT.value)
			if guiPoint is not None:
				self.axes.add_patch(guiPoint)
				self.axes.annotate(str(pointIndex), (guiPositionX+2, guiPositionY+2))
				guiPoint.connect()
				self.viewModel.points.append(guiPoint)
			pointIndex += 1
			
		if latestNonPortPointIndex != -1:
			latestPoint = self.viewModel.points[latestNonPortPointIndex]
			latestPoint.set_edgecolor('red')
		if self.model.lines is not None:
			for modelLine in self.model.lines:
				xPos = modelLine.xPos
				yPos = modelLine.yPos
				guiLine = DraggableLine(self, xPos, yPos)
				for point in self.viewModel.points:
					lineStartX = xPos[0]
					lineStopX = xPos[1]
					lineStartY = yPos[0]
					lineStopY = yPos[1]
					x0, y0 = point.center
					if lineStartX == x0 and lineStartY == y0:
						guiLine.points.append(point)
						point.fromMeLines.append(guiLine)
					elif lineStopX == x0 and lineStopY == y0:
						guiLine.points.append(point)
						point.toMeLines.append(guiLine)
				self.viewModel.lines.append(guiLine)
				self.axes.add_line(guiLine)