from pubsub import pub
from topics import Topics

class Publisher:
	@staticmethod
	def moneyChanged(money):
		#pub.sendMessage(Topics.money_changed.name, money)
		pub.sendMessage("money_changed", 20)	