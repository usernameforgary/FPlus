import wx

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.lines import Line2D

from models.Topology import Topology
from enumObjs.EnumObjs import DrawElementType

class TopologyGUI(wx.Panel):
	def __init__(self, parent, topology: Topology):
		super().__init__(parent)
		self.parent = parent
		# draw type selected, default value is SELECT ELEMENT type	
		self.drawTypeSelected: str = DrawElementType.SELECT.value
		# stored all points(DraggablePoint)
		self.points = []
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

		self.figure = plt.figure()
		self.axes = self.figure.add_axes([0., 0., 1., 1.])
		self.axes.set_xlim([0, 120])
		self.axes.set_ylim([0, 80])
		self.axes.set_aspect('equal')
		#self.axes.get_xaxis().set_visible(False)
		#self.axes.get_yaxis().set_visible(False)
		self.canvas = FigureCanvas(self, -1, self.figure)

		# figure canvas connect
		self.connect()

		topologySizer.Add(typeBoxSizer, 1, wx.ALL|wx.EXPAND, 0)
		topologySizer.Add(self.canvas, 6, wx.ALL | wx.EXPAND, 0)

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
					deleteLine.remove()
					self.canvas.draw()
					# This set vary important. Other wise, can not select other line
					DraggableLine.picking = None
					self.selectedDraggableLine = None
				elif self.selectedDraggablePoint is not None:
					deletePoint = self.selectedDraggablePoint
					# remove lines in siblings connected with this point
					self.removePoint(deletePoint)
					DraggableLine.picking = None
					deletePoint.remove()
					# This set vary important. Other wise, can not select other point 
					self.canvas.draw()
					DraggablePoint.picking = None
					self.selectedDraggablePoint = None

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
				if event.dblclick:
					if self.drawTypeSelected is None or self.drawTypeSelected is '':
						self.parent.projectViewStatusBar.SetStatusText("Please select 'Draw Type' first, than double click to draw.")
						return	
					circle = None
					if self.drawTypeSelected == DrawElementType.CAVITY.value:
						circle = DraggablePoint((xdata, ydata), 2.5, facecolor='black', edgecolor="black", alpha=None, pointType=DrawElementType.CAVITY.value)
					elif self.drawTypeSelected == DrawElementType.COUPLING.value:
						circle = DraggablePoint((xdata, ydata), 1.5, facecolor='black', edgecolor="black", alpha=None, pointType=DrawElementType.COUPLING.value)
					elif self.drawTypeSelected == DrawElementType.PORT.value:
						circle = DraggablePoint((xdata, ydata), 2.5, facecolor='none', edgecolor="black", alpha=None, pointType=DrawElementType.PORT.value)

					if circle is not None:
						self.axes.add_patch(circle)
						circle.connect()		
						self.points.append(circle)
						self.canvas.draw()
				else:
					pass

	def onRelease(self, event):
		if (self.drawTypeSelected == DrawElementType.LINE.value) and (self.drawingLineStart is not None):
			xStart, yStart = self.drawingLineStart
			newLine = DraggableLine([xStart, event.xdata], [yStart, event.ydata])	
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
		for point in self.points:
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
			newLine = DraggableLine([startX, pCenteX], [startY, pCenterY])	
			#new line add two points it connected. COMMENT start
			newLine.points.append(startPoint)
			newLine.points.append(stopClosestPoint)
			#new line add two points it connected. COMMENT stop 
			self.axes.add_line(newLine)
			self.canvas.draw()	
			startPoint.fromMeLines.append(newLine)
			stopClosestPoint.toMeLines.append(newLine)

class DraggableLine(Line2D):
	picking = None
	def __init__(self, xPos, yPos, color='black', linewidth=2.0, picker=2.0):
		super().__init__(xPos, yPos, color=color, linewidth=linewidth, picker=picker)
		# points contains two point this line connected
		self.points = []
	def onPick(self, event):
		if event.artist is self:
			curPick = DraggableLine.picking
			if curPick is not self:
				if curPick is not None:
					curPick.switchSeletedStyle(toDefault=True)
				self.switchSeletedStyle()
				DraggableLine.picking = self
			else:
				self.switchSeletedStyle()
				DraggableLine.picking = None

	def switchSeletedStyle(self, toDefault=None):
		if self is not None and isinstance(self, DraggableLine):
			targetColor = 'black'
			if(not toDefault):
				currentColor = self.get_color()
				targetColor = 'red' if (currentColor == 'black') else 'black'
			self.set_color(targetColor)
			self.figure.canvas.draw()

