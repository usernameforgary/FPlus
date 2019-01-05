from models.TuningPhase import TuningPhase

from utils.MockCommunication import mockGetDataBySParameterName

class SampleCollectionController:
	def __init__(self, model:TuningPhase):
		self.model = model

	def MockReadData(self):
		xS11, yS11 = mockGetDataBySParameterName("S11")
		xS22, yS22 = mockGetDataBySParameterName("S22")
		xS21, yS21 = mockGetDataBySParameterName("S21")
		return (xS11, yS11, xS22, yS22, xS21, yS21)