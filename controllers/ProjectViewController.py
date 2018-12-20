from Views.ProjectView import ProjectView

class ProjectViewController:
	def __init__(self):
		self.gui = ProjectView()

	def showView(self):
		self.gui.Show()