class DraggablePoint(patches.Circle):
	#only one can be animated at a time
	lock = None
	#only ome can be picked at a time
	picking = None
	# put this static property to get current selected type
	selectedDrawType = None
	def __init__(self, position, radius, facecolor, edgecolor, alpha=None, pointType = None):
		super().__init__(position, radius, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, picker=5)
		self.press = None
		self.background = None
		self.pointType = pointType
		#Lines draw to me
		self.toMeLines = []
		#Lines draw from me
		self.fromMeLines = []

	def connect(self):
		self.cidpress = self.figure.canvas.mpl_connect('button_press_event', self.on_press)
		self.cidrelease = self.figure.canvas.mpl_connect('button_release_event', self.on_release)
		self.cidmotion = self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
		#self.cidPick = self.figure.canvas.mpl_connect('pick_event', self.on_pick)
	
	def onPick(self, event):
		if event.artist is self:
			curPick = DraggablePoint.picking
			if curPick is not self:
				if curPick is not None:
					# switch style of previous picked element
					curPick.switchSeletedStyle(toDefault=True)
				self.switchSeletedStyle()
				DraggablePoint.picking = self
			else:
				self.switchSeletedStyle()
				DraggablePoint.picking = None

	def on_press(self, event):
		# if current selection is draw line, stop drag circle
		if DraggablePoint.selectedDrawType == DrawElementType.LINE.value: return
		if event.inaxes != self.axes: return
		if DraggablePoint.lock is not None: return
		contains, attrd = self.contains(event)
		if not contains: return
		x0, y0 = self.center
		self.press = x0, y0, event.xdata, event.ydata
		DraggablePoint.lock = self

		# draw everything but the selected rectangle and store the pixel buffer
		canvas = self.figure.canvas
		axes = self.axes
		self.set_animated(True)
		canvas.draw()
		self.background = canvas.copy_from_bbox(self.axes.bbox)

		# now redraw just the rectangle
		axes.draw_artist(self)
		# and blit just the redrawn area
		canvas.blit(axes.bbox)

	def on_motion(self, event):
		# if current selection is draw line, stop drag circle
		if DraggablePoint.selectedDrawType == DrawElementType.LINE.value: return
		if DraggablePoint.lock is not self:
			return
		if event.inaxes != self.axes: return
		x0, y0, xpress, ypress = self.press
		dx = event.xdata - xpress
		dy = event.ydata - ypress
		self.center = (x0+dx, y0+dy)

		canvas = self.figure.canvas
		axes = self.axes
		# restore the background region
		canvas.restore_region(self.background)

		# redraw just the current rectangle
		axes.draw_artist(self)

		for line in self.toMeLines:
			lineX = [line.get_xdata()[0], self.center[0]]
			lineY = [line.get_ydata()[0], self.center[1]]
			line.set_data(lineX, lineY)

		for line in self.fromMeLines:
			lineX = [self.center[0], line.get_xdata()[1]]
			lineY = [self.center[1], line.get_ydata()[1]]
			line.set_data(lineX, lineY)
		# blit just the redrawn area
		canvas.blit(axes.bbox)

	def on_release(self, event):
		if DraggablePoint.lock is not self:
			return

		self.press = None
		DraggablePoint.lock = None

		# turn off the rect animation property and reset the background
		self.set_animated(False)
		self.background = None

		# redraw the full figure
		self.figure.canvas.draw()

	def disconnect(self):
		self.figure.canvas.mpl_disconnect(self.cidpress)
		self.figure.canvas.mpl_disconnect(self.cidrelease)
		self.figure.canvas.mpl_disconnect(self.cidmotion)

	def switchSeletedStyle(self, toDefault=False):
		if self is not None and isinstance(self, DraggablePoint):
			targetColor = 'black'
			if(not toDefault):
				currentEdgeColor = self.get_edgecolor()
				targetColor = 'red' if (currentEdgeColor == mcolors.to_rgba('black')) else 'black'
			self.set_edgecolor(targetColor)
			self.axes.draw_artist(self)