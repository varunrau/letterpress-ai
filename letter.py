from side import Side
import random
import colors

class Letter():

	def __init__(self, pos=None, value=None, color=None):
		self.position = pos
		self.value = value if value else self.randomValue()
		self.color = color if color else Side()
		self.protected = False

	def changeTeam(self, team):
		if not self.protected:
			self.color.changeTeam(team)

	def randomValue(self):
		return chr(random.randint(97, 122))


	def getStringVal(self):
		color = colors.Color.GREEN
		if self.color.team == "RED":
			color = colors.Color.RED
		elif self.color.team == "BLUE":
			color = colors.Color.BLUE
		return color + str(self.value).upper()  + colors.Color.END


	def __repr__(self):
		return self.getStringVal()

	def __str__(self):
		return self.getStringVal()


	def __eq__(self, letter):
		return self.value == letter.value

