from pubsub import pub

from topics.Topics import AppGUITopics

from views.AppGUI import AppGUI
from controllers.ProjectViewController import ProjectViewController
from models.ProjectViewModel import ProjectViewModel
from views.ProjectViewGUI import ProjectViewGUI
from utils.JsonConvert import JsonConvert

class AppController:

	def __init__(self):
		self.appGui = AppGUI(None)
		self.appGui.Show()

		# subscribe events
		pub.subscribe(self.showProjectViewGUI, AppGUITopics.SHOW_PROEJCT_VIEW_GUI.value)
		pub.subscribe(self.loadProject, AppGUITopics.LOAD_PROJECT.value)

	def showProjectViewGUI(self):
		self.projectViewController = ProjectViewController()
		self.projectViewController.showProjectView()

	def loadProject(self, projectFilePath):
		projectViewModel = JsonConvert.FromFile(projectFilePath)	
		self.projectViewController = ProjectViewController(projectViewModel)
		self.projectViewController.showProjectView()