from models.TuningPhase import TuningPhase

# from utils.MockCommunication import mockGetDataBySParameterName
from models.SampleDataSParameter import SampleDataSParameter
from models.SampleDataPoint import SampleDataPoint
from models.SampleDataPosition import SampleDataPosition
from utils.AnalyzerCommunication import AnalyzerCommunication
from utils.AnalyzerDataUtil import AnalyzerDataUtil

class SampleCollectionController:
	def __init__(self, model:TuningPhase):
		self.model = model
		self.analyzerCommunication = None

	# def MockReadData(self):
	# 	xS11, yS11 = mockGetDataBySParameterName("S11")
	# 	xS22, yS22 = mockGetDataBySParameterName("S22")
	# 	xS21, yS21 = mockGetDataBySParameterName("S21")
	# 	return (xS11, yS11, xS22, yS22, xS21, yS21)

	# TODO, currently default read S11, S22, S21
	def readDefaultData(self):
		self.analyzerCommunication = AnalyzerCommunication.getInstance('192.168.253.253')
		self.analyzerCommunication.openConnection()
		if self.analyzerCommunication.session is not None:
			S11Freq, S11MarkerValues = self.analyzerCommunication.getDataBySParameterName("S11")
			S22Freq, S22MarkerValues = self.analyzerCommunication.getDataBySParameterName("S22")
			S21Freq, S21MarkerValues = self.analyzerCommunication.getDataBySParameterName("S21")

			S11MarkerValues = AnalyzerDataUtil.analyzerMarkerValues2LogMag(S11Freq, S11MarkerValues)
			S22MarkerValues = AnalyzerDataUtil.analyzerMarkerValues2LogMag(S22Freq, S22MarkerValues)
			S21MarkerValues = AnalyzerDataUtil.analyzerMarkerValues2LogMag(S21Freq, S21MarkerValues)
			S11Freq = AnalyzerDataUtil.analyzerStrArr2NumpyFloatArr(S11Freq)
			S22Freq = AnalyzerDataUtil.analyzerStrArr2NumpyFloatArr(S22Freq)
			S21Freq = AnalyzerDataUtil.analyzerStrArr2NumpyFloatArr(S21Freq)
			return (S11Freq, S11MarkerValues, S22Freq, S22MarkerValues, S21Freq, S21MarkerValues)
		else:
			return (None, None, None, None, None, None)

	def readDataSingle(self, pointNum, pointPosition):
		sParameterNames = self.model.vnaConfig.SParameter
		self.analyzerCommunication = AnalyzerCommunication.getInstance('192.168.253.253')
		self.analyzerCommunication.openConnection()
		if self.analyzerCommunication.session is not None:
			for sParameterName in sParameterNames:
				if self.model.sampleDataSParameters is None:
					self.model.sampleDataSParameters = []
				# find and initial current SampleDataSparameter with current S-Parameter Name, start
				currentSampleDataSParameter = list(filter(lambda smapleDataSparameter: smapleDataSparameter.dataSParameterName == sParameterName, self.model.sampleDataSParameters))
				if len(currentSampleDataSParameter) == 0:
					currentSampleDataSParameter = SampleDataSParameter(sParameterName)
					self.model.sampleDataSParameters.append(currentSampleDataSParameter)
				else:
					currentSampleDataSParameter = currentSampleDataSParameter[0]
				# find and initial current SampleDataSparameter with current S-Parameter Name, end

				if currentSampleDataSParameter.sampleDataPoints is None:
					currentSampleDataSParameter.sampleDataPoints = []
				currentSampleDataPoint = list(filter(lambda sampleDataPoint: sampleDataPoint.pointNumber == pointNum, currentSampleDataSParameter.sampleDataPoints))
				if len(currentSampleDataPoint) == 0:
					currentSampleDataPoint = SampleDataPoint(pointNum)
					currentSampleDataSParameter.sampleDataPoints.append(currentSampleDataPoint)
				else:
					currentSampleDataPoint = currentSampleDataPoint[0]

				if currentSampleDataPoint.sampleDataPositions is None:
					currentSampleDataPoint.sampleDataPositions = []
				currentSampleDataPosition = list(filter(lambda sampleDataPosition: sampleDataPosition.position == pointPosition, currentSampleDataPoint.sampleDataPositions))
				if len(currentSampleDataPosition) == 0:
					currentSampleDataPosition = SampleDataPosition(pointPosition)
					currentSampleDataPoint.sampleDataPositions.append(currentSampleDataPosition)
				else:
					raise Exception('This position sample already exits')

				
				freqValues, makerValues = self.analyzerCommunication.getDataBySParameterName(sParameterName)
				currentSampleDataSParameter.dataFrequency = freqValues
				currentSampleDataPosition.markerValues = makerValues

	def sampleCollectionFinish(self):
		if self.analyzerCommunication is not None:
			self.analyzerCommunication.closeConnection()
