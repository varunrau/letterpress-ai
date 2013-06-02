
class Side():
	"""
	An object to represent the side of a letter.
	"""

	def __init__(self, team=None):
		self.team = team

	def changeTeam(self, team):
		self.team = team

	def __repr__(self):
		return str(self.team) if self.team else "NOT ASSIGNED"

	def isAssigned(self):
		return self.team is not None

	def __eq__(self, otherSide):
		return str(self) == str(otherSide)

