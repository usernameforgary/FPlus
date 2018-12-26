from .Product import Product

from typing import List

class ProjectTree:
	def __init__(self, defaultName: str = 'NewProject'):
		self.projectName: str = defaultName 
		self.products: List[Product] = []