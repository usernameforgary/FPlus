import numpy as np
from .test_mock_data import mockDataFreq, mockDataS21, mockDataS22, mockDataS11

def mockGetDataBySParameterName(SparameterName):
	mockData = None
	if SparameterName == "S11":
		dataLength = mockDataS11.shape[0]
		index = np.random.randint(dataLength, size=1)
		index = index[0]
		mockData = mockDataS11[index]
	elif SparameterName == "S22":
		dataLength = mockDataS22.shape[0]
		index = np.random.randint(dataLength, size=1)
		index = index[0]
		mockData = mockDataS22[index]
	elif SparameterName == "S21":
		dataLength = mockDataS21.shape[0]
		index = np.random.randint(dataLength, size=1)
		index = index[0]
		mockData = mockDataS21[index]

	yMatric = np.reshape(mockData, (len(mockDataFreq), 2))
	yMatric = np.square(yMatric)
	yMatric = yMatric.sum(axis=1)
	yMatric = np.sqrt(yMatric)
	yMatric = np.log10(yMatric)
	yMatric = 20 * yMatric
	return (mockDataFreq, yMatric)
