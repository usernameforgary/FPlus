from typing import List

class TreeItem:
	def __init__(self, itemType: str = None, itemIndex: List = None, itemText: str = 'ProductName'):
		self.itemType: str = None if itemType is None else itemType
		self.itemIndex = None if itemIndex is None else itemIndex
		self.itemText = None if itemText is None else itemText