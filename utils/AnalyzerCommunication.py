import visa
import wx
import numpy as np

class AnalyzerCommunication:
	__instance = None

	@staticmethod
	def getInstance(address):
		if AnalyzerCommunication.__instance == None:
			AnalyzerCommunication(address)
		return AnalyzerCommunication.__instance

	def __init__(self, address):
		if AnalyzerCommunication.__instance != None:
			raise Exception("AnalyzerCommunication is a singleton!")
		else:
			AnalyzerCommunication.__instance = self

		self.visaResourceManager = None
		self.analyzerAddress = 'TCPIP0::' + address + '::inst0::INSTR'
		self.session = None

	def openConnection(self):
		try:
			self.visaResourceManager = visa.ResourceManager()
			self.session = self.visaResourceManager.open_resource(self.analyzerAddress)
			if self.session.resource_name.startswith('ASRL') or self.session.resource_name.endswith('SOCKET'):
				self.session.read_termination = '\n'
		except visa.Error as ex:
			self.closeConnection()
			wx.MessageBox('Connection Error: {0}'.format(ex), 'Error', wx.OK|wx.ICON_ERROR)

	def checkAnalyzerConnection(self):
		try:
			self.session.write('*IDN?')
			idn = self.session.read()
			return "OK"
		except visa.Error as ex:
			self.closeConnection()
			return "{0}".format(ex)

	def getFrequencyData(self):
		try:	
			# read frequency
			self.session.write(':SENS1:FREQ:DATA?')
			freqStr = self.session.read()
			freqListStr = freqStr.split(',')
			freqNpArrayStr = np.array(freqListStr)
			freqArrayFloat = freqNpArrayStr.astype(np.float)	

			return freqResArrayFloat
		except visa.Error as ex:
			self.closeConnection()
			wx.MessageBox('errror: {0}'.format(ex))

	def getDataBySParameterName(self, SparameterName):
		try:	
			#read frequency
			self.session.write(':SENS1:FREQ:DATA?')
			freqStr = self.session.read()
			freqListStr = freqStr.split(',')
			freqNpArrayStr = np.array(freqListStr)
			freqArrayFloat = freqNpArrayStr.astype(np.float)
			self.session.write(':SENS:DATA:CORR? '+SparameterName)
			result = self.session.read()
			listStrRes = result.split(',')
			yMatric = np.array(listStrRes)
			yMatric = yMatric.astype(np.float)
			yMatric = np.reshape(yMatric, (len(freqArrayFloat), 2))
			yMatric = np.square(yMatric)
			yMatric = yMatric.sum(axis=1)
			yMatric = np.sqrt(yMatric)
			yMatric = np.log10(yMatric)
			yMatric = 20 * yMatric

			return (freqResArrayFloat, yMatric)
		except visa.Error as ex:
			self.closeConnection()
			wx.MessageBox('errror: {0}'.format(ex))

	def closeConnection(self):
		if self.session is not None:
			self.session.close()
			self.session = None
		if self.visaResourceManager is not None:
			self.visaResourceManager.close()
			self.visaResourceManager = None