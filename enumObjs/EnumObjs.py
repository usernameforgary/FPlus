from enum import Enum, unique

@unique
class ElementType(Enum):
	PROJECT = 'PROJECT'
	PRODUCT = 'PRODUCT'
	TUNING_PHASE = 'TUNIND_PHASE'