import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from models.Topology import Topology

class AnalyzerResponseGUI(wx.Panel):
	responseFigure = plt.figure()
	def __init__(self, parent, model: Topology):
		super().__init__(parent)
		self.parent = parent
		self.model = model
		sizer = wx.BoxSizer(wx.VERTICAL)
		responseSizer = wx.BoxSizer(wx.HORIZONTAL)
	
		if AnalyzerResponseGUI is None:
			AnalyzerResponseGUI.responseFigure = plt.figure()
		else:
			AnalyzerResponseGUI.responseFigure.clear()

		self.figure = AnalyzerResponseGUI.responseFigure
		self.axes = self.figure.add_axes([0., 0., 1., 1.])
		#self.axes.set_xlim([0, 120])
		#self.axes.set_ylim([0, 80])
		#self.axes.set_aspect('equal')
		self.canvas = FigureCanvas(self, -1, self.figure)

		responseSizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 0)
		sizer.Add(responseSizer, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(sizer)