from pubsub import pub

from Topics.Topics import AppGUITopics

from Views.AppGUI import AppGUI
from Views.ProjectViewGUI import ProjectViewGUI

class AppController:

	def __init__(self):
		self.appGui = AppGUI(None)
		self.appGui.Show()

		pub.subscribe(self.showProjectViewGUI, AppGUITopics.SHOW_PROEJCT_VIEW_GUI.value)

	def showProjectViewGUI(self):
		self.projectViewGUI = ProjectViewGUI(None)	
		self.projectViewGUI.Show()

