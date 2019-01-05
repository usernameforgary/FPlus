import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

from models.Topology import Topology

class AnalyzerResponseGUI(wx.Panel):
	responseFigure = None
	def __init__(self, parent, model: Topology):
		super().__init__(parent)
		self.parent = parent
		self.model = model
		sizer = wx.BoxSizer(wx.VERTICAL)
		responseSizer = wx.BoxSizer(wx.VERTICAL)

		if AnalyzerResponseGUI.responseFigure is None:
			AnalyzerResponseGUI.responseFigure = plt.figure()
		# else:
			# AnalyzerResponseGUI.responseFigure.clear()

		self.figure = AnalyzerResponseGUI.responseFigure
		self.axes = self.figure.add_subplot(111)
		x = []
		y = []
		self.axes.plot(x,y)
		self.canvas = FigureCanvas(self, -1, self.figure)
		self.toolbar = NavigationToolbar(self.canvas)
		self.toolbar.Realize()

		responseSizer.Add(self.toolbar, 0, wx.EXPAND, 0)
		responseSizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 0)
		sizer.Add(responseSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(sizer)

	def reDrawPlot(self, xS11, yS11):
		self.axes.clear()
		self.axes.plot(xS11, yS11, 'b-')
		self.canvas.draw()

	def reDrawPlotAll(self, xS11, yS11, xS22, yS22, xS21, yS21):
		self.axes.clear()
		self.axes.plot(xS11, yS11, 'b-', xS22, yS22, 'g-', xS21, yS21, 'c-')
		self.canvas.draw()