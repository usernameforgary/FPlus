from matplotlib.lines import Line2D

class DraggableLine(Line2D):
	picking = None
	def __init__(self, parent, xPos, yPos, color='black', linewidth=2.0, picker=2.0):
		super().__init__(xPos, yPos, color=color, linewidth=linewidth, picker=picker)
		# parent gui used this class
		self.parent = parent		
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
				if self.parent is not None:
					self.parent.selectedDraggableLine = None

	def switchSeletedStyle(self, toDefault=None):
		if self is not None and isinstance(self, DraggableLine):
			targetColor = 'black'
			if(not toDefault):
				currentColor = self.get_color()
				targetColor = 'red' if (currentColor == 'black') else 'black'
			self.set_color(targetColor)
			self.figure.canvas.draw()