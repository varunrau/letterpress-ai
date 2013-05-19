from side import Side
import random

class Letter():

	def __init__(self, pos=None, value=None, color=None):

		self.position = pos

		if value:
			self.value = value
		else:
			self.value = self.randomValue()

		if color:
			self.color = color
		else:
			self.color = Side()

		self.protected = False

	def changeTeam(self, team):
		if not self.protected:
			self.changeColor(team)

	def changeColor(self, team):
		self.color = team

	def randomValue(self):
		return chr(random.randint(65, 90))

	def __repr__(self):
		return self.value + str(self.color)

	def __str__(self):
		return self.value

	def __eq__(self, letter):
		return self.value == letter.value

