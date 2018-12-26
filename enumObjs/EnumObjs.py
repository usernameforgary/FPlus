from enum import Enum, unique

@unique
class ElementType(Enum):
	PROJECT = 'PROJECT'
	PRODUCT = 'PRODUCT'
	TUNING_PHASE = 'TUNIND_PHASE'

@unique
class PointType(Enum):
	CAVITY = 'CAVITY'
	COUPLING = 'COUPLING'

@unique
class DrawElementType(Enum):
	SELECT = "Select ELEMENT"
	CAVITY = 'Draw CAVITY'
	COUPLING = 'Draw COUPLING'
	LINE = 'Draw LINE'
	PORT = 'Draw PORT'