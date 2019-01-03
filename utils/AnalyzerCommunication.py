import visa
import wx

class AnalyzerCommunication:
	__instance = None

	@staticmethod
	def getInstance():
		if AnalyzerCommunication.__instance == None:
			AnalyzerCommunication()
		return AnalyzerCommunication.__instance

	def __init__(self):
		if AnalyzerCommunication.__instance != None:
			raise Exception("AnalyzerCommunication is a singleton!")
		else:
			AnalyzerCommunication.__instance = self

		self.visaResourceManager = None
		self.session = None

	def checkAnalyzerConnection(self, analyzerAddress):
		try:
			analyzerAddress = 'TCPIP0::'+ analyzerAddress +'::inst0::INSTR'
			self.resourceManager = visa.ResourceManager()
			self.session = self.resourceManager.open_resource(analyzerAddress)
			return "OK"
		except visa.Error as ex:
			return "{0}".format(ex)
		finally:
			self.closeConnection()

	def getDataTest(self):
		try:
			analyzerAddress = 'TCPIP0::192.168.253.253::inst0::INSTR'
			self.resourceManager = visa.ResourceManager()
			self.session = self.resourceManager.open_resource(analyzerAddress)
			self.session.write(':SENS:DATA:CORR? S11')
			result = self.session.read()
			listRes = result.split(',')
			print('........number of data: {0}'.format(len(listRes)))
			print('...............result is: {0}'.format(result))
			self.session.write(':SENS1:FREQ:DATA?')
			freqRes = self.session.read()
			print('...............freq res: {0}'.format(freqRes))
			print('..........number of freq res: {0}'.format(len(freqRes.split(','))))
		except visa.Error as ex:
			wx.MessageBox('errror: {0}'.format(ex))
		finally:
			self.closeConnection()

	def closeConnection(self):
		if self.session is not None:
			self.session.close()
		if self.visaResourceManager is not None:
			self.visaResourceManager.close()