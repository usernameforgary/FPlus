from pubsub import pub

from topics.Topics import AppGUITopics

from views.AppGUI import AppGUI
from controllers.ProjectViewController import ProjectViewController
from views.ProjectViewGUI import ProjectViewGUI

class AppController:

	def __init__(self):
		self.appGui = AppGUI(None)
		self.appGui.Show()

		# subscribe events
		pub.subscribe(self.showProjectViewGUI, AppGUITopics.SHOW_PROEJCT_VIEW_GUI.value)

	def showProjectViewGUI(self):
		self.projectViewController = ProjectViewController()
		self.projectViewController.showProjectView()