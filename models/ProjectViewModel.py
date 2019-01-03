from .ProjectTree import ProjectTree
from utils.JsonConvert import JsonConvert

@JsonConvert.register
class ProjectViewModel:
	def __init__(self):
		self.projectTree: ProjectTree = None
		self.vnaAddress: str = ''