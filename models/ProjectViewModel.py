from .ProjectTree import ProjectTree
from utils.JsonConvert import JsonConvert

@JsonConvert.register
class ProjectViewModel:
	def __init__(self, projectTree: ProjectTree = None, vnaAddress: str = None):
		self.projectTree: ProjectTree = None if projectTree is None else projectTree
		self.vnaAddress: str = ''