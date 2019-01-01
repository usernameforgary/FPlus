import wx

class SizerUtils:
	@classmethod
	def cleanSizer(sizer):
		if isinstance(sizer, wx.Sizer):
			sizerItemList = sizer.GetChildren()
			if sizerItemList:
			for item in sizerItemList:
				if item.IsWindow():
					window = item.GetWindow()
					window.Destroy()
				else:
					raise Exception('No-window object in rightSizer')
		else:
			raise Exception('Not a wx Sizer')
