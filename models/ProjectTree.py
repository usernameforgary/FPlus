from .Product import Product

from typing import List

from utils.JsonConvert import JsonConvert

@JsonConvert.register              
class ProjectTree:
	def __init__(self, projectName: str = 'NewProject', products: List[Product] = None):
		self.projectName: str = projectName 
		self.products: List[Product] = [] if products is None else products