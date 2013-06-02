
class Move:
	"""
	A class that represents a move.
	"""

	def __init__(self, letters):
		"""
		Constructs a move object.
		@param letters - A list of letter objects.
		"""
		self.letters = letters

	def __hash__(self):
		return hash(str(self.letters))

	def getWord(self):
		"""
		Returns the letters of the move.
		@return a list of letter objects.
		"""
		return self.letters

	def __str__(self):
		toPrint = ""
		for letter in self.getWord():
			toPrint += str(letter)
		return toPrint

	def __eq__(self, otherMove):
		otherWord = otherMove.getWord()
		if not len(self.letters) == len(otherWord):
			return False
		for i in xrange(len(self.letters)):
			if not self.letters[i] == otherWord[i]:
				return False
		return True
