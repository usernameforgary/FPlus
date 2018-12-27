import matplotlib.patches as patches
import matplotlib.colors as mcolors
from enumObjs.EnumObjs import DrawElementType

class DraggablePoint(patches.Circle):
	#only one can be animated at a time
	lock = None
	#only ome can be picked at a time
	picking = None
	# put this static property to get current selected type
	selectedDrawType = None
	def __init__(self, parent, position, radius, facecolor, edgecolor, alpha=None, pointType = None):
		super().__init__(position, radius, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, picker=5)
		self.parent = parent
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
				# set parent Topology GUI
				if self.parent is not None:
					self.parent.selectedDraggablePoint = None

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