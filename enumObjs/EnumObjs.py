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
	PORT = 'PORT'

@unique
class DrawElementType(Enum):
	SELECT = "Select ELEMENT"
	CAVITY = 'Draw CAVITY'
	COUPLING = 'Draw COUPLING'
	LINE = 'Draw LINE'
	PORT = 'Draw PORT'

@unique
class SParameterType(Enum):
	S11 = 'S11'
	S22 = 'S22'
	S21 = 'S21'
	S12 = 'S12'
	
@unique
class SweepType(Enum):
	LINEAR = 'Linear',
	SEGMENT = 'Segment'