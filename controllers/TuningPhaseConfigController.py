from models.TuningPhase import TuningPhase
from views.TuningPhaseConfigGUI import TuningPhaseConfigGUI

class TuningPhaseConfigController:
	def __init__(self, model: TuningPhase):
		self.model = model

	def initialView(self, parentGUI):
		tuningPhaseGUI = TuningPhaseConfigGUI(parentGUI, self.model)
		return tuningPhaseGUI