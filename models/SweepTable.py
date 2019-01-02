class SweepTable:
	def __init__(self, startFreq: float = None, stopFreq: float = None, numberPoints: int = None, IFBW: float = None, Power: float = None):
		self.startFreq: float = startFreq if startFreq is not None else 0
		self.stopFreq: float = stopFreq if stopFreq is not None else 0
		self.numberPoints: int = numberPoints if numberPoints is not None else 0
		self.IFBW: float = IFBW if IFBW is not None else 0 
		self.Power: float = Power if Power is not None else 0