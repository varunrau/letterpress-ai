from side import Side
import random
import colors

class Letter():
	"""
	A class that represents a letter.
	"""

	def __init__(self, pos, value=None, color=None):
		"""
		Constructs a letter.
		@param pos - the position of the letter on the board.
		@param value - The value of the letter. (eg. 'a'). A String. Optional.
		@pararm color - the color of the letter. A Side object. Defaults to no color.
		"""
		self.position = pos
		self.value = value if value else self._randomValue()
		self.color = color if color else Side()
		self.protected = False

	def changeTeam(self, team):
		"""
		Switches sides if the letter is not protected.
		@param team - the team to switch to.
		"""
		if not self.protected:
			self.color.changeTeam(team)

	def _randomValue(self):
		return chr(random.randint(97, 122))


	def getStringVal(self):
		"""
		The string representation of the letter with color.
		@return the string.
		"""
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

