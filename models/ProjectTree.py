from .Product import Product

from typing import List

class ProjectTree:
	def __init__(self, defaultName: str = 'NewProject', products: List[Product] = None):
		self.projectName: str = defaultName 
		self.products: List[Product] = [] if products is None else products