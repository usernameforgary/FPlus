import numpy as np

class AnalyzerDataUtil:
	@staticmethod
	def analyzerStrArr2NumpyFloatArr(strArr):
		npStrArr = np.array(strArr)
		return npStrArr.astype(np.float)
	# convert str list marker values(Real, Imaginary) to numpy float list
	@staticmethod
	def analyzerMarkerValues2LogMag(freqStrArr, markerValStrArr):
		markerValFloatArr = AnalyzerDataUtil.analyzerStrArr2NumpyFloatArr(markerValStrArr)
		lenFreq = len(freqStrArr)
		squareMarkers = np.square(markerValFloatArr)
		#reshape markers to Real and Imaginary
		reshapeMarkers = squareMarkers.reshape(lenFreq, 2)
		reshapeMarkersSum = np.sum(reshapeMarkers, axis=1)
		markersSqrt = np.sqrt(reshapeMarkersSum)
		markerValues = 20 * np.log10(markersSqrt)
		return markerValues