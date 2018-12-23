from enumObjs.EnumObjs import ElementType
from typing import List

class TreeItem:
	def __init__(self, itemType: ElementType, itemIndex: List = None, itemText: str = None):
		self.itemType = itemType
		self.itemIndex = itemIndex
		self.itemText = itemText