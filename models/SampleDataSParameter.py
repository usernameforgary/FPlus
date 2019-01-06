from typing import List

from .SampleDataPoint import SampleDataPoint

class SampleDataSParameter:
	def __init__(self, dataSParameterName:str = None, dataFrequency:List[str] = None, sampleDataPoints:List[SampleDataPoint] = None):
		self.dataSParameterName: str = dataSParameterName
		self.dataFrequency:List[str] = dataFrequency if dataFrequency is not None else []
		self.sampleDataPoints: List[SampleDataPoint] = sampleDataPoints if sampleDataPoints is not None else []